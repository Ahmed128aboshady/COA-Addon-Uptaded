# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_negative_stock = fields.Boolean(
        string="Allow Negative Stock",
        default=False,
        groups="base.group_system",
        help="If checked, stock operations on this product are allowed to "
             "drive its on-hand quantity below zero. Leave unchecked to "
             "block any operation that would create negative stock.",
    )
