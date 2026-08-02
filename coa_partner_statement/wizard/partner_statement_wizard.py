from odoo import models, fields, api
from odoo.exceptions import UserError


class PartnerStatementWizard(models.TransientModel):
    _name = 'partner.statement.wizard'
    _description = 'Partner Statement Report Wizard'

    date_from = fields.Date(
        string='From',
        required=True,
        default=lambda self: fields.Date.today().replace(month=1, day=1),
    )
    date_to = fields.Date(
        string='To',
        required=True,
        default=fields.Date.today,
    )
    all_accounts = fields.Boolean(
        string='All Accounts for Partner',
        default=False,
        help='If checked, includes all accounts for the selected partner.',
    )
    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Account',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
    )

    @api.onchange('all_accounts')
    def _onchange_all_accounts(self):
        if self.all_accounts:
            self.account_id = False

    def action_print_report(self):
        if not self.all_accounts and not self.account_id:
            raise UserError('Please select an account or check "All Accounts for Partner".')

        data = {
            'date_from':    str(self.date_from),
            'date_to':      str(self.date_to),
            'all_accounts': self.all_accounts,
            'account_id':   self.account_id.id if self.account_id else False,
            'account_name': self.account_id.display_name if self.account_id else '',
            'partner_id':   self.partner_id.id,
            'partner_name': self.partner_id.display_name,
        }

        return self.env.ref(
            'partner_statement.action_partner_statement_report'
        ).report_action(self, data=data)
