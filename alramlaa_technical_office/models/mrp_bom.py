# -*- coding: utf-8 -*-
from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    is_estimated = fields.Boolean(
        string='Estimated BOM (Technical Office)',
        default=False,
        help='This BOM was created by the Technical Office as a preliminary / '
             'estimated BOM. It has not yet been verified by engineering.',
        tracking=True,
    )
