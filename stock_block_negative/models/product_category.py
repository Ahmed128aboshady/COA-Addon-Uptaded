# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    allow_negative_stock = fields.Boolean(
        string="Allow Negative Stock",
        default=False,
        groups="base.group_system",
        help="If checked, all products in this category are allowed to have "
             "negative on-hand quantities.",
    )
