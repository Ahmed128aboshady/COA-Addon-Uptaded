from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    secondary_uom_id = fields.Many2one(
        related='product_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')
    secondary_product_qty = fields.Float(
        'Secondary Qty', digits='Product Unit', default=0.0,
        help="Quantity in the secondary unit of measure.")
    secondary_qty_received = fields.Float(
        'Secondary Received', compute='_compute_secondary_qty_received',
        digits='Product Unit', store=True)

    @api.constrains('secondary_product_qty', 'product_qty', 'has_secondary_uom')
    def _check_secondary_qty(self):
        for line in self:
            if line.has_secondary_uom and line.product_qty > 0 and not line.secondary_product_qty:
                raise ValidationError(
                    "Secondary quantity is mandatory for product '%s' which has a secondary UoM set."
                    % line.product_id.display_name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'product_id' in vals:
                product = self.env['product.product'].browse(vals['product_id'])
                if product.has_secondary_uom and vals.get('product_qty', 0.0) > 0:
                    if not vals.get('secondary_product_qty'):
                        vals['secondary_product_qty'] = vals['product_qty']
        return super().create(vals_list)

    def write(self, vals):
        if 'product_qty' in vals:
            for line in self:
                if line.has_secondary_uom and vals.get('product_qty', 0.0) > 0:
                    if 'secondary_product_qty' not in vals and not line.secondary_product_qty:
                        line.secondary_product_qty = vals['product_qty']
        return super().write(vals)

    @api.depends('move_ids.state', 'move_ids.secondary_quantity')
    def _compute_secondary_qty_received(self):
        for line in self:
            if not line.has_secondary_uom:
                line.secondary_qty_received = 0.0
                continue
            total = 0.0
            for move in line._get_po_line_moves():
                if move.state == 'done':
                    if move._is_purchase_return():
                        if not move.origin_returned_move_id or move.to_refund:
                            total -= move.secondary_quantity
                    else:
                        total += move.secondary_quantity
            line.secondary_qty_received = total

    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, po):
        """Pick up secondary qty from procurement values (e.g. MO component → Buy → PO)."""
        res = super()._prepare_purchase_order_line_from_procurement(
            product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, po)
        if values.get('secondary_product_uom_qty'):
            res['secondary_product_qty'] = values['secondary_product_uom_qty']
        return res

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        vals = super()._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        if self.has_secondary_uom:
            vals['secondary_product_uom_qty'] = self.secondary_product_qty
            vals['secondary_uom_id'] = self.secondary_uom_id.id
        return vals

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=move)
        if self.has_secondary_uom:
            res['secondary_quantity'] = self.secondary_product_qty
        return res
