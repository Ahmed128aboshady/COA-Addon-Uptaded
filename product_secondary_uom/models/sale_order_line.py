from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    secondary_uom_id = fields.Many2one(
        related='product_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')
    secondary_product_uom_qty = fields.Float(
        'Secondary Qty', digits='Product Unit', default=0.0,
        help="Quantity in the secondary unit of measure.")
    secondary_qty_delivered = fields.Float(
        'Secondary Delivered', compute='_compute_secondary_qty_delivered',
        digits='Product Unit', store=True)

    @api.constrains('secondary_product_uom_qty', 'product_uom_qty', 'has_secondary_uom')
    def _check_secondary_qty(self):
        for line in self:
            if line.has_secondary_uom and line.product_uom_qty > 0 and not line.secondary_product_uom_qty:
                raise ValidationError(
                    "Secondary quantity is mandatory for product '%s' which has a secondary UoM set."
                    % line.product_id.display_name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'product_id' in vals:
                product = self.env['product.product'].browse(vals['product_id'])
                if product.has_secondary_uom and vals.get('product_uom_qty', 0.0) > 0:
                    if not vals.get('secondary_product_uom_qty'):
                        vals['secondary_product_uom_qty'] = vals['product_uom_qty']
        return super().create(vals_list)

    def write(self, vals):
        if 'product_uom_qty' in vals:
            for line in self:
                if line.has_secondary_uom and vals.get('product_uom_qty', 0.0) > 0:
                    if 'secondary_product_uom_qty' not in vals and not line.secondary_product_uom_qty:
                        line.secondary_product_uom_qty = vals['product_uom_qty']
        return super().write(vals)

    @api.depends('move_ids.state', 'move_ids.secondary_quantity')
    def _compute_secondary_qty_delivered(self):
        for line in self:
            if not line.has_secondary_uom:
                line.secondary_qty_delivered = 0.0
                continue
            qty = 0.0
            outgoing_moves, incoming_moves = line._get_outgoing_incoming_moves()
            for move in outgoing_moves:
                if move.state == 'done':
                    qty += move.secondary_quantity
            for move in incoming_moves:
                if move.state == 'done':
                    qty -= move.secondary_quantity
            line.secondary_qty_delivered = qty

    def _prepare_procurement_values(self):
        values = super()._prepare_procurement_values()
        if self.has_secondary_uom:
            values['secondary_product_uom_qty'] = self.secondary_product_uom_qty
            values['secondary_uom_id'] = self.secondary_uom_id.id
        return values

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        if self.has_secondary_uom:
            res['secondary_quantity'] = self.secondary_product_uom_qty
        return res
