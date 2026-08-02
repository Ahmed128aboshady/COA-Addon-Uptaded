# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

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

    square_meter = fields.Float(
        string="Square Meter",
        compute="_compute_dimensions",
        store=True,
        digits=(16, 4),
    )

    cubic_meter = fields.Float(
        string="Cubic Meter",
        compute="_compute_dimensions",
        store=True,
        digits=(16, 6),
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = vals.get("product_id")
            if product_id:
                product = self.env["product.product"].browse(product_id)
                tmpl = product.product_tmpl_id

                if not vals.get("dimension_length"):
                    vals["dimension_length"] = tmpl.dimension_length or 0.0
                if not vals.get("dimension_width"):
                    vals["dimension_width"] = tmpl.dimension_width or 0.0
                if not vals.get("dimension_thickness"):
                    vals["dimension_thickness"] = tmpl.dimension_thickness or 0.0

        return super().create(vals_list)

    @api.onchange("product_id")
    def _onchange_product_id_set_dimensions(self):
        for move in self:
            tmpl = move.product_id.product_tmpl_id
            move.dimension_length = tmpl.dimension_length or 0.0
            move.dimension_width = tmpl.dimension_width or 0.0
            move.dimension_thickness = tmpl.dimension_thickness or 0.0

    @api.depends(
        "product_uom_qty",
        "dimension_length",
        "dimension_width",
        "dimension_thickness",
    )
    def _compute_dimensions(self):
        for move in self:
            qty = move.product_uom_qty or 0.0
            length = move.dimension_length or 0.0
            width = move.dimension_width or 0.0
            thickness = move.dimension_thickness or 0.0

            move.square_meter = (length * width * qty) / 1000000.0 if length and width and qty else 0.0
            move.cubic_meter = (length * width * thickness * qty) / 1000000000.0 if length and width and thickness and qty else 0.0