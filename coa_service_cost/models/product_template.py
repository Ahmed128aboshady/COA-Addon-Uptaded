# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    coa_service_intermediate_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Intermediate Account',
        company_dependent=True,
        check_company=True,
        help=(
            'SERVICE PRODUCTS ONLY.\n\n'
            'When a vendor bill containing this product is posted, '
            'the cost line is redirected to this account instead of '
            'the standard expense account.\n\n'
            'Acts as a "cost-in-transit" buffer until the service is '
            'invoiced to the customer.'
        ),
    )

    coa_service_cogs_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Cost of Sales Account',
        company_dependent=True,
        check_company=True,
        help=(
            'SERVICE PRODUCTS ONLY.\n\n'
            'When a customer invoice containing this product is posted, '
            'a cost journal entry is created automatically:\n'
            '  DR  Cost of Sales Account  (this field)\n'
            '  CR  Intermediate Account   (field above)\n\n'
            'Amount = product Standard Price × invoiced quantity.'
        ),
    )
