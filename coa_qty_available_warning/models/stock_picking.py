# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.tools import float_compare


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _coa_collect_shortages(self):
        """Return a list of dicts describing lines short on company-wide
        Free To Use stock. Only outgoing moves from internal locations."""
        self.ensure_one()
        shortages = []
        for move in self.move_ids:
            product = move.product_id
            if not product or product.type != 'consu' or not product.is_storable:
                continue
            # Only care when stock is leaving an internal location.
            if move.location_id.usage != 'internal':
                continue
            if move.state in ('done', 'cancel'):
                continue
            free_qty = product.with_company(self.company_id).free_qty
            # Add back this move's own reservation so it doesn't count
            # against itself (e.g. internal transfers reserving from the
            # same internal location they're leaving).
            reserved_by_move = sum(
                move.move_line_ids.filtered(
                    lambda ml: ml.location_id.usage == 'internal'
                ).mapped('quantity')
            )
            free_qty += reserved_by_move
            if move.product_uom and move.product_uom != product.uom_id:
                free_qty = product.uom_id._compute_quantity(
                    free_qty, move.product_uom, rounding_method='HALF-UP')
            demand = move.product_uom_qty
            rounding = (move.product_uom or product.uom_id).rounding
            if float_compare(demand, free_qty,
                                    precision_rounding=rounding) > 0:
                shortages.append({
                    'product_id': product.id,
                    'demand_qty': demand,
                    'free_qty': free_qty,
                    'shortage_qty': demand - free_qty,
                    'uom_id': (move.product_uom or product.uom_id).id,
                })
        return shortages

    def button_validate(self):
        # Skip when the user already confirmed through the wizard.
        if self.env.context.get('coa_skip_qty_warning'):
            return super().button_validate()
        if not self.env.company.coa_qty_warning_enabled:
            return super().button_validate()

        pickings_with_shortage = self.env['stock.picking']
        all_lines = []
        for picking in self:
            shortages = picking._coa_collect_shortages()
            if shortages:
                pickings_with_shortage |= picking
                for vals in shortages:
                    vals['picking_id'] = picking.id
                    all_lines.append(vals)

        if not all_lines:
            return super().button_validate()

        wizard = self.env['coa.qty.warning.wizard'].create({
            'picking_ids': [(6, 0, self.ids)],
            'line_ids': [(0, 0, vals) for vals in all_lines],
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Not Enough Quantity Available'),
            'res_model': 'coa.qty.warning.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
            'context': dict(self.env.context),
        }
