# -*- coding: utf-8 -*-
from odoo import fields, models


class CoaQtyWarningWizard(models.TransientModel):
    _name = 'coa.qty.warning.wizard'
    _description = 'Quantity Available Warning'

    picking_ids = fields.Many2many(
        'stock.picking',
        relation='coa_qty_warn_wiz_picking_rel',
        string='Transfers')
    sale_order_ids = fields.Many2many(
        'sale.order',
        relation='coa_qty_warn_wiz_sale_rel',
        string='Sale Orders')

    line_ids = fields.One2many(
        'coa.qty.warning.wizard.line', 'wizard_id', string='Shortages')

    def action_confirm_anyway(self):
        """Proceed with the stock transfer validation despite the shortage."""
        self.ensure_one()
        return self.picking_ids.with_context(
            coa_skip_qty_warning=True).button_validate()

    def action_confirm_sale_anyway(self):
        """Confirm the sale order(s) despite the shortage."""
        self.ensure_one()
        self.sale_order_ids.with_context(
            coa_skip_qty_warning=True).action_confirm()
        return {'type': 'ir.actions.act_window_close'}


class CoaQtyWarningWizardLine(models.TransientModel):
    _name = 'coa.qty.warning.wizard.line'
    _description = 'Quantity Available Warning Line'

    wizard_id = fields.Many2one(
        'coa.qty.warning.wizard', required=True, ondelete='cascade')
    picking_id = fields.Many2one('stock.picking', string='Transfer')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    product_id = fields.Many2one('product.product', string='Product')
    demand_qty = fields.Float(
        string='Demand', digits='Product Unit of Measure')
    free_qty = fields.Float(
        string='Available (Free To Use)', digits='Product Unit of Measure')
    shortage_qty = fields.Float(
        string='Shortage', digits='Product Unit of Measure')
    uom_id = fields.Many2one('uom.uom', string='Unit')
