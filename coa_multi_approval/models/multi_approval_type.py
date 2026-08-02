from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MultiApprovalType(models.Model):
    _name = 'multi.approval.type'
    _description = 'Multi Approval Type'
    _order = 'model, sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(default=10)
    model_id = fields.Many2one(
        'ir.model', string='Document Model', required=True,
        domain=[('model', 'in', [
            'sale.order',
            'purchase.order',
            'account.move',
            'account.payment',
            'stock.picking',
        ])],
        ondelete='cascade',
    )
    model = fields.Char(related='model_id.model', store=True, string='Model Technical Name')
    active = fields.Boolean(default=True)

    trigger = fields.Selection([
        ('on_save',  'On Save / Create (auto-submit, blocks everything until approved)'),
        ('confirm',  'On Confirm / Post / Validate'),
        ('send',     'On Send Quotation by Email (Sales only)'),
        ('print',    'On Print PDF (Sales only)'),
    ], string='Approval Trigger', default='confirm', required=True,
       help='When should the approval be requested?\n'
            '• On Save/Create: auto-triggers the moment a new quotation is saved.\n'
            '  Blocks printing, sending, and confirming until fully approved.\n'
            '• On Confirm: blocks confirming orders, posting invoices, validating transfers.\n'
            '• On Send: blocks the "Send by Email" button on Quotations.\n'
            '• On Print PDF: blocks printing the Quotation PDF.')

    record_domain = fields.Char(
        string='Record Filter (Domain)',
        help='Optional domain expression to restrict which records require this approval.\n'
             'Examples:\n'
             '  Journal Entries only: [(\'move_type\', \'=\', \'entry\')]\n'
             '  Invoices only:        [(\'move_type\', \'in\', [\'out_invoice\', \'in_invoice\'])]\n'
             'Leave empty to apply to ALL records of this model.',
    )

    is_active_approval = fields.Boolean(
        string='Enable Approval',
        default=True,
        help='When enabled, documents matching this configuration require approval.',
    )
    auto_confirm = fields.Boolean(
        string='Auto-Confirm After Approval',
        default=False,
        help='Automatically confirm/post/validate the document once all stages are approved.',
    )
    stage_ids = fields.One2many('multi.approval.stage', 'type_id', string='Approval Stages')
    stage_count = fields.Integer(compute='_compute_stage_count', string='Stages')
    description = fields.Text(string='Description / Instructions')

    # Stored computed field used by the Kanban card to avoid JS null-domain errors
    card_type = fields.Char(
        compute='_compute_card_type', store=True,
        help='Internal identifier used to pick the right kanban card template.',
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'An approval configuration with this name already exists!'),
    ]

    @api.depends('stage_ids')
    def _compute_stage_count(self):
        for rec in self:
            rec.stage_count = len(rec.stage_ids)

    @api.depends('model', 'trigger', 'record_domain')
    def _compute_card_type(self):
        for rec in self:
            if rec.model == 'sale.order' and rec.trigger == 'on_save':
                rec.card_type = 'sale_on_save'
            elif rec.model == 'sale.order' and rec.trigger == 'send':
                rec.card_type = 'sale_send'
            elif rec.model == 'sale.order' and rec.trigger == 'print':
                rec.card_type = 'sale_print'
            elif rec.model == 'sale.order':
                rec.card_type = 'sale_confirm'
            elif rec.model == 'purchase.order':
                rec.card_type = 'purchase'
            elif rec.model == 'account.move' and rec.record_domain and 'entry' in rec.record_domain:
                rec.card_type = 'journal'
            elif rec.model == 'account.move':
                rec.card_type = 'invoice'
            elif rec.model == 'account.payment':
                rec.card_type = 'payment'
            elif rec.model == 'stock.picking':
                rec.card_type = 'inventory'
            else:
                rec.card_type = 'other'


class MultiApprovalStage(models.Model):
    _name = 'multi.approval.stage'
    _description = 'Multi Approval Stage'
    _order = 'type_id, sequence, id'

    name = fields.Char(string='Stage Name', required=True)
    type_id = fields.Many2one(
        'multi.approval.type', string='Approval Type', required=True, ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=10)
    approver_ids = fields.Many2many(
        'res.users',
        'multi_approval_stage_approver_rel',
        'stage_id', 'user_id',
        string='Approvers',
        domain=[('share', '=', False)],
    )
    approval_type = fields.Selection([
        ('any',     'Any One Approver'),
        ('all',     'All Approvers'),
        ('minimum', 'Minimum Number of Approvers'),
    ], string='Approval Requirement', default='any', required=True)
    min_approvals = fields.Integer(
        string='Minimum Approvals', default=1,
        help='Minimum number of approvals required to pass this stage.',
    )
    note = fields.Text(string='Stage Instructions')

    @api.constrains('min_approvals', 'approver_ids', 'approval_type')
    def _check_min_approvals(self):
        for stage in self:
            if stage.approval_type == 'minimum':
                if stage.min_approvals < 1:
                    raise ValidationError(_('Minimum approvals must be at least 1.'))
                if stage.approver_ids and stage.min_approvals > len(stage.approver_ids):
                    raise ValidationError(_(
                        'Minimum approvals (%d) cannot exceed the number of approvers (%d).',
                        stage.min_approvals, len(stage.approver_ids)
                    ))
