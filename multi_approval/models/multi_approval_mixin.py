from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MultiApprovalMixin(models.AbstractModel):
    _name = 'multi.approval.mixin'
    _description = 'Multi Approval Mixin'

    approval_request_id = fields.Many2one(
        'multi.approval.request',
        string='Approval Request',
        copy=False,
        readonly=True,
    )
    approval_state = fields.Selection(
        related='approval_request_id.state',
        string='Approval Status',
        store=True,
    )
    can_approve = fields.Boolean(
        compute='_compute_can_approve',
        string='Can Approve',
    )
    approval_current_stage = fields.Char(
        related='approval_request_id.current_stage_id.name',
        string='Current Approval Stage',
    )

    @api.depends('approval_request_id', 'approval_request_id.state',
                 'approval_request_id.current_stage_id',
                 'approval_request_id.line_ids.status')
    def _compute_can_approve(self):
        user = self.env.user
        for rec in self:
            can = False
            if rec.approval_request_id and rec.approval_request_id.state == 'pending':
                current_stage = rec.approval_request_id.current_stage_id
                pending_line = rec.approval_request_id.line_ids.filtered(
                    lambda l: l.stage_id == current_stage
                    and l.approver_id == user
                    and l.status == 'pending'
                )
                can = bool(pending_line)
            rec.can_approve = can

    def _get_approval_type(self, trigger='confirm'):
        """Return the first active approval type matching this record, trigger, and domain."""
        self.ensure_one()
        types = self.env['multi.approval.type'].search([
            ('model', '=', self._name),
            ('is_active_approval', '=', True),
            ('active', '=', True),
            ('trigger', '=', trigger),
        ], order='sequence, id')

        for approval_type in types:
            if approval_type.record_domain:
                try:
                    domain = safe_eval(approval_type.record_domain)
                    if self.filtered_domain(domain):
                        return approval_type
                except Exception:
                    continue
            else:
                return approval_type
        return self.env['multi.approval.type']

    def action_submit_for_approval(self):
        self.ensure_one()
        # Try both triggers to find the relevant one from context
        trigger = self.env.context.get('approval_trigger', 'confirm')
        approval_type = self._get_approval_type(trigger=trigger)
        if not approval_type:
            # Fallback: try confirm trigger
            approval_type = self._get_approval_type(trigger='confirm')
        if not approval_type:
            raise UserError(_(
                'No approval configuration found for this document.\n'
                'Please configure one under Approvals > Configuration > Approval Settings.'
            ))
        if not approval_type.stage_ids:
            raise UserError(_('No approval stages configured. Please add stages in Approvals > Configuration > Approval Settings.'))

        # Cancel any previous pending request
        if self.approval_request_id and self.approval_request_id.state not in ('approved', 'cancel'):
            self.approval_request_id.action_cancel()

        request = self.env['multi.approval.request'].create({
            'name': '/',
            'type_id': approval_type.id,
            'res_model': self._name,
            'res_id': self.id,
            'res_name': self.display_name,
        })
        self.approval_request_id = request
        request.action_submit()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'multi.approval.request',
            'res_id': request.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_approve_request(self):
        self.ensure_one()
        if not self.approval_request_id:
            raise UserError(_('No active approval request found.'))
        self.approval_request_id.action_approve()

    def action_refuse_request(self):
        self.ensure_one()
        if not self.approval_request_id:
            raise UserError(_('No active approval request found.'))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'multi.approval.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_request_id': self.approval_request_id.id},
        }

    def action_view_approval_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'multi.approval.request',
            'res_id': self.approval_request_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _check_approval_before_action(self, trigger='confirm'):
        """Raise UserError if approval is required and not yet granted.

        Priority 1 – Global pending block:
          Any pending approval (e.g. on_save) stops ALL actions immediately.
        Priority 2 – Trigger-specific block:
          If a specific trigger type is configured and not yet submitted/approved,
          stop that specific action.
        """
        for rec in self:
            # ── Global block: pending on_save (or any) approval blocks everything ──
            if rec.approval_request_id and rec.approval_request_id.state == 'pending':
                raise UserError(_(
                    'This document is waiting for approval at stage: "%s".\n'
                    'You cannot perform any action until it is fully approved.'
                ) % (rec.approval_request_id.current_stage_id.name or ''))

            # ── Trigger-specific block: approval not yet submitted ──
            approval_type = rec._get_approval_type(trigger=trigger)
            if not approval_type or not approval_type.stage_ids:
                continue
            if not rec.approval_request_id or rec.approval_request_id.state in ('refused', 'cancel'):
                raise UserError(_(
                    'This document requires approval before this action.\n'
                    'Please click "Submit for Approval" first.'
                ))

    def _on_approval_approved(self):
        pass

    def _on_approval_refused(self):
        pass
