from odoo import api, fields, models
from odoo.tools.float_utils import float_round, float_is_zero


class StockMove(models.Model):
    _inherit = 'stock.move'

    secondary_uom_id = fields.Many2one(
        'uom.uom', string='Secondary UoM',
        compute='_compute_secondary_uom_id', store=True, readonly=False)
    secondary_product_uom_qty = fields.Float(
        'Secondary Demand', digits='Product Unit', default=0.0,
        help="Quantity demanded in the secondary unit of measure.")
    secondary_quantity = fields.Float(
        'Secondary Done', digits='Product Unit',
        compute='_compute_secondary_quantity', store=True, readonly=False,
        help="Done quantity in the secondary unit of measure.")
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')

    @api.depends('product_id.secondary_uom_id')
    def _compute_secondary_uom_id(self):
        for move in self:
            move.secondary_uom_id = move.product_id.secondary_uom_id

    @api.depends('quantity', 'product_uom_qty', 'secondary_product_uom_qty')
    def _compute_secondary_quantity(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit')
        for move in self:
            if move.has_secondary_uom and move.product_uom_qty and move.secondary_product_uom_qty:
                ratio = move.quantity / move.product_uom_qty
                move.secondary_quantity = float_round(
                    move.secondary_product_uom_qty * ratio,
                    precision_digits=precision)
            else:
                move.secondary_quantity = 0.0

    def _action_done(self, cancel_backorder=False):
        """After standard action_done, update secondary quantities on quants."""
        res = super()._action_done(cancel_backorder=cancel_backorder)

        for move in self:
            if not move.has_secondary_uom or not move.secondary_quantity:
                continue
            if not move.move_line_ids:
                continue

            # Distribute secondary qty proportionally across move lines
            total_primary = sum(move.move_line_ids.mapped('quantity'))
            if not total_primary:
                continue

            Quant = self.env['stock.quant']
            for ml in move.move_line_ids:
                if not ml.quantity:
                    continue
                ratio = ml.quantity / total_primary
                ml_secondary = float_round(
                    move.secondary_quantity * ratio,
                    precision_digits=self.env['decimal.precision'].precision_get('Product Unit'))

                # Decrease secondary qty at source location
                Quant._update_secondary_quantity(
                    ml.product_id, ml.location_id,
                    -ml_secondary,
                    lot_id=ml.lot_id,
                    package_id=ml.package_id,
                    owner_id=ml.owner_id)
                # Increase secondary qty at destination location
                Quant._update_secondary_quantity(
                    ml.product_id, ml.location_dest_id,
                    ml_secondary,
                    lot_id=ml.lot_id,
                    package_id=ml.result_package_id,
                    owner_id=ml.owner_id)

        return res

    def _prepare_procurement_values(self):
        """Pass secondary qty through procurement chain (e.g. MO → Buy → PO)."""
        values = super()._prepare_procurement_values()
        if self.has_secondary_uom and self.secondary_product_uom_qty:
            values['secondary_product_uom_qty'] = self.secondary_product_uom_qty
            values['secondary_uom_id'] = self.secondary_uom_id.id
        return values

    def _prepare_move_split_vals(self, qty):
        """qty here is in move's product_uom (or product UoM if force_split_uom_id is set)."""
        vals = super()._prepare_move_split_vals(qty)
        if self.has_secondary_uom and self.secondary_product_uom_qty and self.product_uom_qty:
            ratio = vals['product_uom_qty'] / self.product_uom_qty
            precision = self.env['decimal.precision'].precision_get('Product Unit')
            vals['secondary_product_uom_qty'] = float_round(
                self.secondary_product_uom_qty * ratio,
                precision_digits=precision)
        return vals

    def _split(self, qty, restrict_partner_id=False):
        """After split, reduce original move's secondary qty proportionally."""
        original_secondary = self.secondary_product_uom_qty
        original_primary = self.product_uom_qty

        result = super()._split(qty, restrict_partner_id=restrict_partner_id)

        if result and self.has_secondary_uom and original_secondary and original_primary:
            new_primary = self.product_uom_qty
            precision = self.env['decimal.precision'].precision_get('Product Unit')
            remaining_ratio = new_primary / original_primary if original_primary else 0.0
            new_secondary = float_round(
                original_secondary * remaining_ratio,
                precision_digits=precision)
            self.write({'secondary_product_uom_qty': max(0, new_secondary)})

        return result
