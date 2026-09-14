# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    coa_free_qty = fields.Float(
        string='Available (Free To Use)',
        compute='_compute_coa_free_qty',
        digits='Product Unit of Measure',
        help='Quantity available across the whole company (Free To Use), '
             'expressed in the unit of measure of this line.')
    coa_qty_warning = fields.Boolean(
        string='Not Enough Stock', compute='_compute_coa_free_qty')

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _coa_get_free_qty(self, product, uom=None):
        """Company-wide Free To Use quantity of `product`, converted to `uom`.

        Storable products only; services / consumables return False.
        """
        if not product or product.type != 'consu' or not product.is_storable:
            return None
        # No location in the context => Odoo computes over all internal
        # locations of the allowed companies.
        qty = product.with_company(self.env.company).free_qty
        if uom and uom != product.uom_id:
            qty = product.uom_id._compute_quantity(
                qty, uom, rounding_method='HALF-UP')
        return qty

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_coa_free_qty(self):
        for line in self:
            free_qty = line._coa_get_free_qty(line.product_id, line.product_uom)
            if free_qty is None:
                line.coa_free_qty = 0.0
                line.coa_qty_warning = False
                continue
            line.coa_free_qty = free_qty
            rounding = (line.product_uom or line.product_id.uom_id).rounding
            line.coa_qty_warning = bool(
                line.product_uom_qty
                and float_compare(
                    line.product_uom_qty, free_qty,
                    precision_rounding=rounding) > 0)

