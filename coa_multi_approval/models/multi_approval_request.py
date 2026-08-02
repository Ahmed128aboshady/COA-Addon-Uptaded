from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MultiApprovalRequest(models.Model):
    _name = 'multi.approval.request'
    _description = 'Multi Approval Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(string='Request Reference', required=True, readonly=True, default='/')
    type_id = fields.Many2one(
        'multi.approval.type', string='Approval Type', required=True, readonly=True,
    )
    res_model = fields.Char(string='Document Model', readonly=True)
    res_id = fields.Integer(string='Document ID', readonly=True)
    res_name = fields.Char(string='Document Reference', readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Fully Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, readonly=True)

    current_stage_id = fields.Many2one('multi.approval.stage', string='Current Stage', readonly=True)
    line_ids = fields.One2many('multi.approval.line', 'request_id', string='Approval Lines')

    requester_id = fields.Many2one(
        'res.users', string='Requested By',
        default=lambda self: self.env.user, readonly=True,
    )
    request_date = fields.Datetime(string='Request Date', default=fields.Datetime.now, readonly=True)
    refuse_reason = fields.Text(string='Refusal Reason', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # Progress info
    approved_stages = fields.Integer(compute='_compute_progress', string='Approved Stages')
    total_stages = fields.Integer(compute='_compute_progress', string='Total Stages')

    @api.depends('line_ids.status', 'current_stage_id', 'type_id.stage_ids')
    def _compute_progress(self):
        for rec in self:
            rec.total_stages = len(rec.type_id.stage_ids)
            if rec.state == 'approved':
                rec.approved_stages = rec.total_stages
            elif rec.current_stage_id:
                all_stages = rec.type_id.stage_ids.sorted('sequence')
                idx = list(all_stages.ids).index(rec.current_stage_id.id) if rec.current_stage_id.id in all_stages.ids else 0
                rec.approved_stages = idx
            else:
                rec.approved_stages = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('multi.approval.request') or '/'
        return super().create(vals_list)

    def action_submit(self):
        """Submit the approval request - notify first stage approvers."""
        self.ensure_one()
        if not self.type_id.stage_ids:
            raise UserError(_('No approval stages are configured for this approval type. Please configure at least one stage.'))

        first_stage = self.type_id.stage_ids.sorted('sequence')[0]
        if not first_stage.approver_ids:
            raise UserError(_('Stage "%s" has no approvers configured.') % first_stage.name)

        self.write({
            'current_stage_id': first_stage.id,
            'state': 'pending',
        })
        self._create_lines_for_stage(first_stage)
        self._notify_approvers(first_stage)
        self.message_post(
            body=_('Approval request submitted. Awaiting approval for stage: <b>%s</b>') % first_stage.name,
            message_type='notification',
        )

    def _create_lines_for_stage(self, stage):
        """Create approval lines for the given stage (idempotent)."""
        existing_approvers = self.line_ids.filtered(lambda l: l.stage_id == stage).mapped('approver_id')
        for approver in stage.approver_ids:
            if approver not in existing_approvers:
                self.env['multi.approval.line'].create({
                    'request_id': self.id,
                    'stage_id': stage.id,
                    'approver_id': approver.id,
                    'status': 'pending',
                })

    def _notify_approvers(self, stage):
        """Create activities for all approvers of a stage."""
        for approver in stage.approver_ids:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=approver.id,
                note=_('Please review and approve: %s') % self.name,
                summary=_('Approval Required'),
            )

    def action_approve(self):
        """Called when the current user clicks Approve."""
        self.ensure_one()
        user = self.env.user
        line = self.line_ids.filtered(
            lambda l: l.stage_id == self.current_stage_id
            and l.approver_id == user
            and l.status == 'pending'
        )
        if not line:
            raise UserError(_('You are not listed as an approver for the current stage, or you have already responded.'))

        line.write({'status': 'approved', 'date': fields.Datetime.now()})
        # Mark activities done for this user
        self.activity_ids.filtered(lambda a: a.user_id == user).action_done()

        self.message_post(
            body=_('<b>%s</b> approved stage: <b>%s</b>') % (user.name, self.current_stage_id.name),
            message_type='notification',
        )
        self._check_stage_completion()

    def action_refuse(self, reason=''):
        """Called when the current user refuses the request."""
        self.ensure_one()
        user = self.env.user
        line = self.line_ids.filtered(
            lambda l: l.stage_id == self.current_stage_id
            and l.approver_id == user
            and l.status == 'pending'
        )
        if not line:
            raise UserError(_('You are not listed as an approver for the current stage, or you have already responded.'))

        line.write({'status': 'refused', 'date': fields.Datetime.now()})
        self.write({
            'refuse_reason': reason,
            'state': 'refused',
        })
        # Cancel remaining activities
        self.activity_ids.unlink()

        self.message_post(
            body=_('<b>%s</b> refused stage: <b>%s</b>.<br/>Reason: %s') % (
                user.name, self.current_stage_id.name, reason or _('No reason provided')
            ),
            message_type='notification',
        )
        self._notify_document_refused()

    def _check_stage_completion(self):
        """Check if current stage requirements are met; advance or finalize."""
        stage = self.current_stage_id
        stage_lines = self.line_ids.filtered(lambda l: l.stage_id == stage)
        approved_count = len(stage_lines.filtered(lambda l: l.status == 'approved'))
        total_count = len(stage_lines)

        stage_complete = False
        if stage.approval_type == 'any':
            stage_complete = approved_count >= 1
        elif stage.approval_type == 'all':
            stage_complete = approved_count == total_count
        elif stage.approval_type == 'minimum':
            stage_complete = approved_count >= stage.min_approvals

        if not stage_complete:
            return

        # Find next stage
        next_stages = self.type_id.stage_ids.filtered(
            lambda s: s.sequence > stage.sequence
        ).sorted('sequence')

        if next_stages:
            next_stage = next_stages[0]
            if not next_stage.approver_ids:
                raise UserError(_('Stage "%s" has no approvers configured.') % next_stage.name)
            self.current_stage_id = next_stage
            self._create_lines_for_stage(next_stage)
            self._notify_approvers(next_stage)
            self.message_post(
                body=_('Stage <b>%s</b> completed. Moving to next stage: <b>%s</b>') % (stage.name, next_stage.name),
                message_type='notification',
            )
        else:
            # All stages approved
            self.state = 'approved'
            self.activity_ids.unlink()
            self.message_post(
                body=_('All approval stages completed. Request fully <b>approved</b>!'),
                message_type='notification',
            )
            self._notify_document_approved()

    def _notify_document_approved(self):
        """Callback to the source document once fully approved."""
        if self.res_model and self.res_id:
            doc = self.env[self.res_model].browse(self.res_id).exists()
            if doc and hasattr(doc, '_on_approval_approved'):
                doc._on_approval_approved()

    def _notify_document_refused(self):
        """Callback to the source document when refused."""
        if self.res_model and self.res_id:
            doc = self.env[self.res_model].browse(self.res_id).exists()
            if doc and hasattr(doc, '_on_approval_refused'):
                doc._on_approval_refused()

    def action_cancel(self):
        self.ensure_one()
        self.activity_ids.unlink()
        self.state = 'cancel'
        self.message_post(body=_('Approval request cancelled.'), message_type='notification')

    def action_reset_draft(self):
        self.ensure_one()
        self.write({'state': 'draft', 'current_stage_id': False, 'refuse_reason': False})
        self.line_ids.unlink()
        self.message_post(body=_('Approval request reset to draft.'), message_type='notification')

    def action_open_document(self):
        """Open the related document."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self.res_model,
            'res_id': self.res_id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_refuse_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'multi.approval.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_request_id': self.id},
        }


class MultiApprovalLine(models.Model):
    _name = 'multi.approval.line'
    _description = 'Multi Approval Line'
    _order = 'stage_sequence, id'

    request_id = fields.Many2one(
        'multi.approval.request', string='Approval Request', required=True, ondelete='cascade',
    )
    stage_id = fields.Many2one('multi.approval.stage', string='Stage', required=True)
    stage_sequence = fields.Integer(related='stage_id.sequence', store=True)
    stage_name = fields.Char(related='stage_id.name', string='Stage Name')
    approver_id = fields.Many2one('res.users', string='Approver', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
    ], string='Status', default='pending', required=True)
    date = fields.Datetime(string='Decision Date')
    comment = fields.Text(string='Comment')
    is_current_stage = fields.Boolean(
        compute='_compute_is_current_stage', string='Is Current Stage',
    )

    @api.depends('stage_id', 'request_id.current_stage_id')
    def _compute_is_current_stage(self):
        for line in self:
            line.is_current_stage = (line.stage_id == line.request_id.current_stage_id)
