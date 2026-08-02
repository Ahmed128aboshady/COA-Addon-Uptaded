from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, UserError


class PettyCashCustody(models.Model):
    _name = 'petty.cash.custody'
    _description = 'Petty Cash Custody'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(
        string='Custody Number',
        required=True, copy=False, readonly=True,
        default=lambda self: 'New'
    )
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True, tracking=True
    )
    user_id = fields.Many2one(
        related='employee_id.user_id', string='User', store=True
    )
    date = fields.Date(
        string='Custody Date', required=True,
        default=fields.Date.today, tracking=True
    )
    amount = fields.Monetary(
        string='Custody Amount', required=True, tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)

    current_approval_level = fields.Integer(
        string='Current Approval Level', default=0, copy=False,
        help='0 = not yet submitted for approval'
    )

    # Accounting
    journal_id = fields.Many2one(
        'account.journal', string='Journal',
        domain="[('type', 'in', ['cash', 'bank', 'general'])]",
        help='Journal where custody entries will be recorded'
    )
    payment_account_id = fields.Many2one(
        'account.account',
        string='Cash/Bank Account',
        required=True,
        tracking=True,
        domain="[('account_type', 'in', ['asset_cash', 'asset_current', 'liability_current'])]",
        help='Credit account when disbursing custody (cash or bank paying account)',
    )
    move_id = fields.Many2one(
        'account.move', string='Journal Entry',
        readonly=True, copy=False
    )
    move_state = fields.Selection(
        related='move_id.state', string='Entry Status'
    )

    expense_ids = fields.One2many(
        'petty.cash.expense', 'custody_id', string='Expenses'
    )
    total_expenses = fields.Monetary(
        string='Total Expenses', compute='_compute_totals', store=True
    )
    remaining_amount = fields.Monetary(
        string='Remaining Amount', compute='_compute_totals', store=True
    )
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company
    )

    @api.depends('expense_ids.amount', 'expense_ids.state', 'amount')
    def _compute_totals(self):
        for rec in self:
            approved = rec.expense_ids.filtered(lambda e: e.state == 'approved')
            rec.total_expenses = sum(approved.mapped('amount'))
            rec.remaining_amount = rec.amount - rec.total_expenses

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'petty.cash.custody') or 'New'
        return super().create(vals_list)

    def _get_petty_cash_account(self):
        """Get custody account from Settings"""
        ICP = self.env['ir.config_parameter'].sudo()
        account_id = ICP.get_param('petty_cash.account_id')
        if not account_id:
            raise UserError(_(
                'Please configure the Petty Cash Account in Settings first!\n'
                'Settings \u2192 Petty Cash \u2192 Petty Cash Account'
            ))
        return self.env['account.account'].browse(int(account_id))

    def _get_employee_partner(self):
        """Get employee partner - work contact or user partner"""
        self.ensure_one()
        return (
            self.employee_id.work_contact_id
            or (self.employee_id.user_id.partner_id if self.employee_id.user_id else self.env['res.partner'])
        )

    def _create_custody_journal_entry(self):
        """Create custody grant entry:
           Debit:  Petty Cash Account (employee)
           Credit: Cash/Bank Account (from custody)
        """
        self.ensure_one()
        petty_account = self._get_petty_cash_account()
        payment_account = self.payment_account_id
        if not payment_account:
            raise UserError(_('Please specify the Cash/Bank Account on the custody!'))

        journal = self.journal_id or self.env['account.journal'].search(
            [('type', 'in', ['cash', 'bank'])], limit=1
        )
        if not journal:
            raise UserError(_('No cash or bank journal found!'))

        partner = self._get_employee_partner()
        partner_id = partner.id if partner else False

        move_vals = {
            'journal_id': journal.id,
            'date': self.date,
            'ref': '%s - %s' % (self.name, self.employee_id.name),
            'line_ids': [
                (0, 0, {
                    'account_id': petty_account.id,
                    'name': '%s - %s - %s' % (
                        _('Petty Cash Custody'),
                        self.employee_id.name,
                        self.name,
                    ),
                    'debit': self.amount,
                    'credit': 0.0,
                    'partner_id': partner_id,
                }),
                (0, 0, {
                    'account_id': payment_account.id,
                    'name': '%s - %s - %s' % (
                        _('Custody Disbursement'),
                        self.employee_id.name,
                        self.name,
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

    def action_submit_for_approval(self):
        """Submit custody for approval - starts at the first level"""
        Approver = self.env['petty.cash.approver']
        first_level = Approver._get_first_level('custody')

        for rec in self:
            if first_level:
                level_records = Approver._get_approvers_at_level('custody', first_level)
                approvers = level_records.mapped('user_ids')
                rec.write({'state': 'pending_approval', 'current_approval_level': first_level})
                rec.message_post(
                    body=_(
                        '\U0001f4cb <b>Custody Approval Request - Level %(level)s</b><br/>'
                        'Custody No: <b>%(name)s</b><br/>'
                        'Employee: %(employee)s<br/>'
                        'Amount: <b>%(amount)s %(currency)s</b><br/>'
                        'Date: %(date)s<br/>'
                        '<a href="/odoo/petty-cash/custody/%(id)s">Open Custody</a>'
                    ) % {
                        'level': first_level,
                        'name': rec.name,
                        'employee': rec.employee_id.name,
                        'amount': '%.2f' % rec.amount,
                        'currency': rec.currency_id.symbol,
                        'date': rec.date,
                        'id': rec.id,
                    },
                    partner_ids=approvers.mapped('partner_id').ids,
                    message_type='notification',
                    subtype_xmlid='mail.mt_note',
                )
            else:
                rec.write({'state': 'pending_approval', 'current_approval_level': 0})
                rec.message_post(
                    body=_('Custody submitted for approval (no approvers configured)'),
                    message_type='notification',
                    subtype_xmlid='mail.mt_note',
                )

    def action_approve(self):
        """Approve custody with multi-level approval support"""
        Approver = self.env['petty.cash.approver']

        for rec in self:
            current_level = rec.current_approval_level
            all_records = Approver._get_records_for_type('custody')

            if all_records and current_level > 0:
                # Verify current user is an approver at this level
                level_records = all_records.filtered(lambda r: r.level == current_level)
                level_users = level_records.mapped('user_ids')
                if level_users and self.env.user not in level_users:
                    names = ', '.join(level_users.mapped('name'))
                    raise UserError(_(
                        'You are not authorized to approve at level %s!\n'
                        'Authorized approvers: %s'
                    ) % (current_level, names))

                # Is there a next level?
                next_level = Approver._get_next_level('custody', current_level)
                if next_level:
                    next_records = all_records.filtered(lambda r: r.level == next_level)
                    next_users = next_records.mapped('user_ids')
                    rec.write({'current_approval_level': next_level})
                    rec.message_post(
                        body=_(
                            '\u2705 <b>Level %(level)s approved</b> by <b>%(user)s</b><br/>'
                            '\u23f3 Awaiting Level %(next)s approval...<br/>'
                            '<a href="/odoo/petty-cash/custody/%(id)s">Open Custody</a>'
                        ) % {
                            'level': current_level,
                            'user': self.env.user.name,
                            'next': next_level,
                            'id': rec.id,
                        },
                        partner_ids=next_users.mapped('partner_id').ids,
                        message_type='notification',
                        subtype_xmlid='mail.mt_note',
                    )
                    continue  # Don't finalize yet

            elif all_records and current_level == 0:
                all_users = all_records.mapped('user_ids')
                if all_users and self.env.user not in all_users:
                    names = ', '.join(all_users.mapped('name'))
                    raise UserError(_(
                        'You are not authorized to approve this custody!\n'
                        'Authorized approvers: %s'
                    ) % names)

            # Final approval
            move = rec._create_custody_journal_entry()
            rec.write({'state': 'approved', 'move_id': move.id, 'current_approval_level': 0})
            rec.message_post(
                body=_('\u2705 <b>Custody finally approved</b> by <b>%s</b>') % self.env.user.name,
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )

    def action_refuse(self):
        """Refuse custody and reset to draft"""
        for rec in self:
            rec.write({'state': 'draft', 'current_approval_level': 0})
            rec.message_post(
                body=_('\u274c Custody refused by <b>%s</b>') % self.env.user.name,
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )

    def action_close(self):
        self.write({'state': 'closed'})

    def action_reset_draft(self):
        for rec in self:
            if rec.move_id and rec.move_id.state == 'posted':
                rec.move_id.button_draft()
                rec.move_id.button_cancel()
        self.write({'state': 'draft', 'current_approval_level': 0})

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
                raise ValidationError(_('Custody amount must be greater than zero!'))
