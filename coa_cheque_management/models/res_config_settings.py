# -*- coding: utf-8 -*-
""" Res Config Settings """
from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    """ inherit Res Config Settings """
    _inherit = 'res.config.settings'

    outgoing_journal_id = fields.Many2one('account.journal',
                                          related='company_id.outgoing_journal_id',
                                          readonly=0)
    incoming_journal_id = fields.Many2one('account.journal',
                                          related='company_id.incoming_journal_id',
                                          readonly=0)
    notes_payable_account_id = fields.Many2one('account.account',related='company_id.notes_payable_account_id',
                                               readonly=0,string="Note Payable Account")
    notes_receivable_account_id = fields.Many2one('account.account',related='company_id.notes_receivable_account_id',
                                                  readonly=0,string="Notes Receivable Account")
    outgoing_bank_account_id = fields.Many2one('account.account',related='company_id.outgoing_bank_account_id',
    readonly=0,string="Outgoing Bank Account")
    incoming_bank_account_id = fields.Many2one('account.account',related='company_id.incoming_bank_account_id',
                                               readonly=0,string="Incoming Bank Account")


class ResCompany(models.Model):
    """ inherit Res Company """
    _inherit = 'res.company'

    outgoing_journal_id = fields.Many2one('account.journal')
    incoming_journal_id = fields.Many2one('account.journal')
    notes_payable_account_id = fields.Many2one('account.account')
    notes_receivable_account_id = fields.Many2one('account.account')
    outgoing_bank_account_id = fields.Many2one('account.account')
    incoming_bank_account_id = fields.Many2one('account.account')
