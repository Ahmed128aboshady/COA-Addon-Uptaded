# -*- coding: utf-8 -*-
""" Check Lg Accounts """
from odoo import api, fields, models, _


class CheckLgAccounts(models.TransientModel):
    """ Check Lg Accounts """
    _name = 'check.lg.accounts'
    _description = 'Check Lg Accounts'

    def _get_journal(self):
        """ Get Incoming Journal """
        return self.env.company.journal_id.id

    def _get_bid_bond_account_id(self):
        """ Get Incoming Journal """
        return self.env.company.bid_bond_account_id.id

    def _get_performance_bond_account_id(self):
        """ Get Incoming Journal """
        return self.env.company.performance_bond_account_id.id
    def _get_payment_guarantee_account_id(self):
        """ Get Incoming Journal """
        return self.env.company.advance_payment_guarantee_account_id.id

    journal_id = fields.Many2one('account.journal', default=_get_journal)
    bid_bond_account_id = fields.Many2one('account.account',
                                          default=_get_bid_bond_account_id)
    performance_bond_account_id = fields.Many2one('account.account',
                                                  default=_get_performance_bond_account_id)
    advance_payment_guarantee_account_id = fields.Many2one('account.account',string="Advance Payment Guarantee Account")
    maintenance_bond_account_id = fields.Many2one('account.account',string="Maintenance Bond Account")

    bank_account_id = fields.Many2one('account.account')
    date = fields.Date(default=fields.Date.today())
    lg_type = fields.Selection(
        [('bid_bond', 'Bid Bond'), ('bid_cancellation', ' Bid Cancellation'),
         ('performance_bond', 'Performance Bond'),
         ('cancellation_performance', 'Cancellation Performance'),
         ('advance_payment', 'Advance Payment'),
         ('advance_payment_cancellation', 'Advance Payment Cancellation'),
         ('maintenance_bond', 'Maintenance Bond'),
         ('maintenance_bond_cancellation', 'Maintenance Bond Cancellation')
         ])

    def bid_bond_confirm(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        bid_bond = self.env['lg.bid.bond'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.bid_bond_account_id.id,
                           'credit': 0.0,
                           'debit': bid_bond.guarantee_amount,
                           'name': "Issuance of a letter of guarantee for the tender",
                           'lg_bid_bond_id': bid_bond.id}))
            items.append((0, 0, {
                'account_id': rec.bank_account_id.id,
                'debit': 0.0, 'credit': bid_bond.guarantee_amount,
                'name': "Issuance of a letter of guarantee for the tender",
                'lg_bid_bond_id': bid_bond.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_bid_bond_id': bid_bond.id,
                 'move_type': 'entry'})
            account_move.action_post()
            bid_bond.journal_id = rec.journal_id.id
            bid_bond.bid_bond_account_id = rec.bid_bond_account_id.id
            bid_bond.bank_account_id = rec.bank_account_id.id
            bid_bond.date = rec.date
            bid_bond.state = 'confirmed'

    def bid_bond_Cancellation(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        bid_bond = self.env['lg.bid.bond'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': bid_bond.bid_bond_account_id.id,
                           'debit': 0.0,
                           'credit': bid_bond.guarantee_amount,
                           'name': "Cancellation letter of guarantee and get the money back.",
                           'lg_bid_bond_id': bid_bond.id}))
            items.append((0, 0, {
                'account_id': bid_bond.bank_account_id.id,
                'credit': 0.0, 'debit': bid_bond.guarantee_amount,
                'name': "Cancellation letter of guarantee and get the money back.",
                'lg_bid_bond_id': bid_bond.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_bid_bond_id': bid_bond.id,
                 'move_type': 'entry'})
            account_move.action_post()
            bid_bond.expiry_date = rec.date
            bid_bond.state = 'cancellation'

    def performance_bond_confirm(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        performance_bond = self.env['lg.performance.bond'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.performance_bond_account_id.id,
                           'credit': 0.0,
                           'debit': performance_bond.guarantee_amount,
                           'name': "Confirm/Issuance of letter of guarantee",
                           'lg_bid_bond_id': performance_bond.id}))
            items.append((0, 0, {
                'account_id': rec.bank_account_id.id,
                'debit': 0.0, 'credit': performance_bond.guarantee_amount,
                'name': "Confirm/Issuance of letter of guarantee",
                'lg_performance_bond_id': performance_bond.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_performance_bond_id': performance_bond.id,
                 'move_type': 'entry'})
            account_move.action_post()
            performance_bond.journal_id = rec.journal_id.id
            performance_bond.performance_bond_account_id = rec.performance_bond_account_id.id
            performance_bond.bank_account_id = rec.bank_account_id.id
            performance_bond.date = rec.date
            performance_bond.state = 'confirmed'

    def performance_bond_Cancellation(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        performance_bond = self.env['lg.performance.bond'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.bid_bond_account_id.id,
                           'debit': 0.0,
                           'credit': performance_bond.guarantee_amount,
                           'name': "Cancellation letter of guarantee and get the money back.",
                           'lg_bid_bond_id': performance_bond.id}))
            items.append((0, 0, {
                'account_id': performance_bond.bank_account_id.id,
                'credit': 0.0, 'debit': performance_bond.guarantee_amount,
                'name': "Cancellation letter of guarantee and get the money back.",
                'lg_performance_bond_id': performance_bond.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_performance_bond_id': performance_bond.id,
                 'move_type': 'entry'})
            account_move.action_post()
            performance_bond.expiry_date = rec.date
            performance_bond.state = 'cancellation'

    def advance_payment_confirm(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        advance_payment = self.env['lg.advance.payment.guarantee'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.advance_payment_guarantee_account_id.id,
                           'credit': 0.0,
                           'debit': advance_payment.guarantee_amount,
                           'name': "Confirm/Issuance of letter of guarantee",
                           'lg_advance_payment_guarantee_id': advance_payment.id}))
            items.append((0, 0, {
                'account_id': rec.bank_account_id.id,
                'debit': 0.0, 'credit': advance_payment.guarantee_amount,
                'name': "Confirm/Issuance of letter of guarantee",
                'lg_advance_payment_guarantee_id': advance_payment.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_advance_payment_guarantee_id': advance_payment.id,
                 'move_type': 'entry'})
            account_move.action_post()
            advance_payment.journal_id = rec.journal_id.id
            advance_payment.advance_payment_guarantee_account_id = rec.advance_payment_guarantee_account_id.id
            advance_payment.bank_account_id = rec.bank_account_id.id
            advance_payment.date = rec.date
            advance_payment.state = 'confirmed'

    def advance_payment_Cancellation(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        advance_payment = self.env['lg.advance.payment.guarantee'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': advance_payment.advance_payment_guarantee_account_id.id,
                           'debit': 0.0,
                           'credit': advance_payment.guarantee_amount,
                           'name': "Cancellation letter of guarantee and get the money back.",
                           'lg_advance_payment_guarantee_id': advance_payment.id}))
            items.append((0, 0, {
                'account_id': advance_payment.bank_account_id.id,
                'credit': 0.0, 'debit': advance_payment.guarantee_amount,
                'name': "Cancellation letter of guarantee and get the money back.",
                'lg_advance_payment_guarantee_id': advance_payment.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_advance_payment_guarantee_id': advance_payment.id,
                 'move_type': 'entry'})
            account_move.action_post()
            advance_payment.expiry_date = rec.date
            advance_payment.state = 'cancellation'

    def maintenance_bond_confirm(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        maintenance_bond = self.env['lg.maintenance.bond'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.maintenance_bond_account_id.id,
                           'credit': 0.0,
                           'debit': maintenance_bond.guarantee_amount,
                           'name': "Confirm/Issuance of letter of guarantee",
                           'lg_maintenance_bond_id': maintenance_bond.id}))
            items.append((0, 0, {
                'account_id': rec.bank_account_id.id,
                'debit': 0.0, 'credit': maintenance_bond.guarantee_amount,
                'name': "Confirm/Issuance of letter of guarantee",
                'lg_maintenance_bond_id': maintenance_bond.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_maintenance_bond_id': maintenance_bond.id,
                 'move_type': 'entry'})
            account_move.action_post()
            maintenance_bond.journal_id = rec.journal_id.id
            maintenance_bond.maintenance_bond_account_id = rec.maintenance_bond_account_id.id
            maintenance_bond.bank_account_id = rec.bank_account_id.id
            maintenance_bond.date = rec.date
            maintenance_bond.state = 'confirmed'

    def maintenance_bond_Cancellation(self):
        """ Bid Bond Confirm """
        active_id = self._context.get('active_id')
        maintenance_bond = self.env['lg.maintenance.bond'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': maintenance_bond.maintenance_bond_account_id.id,
                           'debit': 0.0,
                           'credit': maintenance_bond.guarantee_amount,
                           'name': "Cancellation letter of guarantee and get the money back.",
                           'lg_maintenance_bond_id': maintenance_bond.id}))
            items.append((0, 0, {
                'account_id': maintenance_bond.bank_account_id.id,
                'credit': 0.0, 'debit': maintenance_bond.guarantee_amount,
                'name': "Cancellation letter of guarantee and get the money back.",
                'lg_maintenance_bond_id': maintenance_bond.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.journal_id.id, 'line_ids': items,
                 'lg_maintenance_bond_id': maintenance_bond.id,
                 'move_type': 'entry'})
            account_move.action_post()
            maintenance_bond.expiry_date = rec.date
            maintenance_bond.state = 'cancellation'