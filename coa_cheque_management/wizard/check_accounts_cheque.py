# -*- coding: utf-8 -*-
""" Check Accounts Cheque """
from odoo import api, fields, models, _


class CheckAccountsCheque(models.TransientModel):
    """ Check Accounts Cheque """
    _name = 'check.accounts.cheque'
    _description = 'Check Accounts Cheque'

    def _get_outgoing_journal(self):
        """ Get Incoming Journal """
        return self.env.company.outgoing_journal_id.id

    def _get_incoming_journal(self):
        """ Get Incoming Journal """
        return self.env.company.incoming_journal_id.id

    def _get_notes_payable_account(self):
        """ Get Incoming Journal """
        return self.env.company.notes_payable_account_id.id

    def _get_notes_receivable_account(self):
        """ Get Incoming Journal """
        return self.env.company.notes_receivable_account_id.id

    def _get_outgoing_bank_account(self):
        """ Get Incoming Journal """
        return self.env.company.outgoing_bank_account_id.id

    def _get_incoming_bank_account(self):
        """ Get Incoming Journal """
        return self.env.company.incoming_bank_account_id.id

    transient_state = fields.Selection(
        [('incoming_confirm', 'Incoming Confirm'),
         ('outgoing_confirm', 'Outgoing Confirm'),
         ('incoming_deposit', 'Incoming Deposit'),
         ('outgoing_deposit', 'Outgoing Deposit'),
         ('cheque_settlement', 'Cheque Settlement'),
         ('incoming_cancel', 'Incoming Cancel'),
         ('outgoing_cancel', 'Outgoing Cancel')])
    outgoing_journal_id = fields.Many2one('account.journal',
                                          default=_get_outgoing_journal)
    incoming_journal_id = fields.Many2one('account.journal',
                                          default=_get_incoming_journal)
    notes_payable_account_id = fields.Many2one('account.account',
                                               default=_get_notes_payable_account)
    notes_receivable_account_id = fields.Many2one('account.account',
                                                  default=_get_notes_receivable_account)
    outgoing_bank_account_id = fields.Many2one('account.account',
                                               default=_get_outgoing_bank_account,string="Bank Account")
    incoming_bank_account_id = fields.Many2one('account.account',
                                               default=_get_incoming_bank_account,
                                               string="Bank Account")
    date = fields.Date(default=fields.Date.today())

    def incoming_confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        incoming_cheque = self.env['incoming.cheque'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.notes_receivable_account_id.id,
                           'credit': 0.0,
                           'debit': incoming_cheque.amount,
                           'name': "Confirm/Receive the cheque",
                           'incoming_cheque_id': incoming_cheque.id}))
            items.append((0, 0, {
                'account_id': incoming_cheque.partner_id.property_account_receivable_id.id,
                'debit': 0.0, 'credit': incoming_cheque.amount,
                'name': "Confirm/Receive the cheque",
                'incoming_cheque_id': incoming_cheque.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.incoming_journal_id.id, 'line_ids': items,
                 'incoming_cheque_id': incoming_cheque.id,
                 'move_type': 'entry'})
            account_move.action_post()
            incoming_cheque.journal_id = rec.incoming_journal_id.id
            incoming_cheque.notes_receivable_account_id = rec.notes_receivable_account_id.id
            incoming_cheque.state = 'confirmed'

    def incoming_deposit(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        incoming_cheque = self.env['incoming.cheque'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {
                              'account_id': incoming_cheque.notes_receivable_account_id.id,
                              'debit': 0.0,
                              'credit': incoming_cheque.amount,
                              'name': "Deposit Cheque",
                              'incoming_cheque_id': incoming_cheque.id}))
            items.append((0, 0, {
                'account_id': rec.incoming_bank_account_id.id,
                'credit': 0.0, 'debit': incoming_cheque.amount,
                'name': "Deposit Cheque",
                'incoming_cheque_id': incoming_cheque.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': incoming_cheque.journal_id.id, 'line_ids': items,
                 'incoming_cheque_id': incoming_cheque.id,
                 'move_type': 'entry'})
            account_move.action_post()
            incoming_cheque.incoming_bank_account_id = rec.incoming_bank_account_id.id
            incoming_cheque.state = 'deposit'

    def incoming_cancel(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        incoming_cheque = self.env['incoming.cheque'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': rec.notes_receivable_account_id.id,
                           'debit': 0.0,
                           'credit': incoming_cheque.amount,
                           'name': "Cheque Cancelled",
                           'incoming_cheque_id': incoming_cheque.id}))
            items.append((0, 0, {
                'account_id': incoming_cheque.partner_id.property_account_receivable_id.id,
                'credit': 0.0, 'debit': incoming_cheque.amount,
                'name': "Cheque Cancelled",
                'incoming_cheque_id': incoming_cheque.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.incoming_journal_id.id, 'line_ids': items,
                 'incoming_cheque_id': incoming_cheque.id,
                 'move_type': 'entry'})
            account_move.action_post()
            incoming_cheque.state = 'cancelled'


    def outgoing_confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        outgoing_cheque = self.env['outgoing.cheque'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': outgoing_cheque.partner_id.property_account_payable_id.id,
                           'credit': 0.0,
                           'debit': outgoing_cheque.amount,
                           'name': "Confirm/Issuing a Cheque",
                           'outgoing_cheque_id': outgoing_cheque.id}))
            items.append((0, 0, {
                'account_id': rec.notes_payable_account_id.id,
                'debit': 0.0, 'credit': outgoing_cheque.amount,
                'name': "Confirm/Issuing a Cheque",
                'outgoing_cheque_id': outgoing_cheque.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': rec.outgoing_journal_id.id, 'line_ids': items,
                 'outgoing_cheque_id': outgoing_cheque.id,
                 'move_type': 'entry'})
            account_move.action_post()
            outgoing_cheque.journal_id = rec.outgoing_journal_id.id
            outgoing_cheque.notes_payable_account_id = rec.notes_payable_account_id.id
            outgoing_cheque.state = 'confirmed'

    def outgoing_cheque_settlement(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        outgoing_cheque = self.env['outgoing.cheque'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': outgoing_cheque.notes_payable_account_id.id,
                           'credit': 0.0,
                           'debit': outgoing_cheque.amount,
                           'name': "Cheque Settlement",
                           'outgoing_cheque_id': outgoing_cheque.id}))
            items.append((0, 0, {
                'account_id': rec.outgoing_bank_account_id.id,
                'debit': 0.0, 'credit': outgoing_cheque.amount,
                'name': "Cheque Settlement",
                'outgoing_cheque_id': outgoing_cheque.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': outgoing_cheque.journal_id.id, 'line_ids': items,
                 'outgoing_cheque_id': outgoing_cheque.id,
                 'move_type': 'entry'})
            account_move.action_post()
            outgoing_cheque.bank_account_id=rec.outgoing_bank_account_id.id
            outgoing_cheque.state = 'cheque_settlement'

    def outgoing_cancel(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        outgoing_cheque = self.env['outgoing.cheque'].browse(
            active_id)
        items = []
        for rec in self:
            items.append((0, 0,
                          {'account_id': outgoing_cheque.partner_id.property_account_payable_id.id,
                           'debit': 0.0,
                           'credit': outgoing_cheque.amount,
                           'name': "Confirm/Issuing a Cheque",
                           'outgoing_cheque_id': outgoing_cheque.id}))
            items.append((0, 0, {
                'account_id': outgoing_cheque.notes_payable_account_id.id,
                'credit': 0.0, 'debit': outgoing_cheque.amount,
                'name': "Confirm/Issuing a Cheque",
                'outgoing_cheque_id': outgoing_cheque.id}))
            account_move = self.env['account.move'].sudo().create(
                {'journal_id': outgoing_cheque.incoming_journal_id.id, 'line_ids': items,
                 'outgoing_cheque_id': outgoing_cheque.id,
                 'move_type': 'entry'})
            account_move.action_post()
            outgoing_cheque.state = 'cancelled'