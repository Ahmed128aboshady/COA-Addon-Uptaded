# -*- coding: utf-8 -*-
""" Advance Payment Guarantee """
from odoo import api, fields, models, _


class LgAdvancePaymentGuarantee(models.Model):
    """ Lg Advance Payment Guarantee """
    _name = 'lg.advance.payment.guarantee'
    _description = 'Lg Advance Payment Guarantee'

    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancellation', 'Cancellation')],
        string="Status", default='draft')
    name = fields.Char(default='New')
    tender_no = fields.Char()
    partner_id = fields.Many2one('res.partner',string="Customer")
    guarantee_amount  = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    date = fields.Date()
    expiry_date = fields.Date()
    beneficiary_name = fields.Char()
    beneficiary_address = fields.Char()
    guarantee_details = fields.Html()
    description = fields.Text()
    journal_id = fields.Many2one('account.journal')
    advance_payment_guarantee_account_id = fields.Many2one('account.account',string="Advance Payment Guarantee Account")
    bank_account_id = fields.Many2one('account.account')
    count_move_line = fields.Integer(compute='_compute_count_move_line',
                                     store=True)
    account_move_line_ids = fields.One2many('account.move.line',
                                            'lg_advance_payment_guarantee_id')

    @api.depends('account_move_line_ids')
    def _compute_count_move_line(self):
        """ Compute count_move_line  value """
        for rec in self:
            rec.count_move_line = len(rec.account_move_line_ids.ids)

    def action_view_all_account_move_line(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.move.line",
            "domain": [('lg_advance_payment_guarantee_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Account Move Line"),
            'view_mode': 'list,form',
        }
        return result


    def confirm(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_letters_of_guarantee.check_lg_accounts_action').sudo().read()[
            0]
        action['context'] = {'default_lg_type': 'advance_payment'}
        action['views'] = [(self.env.ref(
            'arabian_letters_of_guarantee.check_lg_accounts_form').id, 'form')]
        return action

    def cancellation(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_letters_of_guarantee.check_lg_accounts_action').sudo().read()[
            0]
        action['context'] = {'default_lg_type': 'advance_payment_cancellation'}
        action['views'] = [(self.env.ref(
            'arabian_letters_of_guarantee.check_lg_accounts_form').id, 'form')]
        return action

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('lg.advance.payment.guarantee') or '/'
        return super(LgAdvancePaymentGuarantee, self).create(vals)
