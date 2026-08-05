from odoo import models, fields, api
import math

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    # 1. تعريف الحقول
    dimension_length = fields.Float(string="Length (mm)")
    dimension_width = fields.Float(string="Width (mm)")
    dimension_thickness = fields.Float(string="Thickness (mm)")
    square_meter = fields.Float(string="Square Meter", digits=(12, 4))
    cubic_meter = fields.Float(string="Cubic Meter", digits=(12, 4))

    # 2. حساب المربع والمكعب والكمية من الأبعاد
    @api.onchange('dimension_length', 'dimension_width', 'dimension_thickness')
    def _onchange_dimensions(self):
        for rec in self:
            if rec.dimension_length and rec.dimension_width:
                rec.square_meter = (rec.dimension_length * rec.dimension_width) / 1000000
                if rec.dimension_thickness:
                    rec.cubic_meter = rec.square_meter * (rec.dimension_thickness / 1000)
                if rec.square_meter > 0:
                    calculated_qty = rec.square_meter / 5.9536
                    rec.product_qty = math.ceil(calculated_qty)

    # التعديل الأول: لو حطيت المربع (يسمع في المكعب والوحدات)
    @api.onchange('square_meter')
    def _onchange_square_meter(self):
        for rec in self:
            if rec.square_meter > 0:
                # 1. تحديث الوحدات (الكمية)
                calculated_qty = rec.square_meter / 5.9536
                rec.product_qty = math.ceil(calculated_qty)
                # 2. تحديث المكعب (لو التخانة موجودة)
                if rec.dimension_thickness:
                    rec.cubic_meter = rec.square_meter * (rec.dimension_thickness / 1000)

    # التعديل التاني: لو حطيت المكعب (يسمع في المربع والوحدات)
    @api.onchange('cubic_meter')
    def _onchange_cubic_meter(self):
        for rec in self:
            if rec.cubic_meter > 0 and rec.dimension_thickness > 0:
                # 1. تحديث المربع
                rec.square_meter = rec.cubic_meter / (rec.dimension_thickness / 1000)
                # 2. تحديث الوحدات (الكمية)
                calculated_qty = rec.square_meter / 5.9536
                rec.product_qty = math.ceil(calculated_qty)

    # التعديل التالت: لو حطيت الوحدات (تسمع في المربع والمكعب)
    @api.onchange('product_qty')
    def _onchange_quantity(self):
        for rec in self:
            if rec.product_qty > 0:
                # 1. تحديث المربع (سواء بالأبعاد أو بمساحة اللوح الثابتة)
                if rec.dimension_length and rec.dimension_width:
                    single_piece_area = (rec.dimension_length * rec.dimension_width) / 1000000
                    rec.square_meter = single_piece_area * rec.product_qty
                else:
                    rec.square_meter = rec.product_qty * 5.9536
                # 2. تحديث المكعب
                if rec.dimension_thickness:
                    rec.cubic_meter = rec.square_meter * (rec.dimension_thickness / 1000)