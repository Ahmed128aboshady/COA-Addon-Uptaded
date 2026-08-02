# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # editable dimensions on PO line
    dimension_length = fields.Float(
        string="Length (mm)",
        store=True,
    )
    dimension_width = fields.Float(
        string="Width (mm)",
        store=True,
    )
    dimension_thickness = fields.Float(
        string="Thickness (mm)",
        store=True,
    )

    # totals on PO line
    square_meter_total = fields.Float(
        string="Total Square Meter",
        compute="_compute_dimension_totals",
        store=True,
        digits=(16, 6),
    )
    cubic_meter_total = fields.Float(
        string="Total Cubic Meter",
        compute="_compute_dimension_totals",
        store=True,
        digits=(16, 9),
    )

    @api.onchange("product_id")
    def _onchange_product_dimensions(self):
        for line in self:
            if line.product_id:
                tmpl = line.product_id.product_tmpl_id
                line.dimension_length = tmpl.dimension_length or 0.0
                line.dimension_width = tmpl.dimension_width or 0.0
                line.dimension_thickness = tmpl.dimension_thickness or 0.0

    @api.depends(
        "product_qty",
        "dimension_length",
        "dimension_width",
        "dimension_thickness",
    )
    def _compute_dimension_totals(self):
        for line in self:
            qty = line.product_qty or 0.0
            length = line.dimension_length or 0.0
            width = line.dimension_width or 0.0
            thickness = line.dimension_thickness or 0.0

            line.square_meter_total = ((length * width) / 1000000.0) * qty if length and width and qty else 0.0
            line.cubic_meter_total = ((length * width * thickness) / 1000000000.0) * qty if length and width and thickness and qty else 0.0