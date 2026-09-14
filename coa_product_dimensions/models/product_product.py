# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    square_meter_stock = fields.Float(
        string="Square Meter",
        compute="_compute_stock_dimensions",
        digits=(16, 4),
    )
    cubic_meter_stock = fields.Float(
        string="Cubic Meter",
        compute="_compute_stock_dimensions",
        digits=(16, 6),
    )
    total_liters = fields.Float(
        string="Total Liters / إجمالي اللترات",
        compute="_compute_stock_dimensions",
        digits=(16, 4),
    )

    @api.depends(
        "qty_available",
        "product_tmpl_id.square_meter",
        "product_tmpl_id.cubic_meter",
        "product_tmpl_id.liter_capacity",
    )
    def _compute_stock_dimensions(self):
        for product in self:
            qty = product.qty_available or 0.0
            tmpl = product.product_tmpl_id
            product.square_meter_stock = qty * (tmpl.square_meter or 0.0)
            product.cubic_meter_stock = qty * (tmpl.cubic_meter or 0.0)
            product.total_liters = qty * (tmpl.liter_capacity or 0.0)