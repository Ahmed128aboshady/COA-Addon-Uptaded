# -*- coding: utf-8 -*-
""" Outgoing Cheque """
from odoo import api, fields, models, _


class OutgoingCheque(models.Model):
    """ Outgoing Cheque """
    _name = 'outgoing.cheque'
    _description = 'Outgoing Cheque'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('cheque_settlement', 'Cheque Settlement'),('cancelled', 'Cancelled')],
                             string="Status", default='draft')
    name = fields.Char(default="New")
    description = fields.Text()
    partner_id = fields.Many2one('res.partner', string="Vendor")
    date = fields.Date(default=fields.Date.today())
    amount = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    beneficiary = fields.Char()
    journal_id = fields.Many2one('account.journal')
    notes_payable_account_id = fields.Many2one('account.account')
    bank_account_id = fields.Many2one('account.account')
    count_move_line = fields.Integer(compute='_compute_count_move_line',
                                     store=True)
    account_move_line_ids = fields.One2many('account.move.line',
                                            'outgoing_cheque_id')
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
            "domain": [('outgoing_cheque_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Account Move Line"),
            'view_mode': 'list,form',
        }
        return result

    def confirm(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_action').sudo().read()[
            0]
        action['context'] = {'default_transient_state': 'outgoing_confirm'}
        action['views'] = [(self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_form').id, 'form')]
        return action

    def cheque_settlement(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_action').sudo().read()[
            0]
        action['context'] = {'default_transient_state': 'cheque_settlement'}
        action['views'] = [(self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_form').id, 'form')]
        return action

    def cancel(self):
        """ Send To Bank """
        action = self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_action').sudo().read()[
            0]
        action['context'] = {'default_transient_state': 'cheque_settlement'}
        action['views'] = [(self.env.ref(
            'arabian_cheque_management.check_accounts_cheque_form').id, 'form')]
        return action
    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'outgoing.cheque') or '/'
        return super(OutgoingCheque, self).create(vals)
