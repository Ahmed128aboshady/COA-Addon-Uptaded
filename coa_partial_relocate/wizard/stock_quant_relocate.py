# -*- coding: utf-8 -*-
# Part of COA Partial Quantity Relocate.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class RelocateStockQuant(models.TransientModel):
    _inherit = 'stock.quant.relocate'

    line_ids = fields.One2many(
        'stock.quant.relocate.line', 'wizard_id',
        string='Quantities to Relocate',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'line_ids' in fields_list:
            quant_ids = self.env.context.get('default_quant_ids') or []
            quants = self.env['stock.quant'].browse(quant_ids).exists()
            res['line_ids'] = [
                (0, 0, {
                    'quant_id': quant.id,
                    'qty_to_relocate': max(
                        quant.quantity - quant.reserved_quantity, 0.0),
                })
                for quant in quants
            ]
        return res

    def action_relocate_quants(self):
        self.ensure_one()
        if not self.line_ids:
            # Wizard used without lines (e.g. programmatically):
            # keep 100% native behavior.
            return super().action_relocate_quants()

        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')

        # ---- Validation -------------------------------------------------
        for line in self.line_ids:
            free_qty = line.quant_id.quantity - line.quant_id.reserved_quantity
            if float_compare(line.qty_to_relocate, 0,
                             precision_digits=precision) < 0:
                raise UserError(_(
                    'The quantity to relocate cannot be negative '
                    '(product: %(product)s).',
                    product=line.product_id.display_name))
            if float_compare(line.qty_to_relocate, free_qty,
                             precision_digits=precision) > 0:
                raise UserError(_(
                    'You cannot relocate %(qty)s of product %(product)s '
                    'from location %(location)s: only %(free)s is free '
                    '(%(onhand)s on hand - %(reserved)s reserved). '
                    'Reserved quantities cannot be relocated.',
                    qty=line.qty_to_relocate,
                    product=line.product_id.display_name,
                    location=line.location_id.display_name,
                    free=max(free_qty, 0.0),
                    onhand=line.quant_id.quantity,
                    reserved=line.quant_id.reserved_quantity))

        zero_lines = self.line_ids.filtered(lambda l: float_is_zero(
            l.qty_to_relocate, precision_digits=precision))
        if len(zero_lines) == len(self.line_ids):
            raise UserError(_(
                'Please set a quantity to relocate on at least one line.'))

        partial_lines = self.line_ids.filtered(
            lambda l: not float_is_zero(
                l.qty_to_relocate, precision_digits=precision)
            and float_compare(l.qty_to_relocate, l.quant_id.quantity,
                              precision_digits=precision) < 0)

        # Quants the user chose not to move at all.
        self.quant_ids -= zero_lines.quant_id

        if not partial_lines:
            # Every remaining line is at full quantity (and, thanks to the
            # validation above, fully unreserved): native flow.
            return super().action_relocate_quants()

        if not self.dest_location_id and not self.dest_package_id:
            return

        # ---- Partial relocation (mirrors stock.quant.move_quants) -------
        partial_quants = partial_lines.quant_id
        all_quants = self.quant_ids
        lot_ids = all_quants.lot_id
        product_ids = all_quants.product_id

        partial_quants.action_clear_inventory_quantity()
        message = self.message or _('Quantity Relocated')
        move_vals = []
        for line in partial_lines:
            quant = line.quant_id
            # The moved portion leaves its source package: it is either
            # placed in the chosen destination package or unpacked.
            move_vals.append(
                quant.with_context(inventory_name=message)
                ._get_inventory_move_values(
                    line.qty_to_relocate,
                    quant.location_id,
                    self.dest_location_id or quant.location_id,
                    quant.package_id,
                    self.dest_package_id,
                ))
        moves = self.env['stock.move'].create(move_vals)
        moves._action_done()

        # ---- Full-quantity quants: hand over to the native flow ---------
        remaining = self.quant_ids - partial_quants
        self.quant_ids = remaining
        if remaining:
            return super().action_relocate_quants()

        # Replicate the native return behavior for consistency.
        if self.env.context.get('default_lot_id', False) and len(lot_ids) == 1:
            return lot_ids.action_lot_open_quants()
        elif (self.env.context.get('single_product', False)
              and len(product_ids) == 1):
            return product_ids.action_update_quantity_on_hand()
        return all_quants.with_context(
            always_show_loc=1).action_view_quants()


class RelocateStockQuantLine(models.TransientModel):
    _name = 'stock.quant.relocate.line'
    _description = 'Stock Relocation Line'

    wizard_id = fields.Many2one(
        'stock.quant.relocate', required=True, ondelete='cascade')
    quant_id = fields.Many2one(
        'stock.quant', required=True, ondelete='cascade')
    product_id = fields.Many2one(
        related='quant_id.product_id', string='Product')
    location_id = fields.Many2one(
        related='quant_id.location_id', string='From Location')
    lot_id = fields.Many2one(
        related='quant_id.lot_id', string='Lot/Serial')
    package_id = fields.Many2one(
        related='quant_id.package_id', string='Package')
    product_uom_id = fields.Many2one(
        related='quant_id.product_uom_id', string='Unit')
    available_qty = fields.Float(
        related='quant_id.quantity', string='On Hand')
    reserved_qty = fields.Float(
        related='quant_id.reserved_quantity', string='Reserved')
    free_qty = fields.Float(
        string='Available to Move', compute='_compute_free_qty',
        digits='Product Unit of Measure', store=False)
    qty_to_relocate = fields.Float(
        string='Qty to Relocate', digits='Product Unit of Measure',
        default=0.0)

    @api.depends('quant_id', 'quant_id.quantity', 'quant_id.reserved_quantity')
    def _compute_free_qty(self):
        for line in self:
            line.free_qty = max(
                line.quant_id.quantity - line.quant_id.reserved_quantity, 0.0)

    @api.onchange('qty_to_relocate')
    def _onchange_qty_to_relocate(self):
        if not self.quant_id:
            return
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        free = max(
            self.quant_id.quantity - self.quant_id.reserved_quantity, 0.0)
        if float_compare(self.qty_to_relocate, 0,
                         precision_digits=precision) < 0:
            self.qty_to_relocate = 0.0
            return {'warning': {
                'title': _('Invalid Quantity'),
                'message': _('Quantity cannot be negative.'),
            }}
        if float_compare(self.qty_to_relocate, free,
                         precision_digits=precision) > 0:
            self.qty_to_relocate = free
            return {'warning': {
                'title': _('Reserved Quantity'),
                'message': _(
                    'You cannot relocate reserved quantities. '
                    'The quantity has been set to the maximum '
                    'free quantity: %(free)s.',
                    free=free),
            }}
