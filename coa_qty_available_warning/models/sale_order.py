# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.tools import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # Already bypassed (user clicked "Confirm Anyway" in the wizard)
        if self.env.context.get('coa_skip_qty_warning'):
            return super().action_confirm()
        # Feature disabled in company settings
        if not self.env.company.coa_qty_warning_enabled:
            return super().action_confirm()

        all_lines = []
        for order in self:
            for line in order.order_line:
                product = line.product_id
                if not product or product.type != 'consu' or not product.is_storable:
                    continue
                if not line.product_uom_qty:
                    continue
                free_qty = product.with_company(order.company_id).free_qty
                if line.product_uom and line.product_uom != product.uom_id:
                    free_qty = product.uom_id._compute_quantity(
                        free_qty, line.product_uom,
                        rounding_method='HALF-UP')
                rounding = (line.product_uom or product.uom_id).rounding
                if float_compare(
                        line.product_uom_qty, free_qty,
                        precision_rounding=rounding) > 0:
                    all_lines.append({
                        'sale_order_id': order.id,
                        'product_id': product.id,
                        'demand_qty': line.product_uom_qty,
                        'free_qty': free_qty,
                        'shortage_qty': line.product_uom_qty - free_qty,
                        'uom_id': (line.product_uom or product.uom_id).id,
                    })

        if not all_lines:
            return super().action_confirm()

        wizard = self.env['coa.qty.warning.wizard'].create({
            'sale_order_ids': [(6, 0, self.ids)],
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
