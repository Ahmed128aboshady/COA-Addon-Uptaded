# -*- coding: utf-8 -*-
""" Incoming Cheque """
from odoo import api, fields, models, _


class IncomingCheque(models.Model):
    """ Incoming Cheque """
    _name = 'incoming.cheque'
    _description = 'Incoming Cheque'

    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('deposit', 'Deposit'),
         ('cancelled', 'Cancelled')],
        string="Status", default='draft')
    name = fields.Char(default="New")
    description = fields.Text()
    partner_id = fields.Many2one('res.partner', string="Customer")
    date = fields.Date(default=fields.Date.today())
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    beneficiary = fields.Char()
    journal_id = fields.Many2one('account.journal')
    count_move_line = fields.Integer(compute='_compute_count_move_line',
                                     store=True)
    account_move_line_ids = fields.One2many('account.move.line',
                                            'incoming_cheque_id')
    notes_receivable_account_id = fields.Many2one('account.account')
    incoming_bank_account_id = fields.Many2one('account.account',string="Bank Account")
    cheque_number = fields.Char()
    
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
            "domain": [('incoming_cheque_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Account Move Line"),
            'view_mode': 'list,form',
        }
        return result

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'incoming.cheque') or '/'
        return super(IncomingCheque, self).create(vals)

    def confirm(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_action').sudo().read()[
            0]
        action['context'] = {'default_transient_state': 'incoming_confirm'}
        action['views'] = [(self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_form').id, 'form')]
        return action

    def deposit(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_action').sudo().read()[
            0]
        action['context'] = {'default_transient_state': 'incoming_deposit'}
        action['views'] = [(self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_form').id, 'form')]
        return action

    def cancel(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_action').sudo().read()[
            0]
        action['context'] = {'default_transient_state': 'incoming_cancel'}
        action['views'] = [(self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_form').id, 'form')]
        return action
