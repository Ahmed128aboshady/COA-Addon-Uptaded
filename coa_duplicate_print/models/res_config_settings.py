# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    coa_duplicate_print_mode = fields.Selection([
        ('none', 'Disabled'),
        ('stock', 'Inventory only'),
        ('sale', 'Sales only'),
        ('both', 'Inventory and Sales'),
    ], string='Duplicate Print Watermark', default='both', required=True,
        help='Show a "DUPLICATE" watermark when a document is printed more '
             'than once.')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    coa_duplicate_print_mode = fields.Selection(
        related='company_id.coa_duplicate_print_mode', readonly=False,
        string='Duplicate Print Watermark')
