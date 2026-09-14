# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    total_liters = fields.Float(
        string='Total Liters / إجمالي اللترات',
        compute='_compute_total_liters',
        digits=(16, 4),
    )
    square_meter = fields.Float(
        string="Square Meter",
        compute='_compute_dimensions_quant',
        digits=(16, 4),
    )
    cubic_meter = fields.Float(
        string="Cubic Meter",
        compute='_compute_dimensions_quant',
        digits=(16, 6),
    )

    @api.depends('quantity', 'product_id.liter_capacity')
    def _compute_total_liters(self):
        for rec in self:
            rec.total_liters = rec.quantity * rec.product_id.liter_capacity

    @api.depends('quantity', 'product_id.dimension_length', 'product_id.dimension_width', 'product_id.dimension_thickness')
    def _compute_dimensions_quant(self):
        for rec in self:
            qty = rec.quantity or 0.0
            length = rec.product_id.dimension_length or 0.0
            width = rec.product_id.dimension_width or 0.0
            thickness = rec.product_id.dimension_thickness or 0.0
            
            # الحساب بالمتر المربع والمكعب (قسمة على مليون ومليار للتحويل من ملم)
            rec.square_meter = (length * width * qty) / 1000000.0 if length and width and qty else 0.0
            rec.cubic_meter = (length * width * thickness * qty) / 1000000000.0 if length and width and thickness and qty else 0.0

class StockLocation(models.Model):
    _inherit = 'stock.location'

    square_meter = fields.Float(
        string="Total Square Meter",
        compute='_compute_location_dimensions',
    )
    cubic_meter = fields.Float(
        string="Total Cubic Meter",
        compute='_compute_location_dimensions',
    )

    def _compute_location_dimensions(self):
        for loc in self:
            # البحث عن جميع الكميات الموجودة في هذا الموقع وفروعه
            quants = self.env['stock.quant'].search([('location_id', 'child_of', loc.id)])
            loc.square_meter = sum(quants.mapped('square_meter'))
            loc.cubic_meter = sum(quants.mapped('cubic_meter'))