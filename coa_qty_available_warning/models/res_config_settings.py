# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    coa_qty_warning_enabled = fields.Boolean(
        string='Quantity Available Warning', default=True,
        help='Show a non-blocking warning when the requested quantity '
             'exceeds the company-wide Free To Use quantity.')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    coa_qty_warning_enabled = fields.Boolean(
        related='company_id.coa_qty_warning_enabled', readonly=False,
        string='Quantity Available Warning')
