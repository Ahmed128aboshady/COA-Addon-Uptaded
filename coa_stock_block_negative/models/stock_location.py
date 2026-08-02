# -*- coding: utf-8 -*-
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    allow_negative_stock = fields.Boolean(
        string="Allow Negative Stock",
        default=False,
        groups="base.group_system",
        help="If checked, products stored in this location are allowed to "
             "have negative on-hand quantities.",
    )
