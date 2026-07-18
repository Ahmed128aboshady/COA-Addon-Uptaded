# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CoaAccruedExpense(models.Model):
    _name = 'coa.accrued.expense'
    _description = 'Accrued Expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    name = fields.Char(
        string='Reference', required=True, copy=False, readonly=True,
        default=lambda self: _('New'), tracking=True)
    description = fields.Char(
        string='Description', required=True, tracking=True,
        help='e.g. Office Rent Contract 2026')
    partner_id = fields.Many2one(
        'res.partner', string='Vendor', required=True, tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        related='company_id.currency_id', string='Currency')

    expense_account_id = fields.Many2one(
        'account.account', string='Expense Account', required=True,
        check_company=True, tracking=True,
        domain="[('account_type', 'in', ('expense', 'expense_depreciation', 'expense_direct_cost')), ('deprecated', '=', False)]",
        help='Debited every month (e.g. Rent Expense).')
    accrual_account_id = fields.Many2one(
        'account.account', string='Accrued Expense Account', required=True,
        check_company=True, tracking=True,
        domain="[('account_type', 'in', ('liability_current', 'liability_payable')), ('deprecated', '=', False)]",
        help='Credited every month (liability). The vendor bill will be '
             'booked against this account to settle the accrual.')
    journal_id = fields.Many2one(
        'account.journal', string='Accrual Journal', required=True,
        check_company=True, tracking=True,
        domain="[('type', '=', 'general')]",
        default=lambda self: self.env['account.journal'].search(
            [('type', '=', 'general'),
             ('company_id', '=', self.env.company.id)], limit=1))

    monthly_amount = fields.Monetary(
        string='Monthly Amount', required=True, tracking=True,
        currency_field='currency_id')
    date_start = fields.Date(
        string='First Accrual Month', required=True, tracking=True,
        default=fields.Date.context_today,
        help='Accruals are generated monthly starting from this month. '
             'Each entry is dated on the last day of its month.')
    date_end = fields.Date(
        string='Last Accrual Month', tracking=True,
        help='Leave empty to accrue indefinitely. '
             'When set, no accrual entry is generated beyond this month.')
    months_total = fields.Integer(
        string='Total Months',
        compute='_compute_duration', store=True,
        help='Number of months from First to Last Accrual Month.')
    total_amount = fields.Monetary(
        string='Total Amount',
        compute='_compute_duration', store=True,
        currency_field='currency_id',
        help='Monthly Amount × Total Months.')
    auto_generate = fields.Boolean(
        string='Generate Automatically (Cron)', default=True, tracking=True,
        help='If enabled, the scheduled action posts the accrual entry of '
             'every elapsed month automatically while the record is Running.')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('billed', 'Billed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', required=True, copy=False,
        tracking=True)

    line_ids = fields.One2many(
        'coa.accrued.expense.line', 'accrual_id', string='Accrual Lines',
        copy=False)
    accrued_total = fields.Monetary(
        string='Total Accrued', compute='_compute_totals', store=True,
        currency_field='currency_id')
    months_count = fields.Integer(
        string='Months Accrued', compute='_compute_totals', store=True)

    bill_id = fields.Many2one(
        'account.move', string='Vendor Bill', copy=False, readonly=True,
        check_company=True,
        domain="[('move_type', '=', 'in_invoice')]")
    bill_state = fields.Selection(
        related='bill_id.state', string='Bill Status')
    move_count = fields.Integer(compute='_compute_move_count')

    # Bill data entered directly on the accrual screen when it arrives
    bill_reference = fields.Char(
        string='Bill Reference', copy=False,
        help='Vendor bill / invoice number as received from the vendor.')
    bill_date = fields.Date(string='Bill Date', copy=False)
    bill_amount = fields.Monetary(
        string='Bill Amount', copy=False, currency_field='currency_id',
        help='Total amount of the vendor bill (untaxed). If it differs from '
             'the total accrued, the difference is booked to the expense '
             'account automatically.')
    bill_attachment = fields.Binary(
        string='Bill Document', copy=False, attachment=True)
    bill_attachment_filename = fields.Char(copy=False)
    bill_difference = fields.Monetary(
        string='Difference vs Accrued', compute='_compute_bill_difference',
        currency_field='currency_id')

    _sql_constraints = [
        ('monthly_amount_positive',
         'CHECK(monthly_amount > 0)',
         'The monthly amount must be strictly positive.'),
    ]

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------
    @api.depends('date_start', 'date_end', 'monthly_amount')
    def _compute_duration(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                start = rec._month_key(rec.date_start)
                end   = rec._month_key(rec.date_end)
                delta = relativedelta(end + relativedelta(months=1), start)
                months = max(0, delta.months + delta.years * 12)
            else:
                months = 0
            rec.months_total = months
            rec.total_amount = months * rec.monthly_amount

    @api.depends('line_ids.amount', 'line_ids.move_id.state')
    def _compute_totals(self):
        for rec in self:
            posted = rec.line_ids.filtered(
                lambda l: l.move_id and l.move_id.state == 'posted')
            rec.accrued_total = sum(posted.mapped('amount'))
            rec.months_count = len(posted)

    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.line_ids.mapped('move_id'))

    @api.depends('bill_amount', 'accrued_total')
    def _compute_bill_difference(self):
        for rec in self:
            rec.bill_difference = (rec.bill_amount or 0.0) - rec.accrued_total

    @api.onchange('bill_reference', 'bill_date')
    def _onchange_bill_default_amount(self):
        for rec in self:
            if not rec.bill_amount and rec.accrued_total:
                rec.bill_amount = rec.accrued_total

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_end and rec.date_end < rec.date_start:
                raise ValidationError(_(
                    'The Last Accrual Month must be on or after '
                    'the First Accrual Month.'))

    @api.constrains('expense_account_id', 'accrual_account_id')
    def _check_accounts(self):
        for rec in self:
            if rec.expense_account_id == rec.accrual_account_id:
                raise ValidationError(_(
                    'The expense account and the accrual account must be '
                    'different.'))

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'coa.accrued.expense') or _('New')
        return super().create(vals_list)

    def unlink(self):
        if any(rec.state not in ('draft', 'cancel') for rec in self):
            raise UserError(_(
                'You can only delete draft or cancelled accruals. '
                'Cancel the record first.'))
        return super().unlink()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _month_key(date):
        return date.replace(day=1)

    @staticmethod
    def _month_end(month_start):
        return month_start + relativedelta(months=1, days=-1)

    def _get_pending_months(self, up_to=None):
        """Month-start dates from date_start whose month has fully elapsed
        (month end <= today) and that have no accrual line yet.
        When date_end is set, generation stops after that month."""
        self.ensure_one()
        up_to = up_to or fields.Date.context_today(self)
        # Respect the end date: never generate past the last accrual month
        if self.date_end:
            up_to = min(up_to, self._month_end(self._month_key(self.date_end)))
        existing = {self._month_key(l.date_month) for l in self.line_ids}
        pending = []
        month = self._month_key(self.date_start)
        while self._month_end(month) <= up_to:
            if month not in existing:
                pending.append(month)
            month += relativedelta(months=1)
        return pending

    def _create_accrual_entry(self, month_start):
        self.ensure_one()
        date = self._month_end(month_start)
        label = _('%(desc)s - Accrual %(month)s',
                  desc=self.description, month=month_start.strftime('%m/%Y'))
        move = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': self.journal_id.id,
            'company_id': self.company_id.id,
            'date': date,
            'ref': '%s / %s' % (self.name, month_start.strftime('%m/%Y')),
            'line_ids': [
                (0, 0, {
                    'name': label,
                    'account_id': self.expense_account_id.id,
                    'partner_id': self.partner_id.id,
                    'debit': self.monthly_amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': label,
                    'account_id': self.accrual_account_id.id,
                    'partner_id': self.partner_id.id,
                    'debit': 0.0,
                    'credit': self.monthly_amount,
                }),
            ],
        })
        move.action_post()
        self.env['coa.accrued.expense.line'].create({
            'accrual_id': self.id,
            'date_month': month_start,
            'amount': self.monthly_amount,
            'move_id': move.id,
        })
        return move

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                continue
            rec.state = 'running'
            rec.action_generate_due()
        return True

    def action_generate_due(self):
        """Generate & post accrual entries for all elapsed months."""
        for rec in self:
            if rec.state != 'running':
                raise UserError(_(
                    '%(name)s: accruals can only be generated while the '
                    'record is Running.', name=rec.name))
            for month in rec._get_pending_months():
                rec._create_accrual_entry(month)
        return True

    def action_generate_current_month(self):
        """Force-generate the current (not yet elapsed) month."""
        for rec in self:
            if rec.state != 'running':
                raise UserError(_(
                    '%(name)s: accruals can only be generated while the '
                    'record is Running.', name=rec.name))
            today = fields.Date.context_today(rec)
            month = rec._month_key(today)
            if month in {rec._month_key(l.date_month) for l in rec.line_ids}:
                raise UserError(_(
                    'The accrual entry of the current month already exists.'))
            if month < rec._month_key(rec.date_start):
                raise UserError(_(
                    'The current month is before the first accrual month.'))
            rec._create_accrual_entry(month)
        return True

    def action_register_bill(self):
        """Create the vendor bill from the data entered on this screen.

        The bill settles the accrual: Debit Accrued Expense / Credit Payable.
        If the bill amount differs from the total accrued, the difference is
        booked to the expense account on a second line.
        """
        self.ensure_one()
        if self.state != 'running':
            raise UserError(_('The record must be Running to register a bill.'))
        if not self.accrued_total:
            raise UserError(_(
                'Nothing has been accrued yet - generate the monthly '
                'entries first.'))
        if not self.bill_date:
            raise UserError(_('Please set the bill date.'))
        if not self.bill_amount:
            raise UserError(_('Please set the bill amount.'))

        lines = [(0, 0, {
            'name': _('%(desc)s - settlement of accrued expenses '
                      '(%(months)s month(s))',
                      desc=self.description, months=self.months_count),
            'account_id': self.accrual_account_id.id,
            'quantity': 1.0,
            'price_unit': self.accrued_total,
            'tax_ids': [(5, 0, 0)],
        })]
        diff = self.currency_id.round(self.bill_amount - self.accrued_total)
        if not self.currency_id.is_zero(diff):
            lines.append((0, 0, {
                'name': _('%(desc)s - difference between bill and accrued',
                          desc=self.description),
                'account_id': self.expense_account_id.id,
                'quantity': 1.0,
                'price_unit': diff,
                'tax_ids': [(5, 0, 0)],
            }))

        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'invoice_date': self.bill_date,
            'ref': self.bill_reference or self.name,
            'invoice_line_ids': lines,
        })
        if self.bill_attachment:
            self.env['ir.attachment'].create({
                'name': self.bill_attachment_filename or _('Vendor Bill'),
                'datas': self.bill_attachment,
                'res_model': 'account.move',
                'res_id': bill.id,
            })
        self.write({'bill_id': bill.id, 'state': 'billed'})
        self.message_post(body=_(
            'Vendor bill %(bill)s registered against the accrual account '
            '(amount: %(amount)s, difference booked to expense: %(diff)s).',
            bill=bill.display_name, amount=self.bill_amount, diff=diff))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': bill.id,
        }

    def action_link_bill(self):
        """Link an existing vendor bill instead of creating one."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Link Vendor Bill'),
            'res_model': 'coa.accrued.expense.link.bill',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_accrual_id': self.id},
        }

    def action_done(self):
        for rec in self:
            if rec.state != 'billed':
                raise UserError(_('Only billed records can be set to Done.'))
            rec.state = 'done'
        return True

    def action_cancel(self):
        for rec in self:
            posted = rec.line_ids.mapped('move_id').filtered(
                lambda m: m.state == 'posted')
            if posted:
                raise UserError(_(
                    'This accrual has posted journal entries. Reverse or '
                    'delete them first:\n%(moves)s',
                    moves=', '.join(posted.mapped('name'))))
            if rec.bill_id and rec.bill_id.state == 'posted':
                raise UserError(_(
                    'The linked vendor bill is posted. Reset it first.'))
            rec.state = 'cancel'
        return True

    def action_draft(self):
        for rec in self:
            if rec.state != 'cancel':
                raise UserError(_('Only cancelled records can be reset.'))
            rec.state = 'draft'
        return True

    def action_view_moves(self):
        self.ensure_one()
        moves = self.line_ids.mapped('move_id')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Accrual Entries'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', moves.ids)],
        }

    def action_view_bill(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.bill_id.id,
        }

    # ------------------------------------------------------------------
    # Cron
    # ------------------------------------------------------------------
    @api.model
    def _cron_generate_accruals(self):
        records = self.search([
            ('state', '=', 'running'),
            ('auto_generate', '=', True),
        ])
        for rec in records:
            try:
                for month in rec._get_pending_months():
                    rec._create_accrual_entry(month)
            except Exception as e:  # noqa: BLE001 - keep cron alive
                rec.message_post(body=_(
                    'Automatic accrual generation failed: %(error)s',
                    error=str(e)))
        return True


class CoaAccruedExpenseLine(models.Model):
    _name = 'coa.accrued.expense.line'
    _description = 'Accrued Expense Line'
    _order = 'date_month'

    accrual_id = fields.Many2one(
        'coa.accrued.expense', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one(related='accrual_id.company_id', store=True)
    currency_id = fields.Many2one(related='accrual_id.currency_id')
    date_month = fields.Date(string='Month', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    move_id = fields.Many2one(
        'account.move', string='Journal Entry', ondelete='restrict')
    move_state = fields.Selection(
        related='move_id.state', string='Entry Status')

    _sql_constraints = [
        ('month_unique', 'unique(accrual_id, date_month)',
         'An accrual entry already exists for this month.'),
    ]


class CoaAccruedExpenseLinkBill(models.TransientModel):
    _name = 'coa.accrued.expense.link.bill'
    _description = 'Link Existing Vendor Bill to Accrual'

    accrual_id = fields.Many2one(
        'coa.accrued.expense', required=True)
    bill_id = fields.Many2one(
        'account.move', string='Vendor Bill', required=True,
        domain="[('move_type', '=', 'in_invoice'), "
               "('partner_id', '=', partner_id)]")
    partner_id = fields.Many2one(related='accrual_id.partner_id')

    def action_link(self):
        self.ensure_one()
        accrual = self.accrual_id
        accrual_account = accrual.accrual_account_id
        if accrual_account not in self.bill_id.invoice_line_ids.mapped(
                'account_id'):
            accrual.message_post(body=_(
                'Warning: the linked bill %(bill)s has no line on the '
                'accrual account %(account)s. Make sure the bill settles '
                'the accrual, otherwise the expense will be duplicated.',
                bill=self.bill_id.display_name,
                account=accrual_account.display_name))
        accrual.write({'bill_id': self.bill_id.id, 'state': 'billed'})
        return {'type': 'ir.actions.act_window_close'}
