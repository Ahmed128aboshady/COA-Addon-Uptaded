from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, UserError


class PettyCashExpense(models.Model):
    _name = 'petty.cash.expense'
    _description = 'Petty Cash Expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(
        string='Expense Number', required=True, copy=False,
        readonly=True, default=lambda self: 'New'
    )
    custody_id = fields.Many2one(
        'petty.cash.custody', string='Custody', required=True, tracking=True,
        domain="[('state', '=', 'approved')]"
    )
    employee_id = fields.Many2one(
        related='custody_id.employee_id', string='Employee', store=True
    )
    user_id = fields.Many2one(
        related='custody_id.user_id', string='User', store=True
    )
    date = fields.Date(
        string='Expense Date', required=True,
        default=fields.Date.today, tracking=True
    )
    description = fields.Char(string='Description', required=True)
    amount = fields.Monetary(string='Amount', required=True, tracking=True)
    currency_id = fields.Many2one(
        related='custody_id.currency_id', string='Currency', store=True
    )

    # Category with account
    category_id = fields.Many2one(
        'petty.cash.category', string='Category', required=True, tracking=True
    )
    account_id = fields.Many2one(
        related='category_id.account_id',
        string='Account', store=True, readonly=True
    )
    analytic_distribution = fields.Json(
        string='Analytic Distribution',
        help='Takes default from category'
    )
    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get('Percentage Analytic'),
    )

    receipt = fields.Binary(string='Receipt')
    receipt_filename = fields.Char(string='Filename')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)

    # Accounting
    move_id = fields.Many2one(
        'account.move', string='Journal Entry',
        readonly=True, copy=False
    )
    move_state = fields.Selection(
        related='move_id.state', string='Entry Status'
    )
    company_id = fields.Many2one(
        related='custody_id.company_id', store=True
    )

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id and self.category_id.analytic_account_id:
            self.analytic_distribution = {
                str(self.category_id.analytic_account_id.id): 100
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'petty.cash.expense') or 'New'
        return super().create(vals_list)

    def action_submit(self):
        for rec in self:
            if rec.amount > rec.custody_id.remaining_amount:
                raise ValidationError(_(
                    'Amount (%(amount)s) exceeds the remaining custody balance (%(remaining)s)!'
                ) % {
                    'amount': rec.amount,
                    'remaining': rec.custody_id.remaining_amount,
                })
        self.write({'state': 'submitted'})
        for rec in self:
            approvers = self.env['petty.cash.approver']._get_approvers_for_type('expense')
            if approvers:
                rec.message_post(
                    body=_(
                        '<b>Expense Approval Request</b><br/>'
                        'Employee: %(employee)s<br/>'
                        'Amount: %(amount)s %(currency)s<br/>'
                        'Description: %(desc)s'
                    ) % {
                        'employee': rec.employee_id.name,
                        'amount': rec.amount,
                        'currency': rec.currency_id.symbol,
                        'desc': rec.description,
                    },
                    partner_ids=approvers.mapped('partner_id').ids,
                    message_type='notification',
                    subtype_xmlid='mail.mt_note',
                )

    def _create_expense_journal_entry(self):
        """Create expense entry:
           Debit:  Expense account (from category)
           Credit: Petty Cash account
        """
        self.ensure_one()
        if not self.category_id.account_id:
            raise UserError(
                _('Category "%s" has no accounting account!') % self.category_id.name
            )

        ICP = self.env['ir.config_parameter'].sudo()
        custody_account_id = ICP.get_param('petty_cash.account_id')
        if not custody_account_id:
            raise UserError(_('Please configure the Petty Cash Account in Settings!'))
        custody_account = self.env['account.account'].browse(int(custody_account_id))

        journal = self.custody_id.journal_id or self.env['account.journal'].search(
            [('type', 'in', ['cash', 'general'])], limit=1
        )

        analytic_distribution = self.analytic_distribution or None

        # Get employee partner
        employee = self.employee_id
        partner = (
            employee.work_contact_id
            or (employee.user_id.partner_id if employee.user_id else self.env['res.partner'])
        )
        partner_id = partner.id if partner else False

        move_vals = {
            'journal_id': journal.id,
            'date': self.date,
            'ref': '%s - %s' % (self.name, self.description),
            'line_ids': [
                # Debit: category expense account
                (0, 0, {
                    'account_id': self.category_id.account_id.id,
                    'name': '%s - %s' % (self.description, self.name),
                    'debit': self.amount,
                    'credit': 0.0,
                    'partner_id': partner_id,
                    'analytic_distribution': analytic_distribution or None,
                }),
                # Credit: petty cash account
                (0, 0, {
                    'account_id': custody_account.id,
                    'name': '%s - %s - %s' % (
                        _('Custody Settlement'),
                        self.custody_id.name,
                        self.employee_id.name,
                    ),
                    'debit': 0.0,
                    'credit': self.amount,
                    'partner_id': partner_id,
                }),
            ]
        }
        move = self.env['account.move'].create(move_vals)
        move.action_post()
        return move

    def action_approve(self):
        # Check approval permission
        approvers = self.env['petty.cash.approver']._get_approvers_for_type('expense')
        if approvers and self.env.user not in approvers:
            names = ', '.join(approvers.mapped('name'))
            raise UserError(_(
                'You are not authorized to approve this expense!\n'
                'Authorized approvers: %s'
            ) % names)
        for rec in self:
            move = rec._create_expense_journal_entry()
            rec.write({'state': 'approved', 'move_id': move.id})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_reset_draft(self):
        for rec in self:
            if rec.move_id and rec.move_id.state == 'posted':
                rec.move_id.button_draft()
                rec.move_id.button_cancel()
        self.write({'state': 'draft', 'move_id': False})

    def action_view_journal_entry(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entry'),
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'view_mode': 'form',
        }

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_('Amount must be greater than zero!'))
