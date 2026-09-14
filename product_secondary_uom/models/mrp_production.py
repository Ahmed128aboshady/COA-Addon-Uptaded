from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    secondary_uom_id = fields.Many2one(
        related='product_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')
    secondary_product_qty = fields.Float(
        'Secondary Quantity', digits='Product Unit', default=0.0,
        help="Quantity to produce in the secondary unit of measure.")

    @api.onchange('secondary_product_qty')
    def _onchange_secondary_product_qty(self):
        """Propagate secondary qty to the finished goods move."""
        if self.has_secondary_uom and self.move_finished_ids:
            for move in self.move_finished_ids.filtered(
                    lambda m: m.product_id == self.product_id):
                move.secondary_product_uom_qty = self.secondary_product_qty

    def _set_qty_producing(self, pick_manual_consumption_moves=True):
        res = super()._set_qty_producing(pick_manual_consumption_moves=pick_manual_consumption_moves)
        # When setting qty producing, propagate secondary qty to finished move lines
        if self.has_secondary_uom:
            for move in self.move_finished_ids.filtered(
                    lambda m: m.product_id == self.product_id):
                move.secondary_product_uom_qty = self.secondary_product_qty
        return res

    def _get_move_raw_values(self, product, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        """Propagate secondary qty from BOM line to component stock move."""
        vals = super()._get_move_raw_values(product, product_uom_qty, product_uom, operation_id=operation_id, bom_line=bom_line)
        if bom_line and bom_line.secondary_product_qty and bom_line.product_qty:
            precision = self.env['decimal.precision'].precision_get('Product Unit')
            ratio = product_uom_qty / bom_line.product_qty
            vals['secondary_product_uom_qty'] = float_round(
                bom_line.secondary_product_qty * ratio,
                precision_digits=precision)
            vals['secondary_uom_id'] = bom_line.secondary_uom_id.id
        return vals
