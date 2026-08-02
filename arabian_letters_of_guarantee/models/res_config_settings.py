# -*- coding: utf-8 -*-
""" Res Config Settings """
from odoo import api, fields, models, _
from odoo.tools import SQL

class ResConfigSettings(models.TransientModel):
    """ inherit Res Config Settings """
    _inherit = 'res.config.settings'

    journal_id = fields.Many2one('account.journal',related='company_id.journal_id',
    readonly=0,string="Journal")
    bid_bond_account_id = fields.Many2one('account.account',related='company_id.bid_bond_account_id',
                                          readonly=0,string="Bid Bond Account")
    performance_bond_account_id = fields.Many2one('account.account',related='company_id.bid_bond_account_id',
                                          readonly=0,string="Performance Bond Account")
    advance_payment_guarantee_account_id = fields.Many2one('account.account',related='company_id.bid_bond_account_id',
                                                  readonly=0,string="Advance Payment Guarantee Account")
    maintenance_bond_account_id = fields.Many2one('account.account',related='company_id.bid_bond_account_id',
                                                           readonly=0,string="Maintenance Bond Account")
class ResCompany(models.Model):
    """ inherit Res Company """
    _inherit = 'res.company'

    journal_id = fields.Many2one('account.journal')
    bid_bond_account_id = fields.Many2one('account.account')
    performance_bond_account_id = fields.Many2one('account.account')
    advance_payment_guarantee_account_id = fields.Many2one('account.account',string="Advance Payment Guarantee Account")
    maintenance_bond_account_id = fields.Many2one('account.account',string="Maintenance Bond Account")

class AccountAsset(models.Model):
    """ inherit Account Asset """
    _inherit = 'account.asset'

    def _query_analytic_accounts(self, table=False):
        return SQL(
            r"""regexp_split_to_array(jsonb_path_query_array(%s.analytic_distribution, '$.keyvalue()."key"')::text, '\D+')""",
            SQL(table or self._table),
        )