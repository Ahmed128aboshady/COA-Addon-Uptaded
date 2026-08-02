# -*- coding: utf-8 -*-
from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        """When a customer invoice is posted, convert any reservation
        transfers of the related Sale Order(s) back to the standard
        outgoing Delivery operation type.

        Requested behaviour:
        * Triggered only on POST (not on draft invoices).
        * Applies even to pickings already in the 'done' state.
        """
        posted = super()._post(soft=soft)
        # Act only on the invoices that actually got posted in this call.
        posted.filtered(
            lambda m: m.move_type in ('out_invoice', 'out_refund')
        )._coa_convert_reservation_to_delivery()
        return posted

    def _coa_convert_reservation_to_delivery(self):
        """Swap reservation picking type -> standard delivery type on every
        reservation transfer linked to the invoice's sale order(s)."""
        for move in self:
            orders = move.line_ids.sale_line_ids.order_id
            reservation_orders = orders.filtered('is_reservation')
            if not reservation_orders:
                continue

            for order in reservation_orders:
                pickings = order.picking_ids.filtered(
                    lambda p: p.picking_type_id.is_reservation
                    and p.state != 'cancel')
                for picking in pickings:
                    self._coa_switch_picking_to_delivery(picking)

    @staticmethod
    def _coa_switch_picking_to_delivery(picking):
        """Move a single picking from its reservation operation type to the
        warehouse's standard outgoing Delivery type.

        Handles 'done' pickings too: the picking type on a validated transfer
        is normally read-only, so the write is forced with sudo() and the
        move lines are realigned to keep the data consistent.
        """
        warehouse = picking.picking_type_id.warehouse_id
        if not warehouse:
            return
        delivery_type = warehouse.out_type_id
        # Guard: only convert genuine reservation types, and skip if the
        # warehouse has no standard delivery type for some reason.
        if not delivery_type or not picking.picking_type_id.is_reservation:
            return
        if picking.picking_type_id.id == delivery_type.id:
            return

        picking_sudo = picking.sudo()
        picking_sudo.write({'picking_type_id': delivery_type.id})
        # Keep the moves' picking_type_id in sync (used by some reports/flows).
        moves_sudo = picking_sudo.move_ids.sudo()
        if moves_sudo:
            moves_sudo.write({'picking_type_id': delivery_type.id})
