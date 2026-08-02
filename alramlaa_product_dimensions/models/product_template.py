# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dimension_length = fields.Float(string='Length (mm) / الطول (مم)')
    dimension_width = fields.Float(string='Width (mm) / العرض (مم)')
    dimension_thickness = fields.Float(string='Thickness (mm) / السماكه (مم)')
    square_meter = fields.Float(
        string='Square Meter / متر مربع',
        compute='_compute_square_cubic_meter',
        store=True,
        digits=(16, 6),
    )
    cubic_meter = fields.Float(
        string='Cubic Meter / متر مكعب',
        compute='_compute_square_cubic_meter',
        store=True,
        digits=(16, 9),
    )
    waste_percentage = fields.Float(string='Waste % / نسبة الهالك (%)')
    product_color = fields.Char(string='Color / اللون')
    expiry_date = fields.Date(string='Expiry Date / تاريخ الصلاحية')
    country_of_origin = fields.Many2one('res.country', string='Country of Origin / بلد المنشأ')

    liter_capacity = fields.Float(
        string='Liters Capacity / سعة اللتر',
        digits=(16, 4),
    )
    total_liters = fields.Float(
        string='Total Liters / إجمالي اللترات',
        compute='_compute_total_liters',
        store=True,
        digits=(16, 4),
    )

    @api.depends('dimension_length', 'dimension_width', 'dimension_thickness')
    def _compute_square_cubic_meter(self):
        for rec in self:
            length = rec.dimension_length
            width = rec.dimension_width
            thickness = rec.dimension_thickness
            rec.square_meter = (length * width) / 1000000.0 if length and width else 0.0
            rec.cubic_meter = (length * width * thickness) / 1000000000.0 if length and width and thickness else 0.0

    @api.depends('qty_available', 'liter_capacity')
    def _compute_total_liters(self):
        for rec in self:
            rec.total_liters = rec.qty_available * rec.liter_capacity