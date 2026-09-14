# -*- coding: utf-8 -*-
import logging

from odoo import models
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """Reduce still-draft outgoing moves in place instead of letting the
        standard flow create a return when the ordered quantity is decreased.

        Only lines whose reduction can be fully absorbed by not-done moves are
        handled here. Every other line (increase, partial delivery, reduction
        below delivered qty, etc.) is passed untouched to ``super()`` so the
        standard behaviour -- including returns -- is preserved.
        """
        if self._context.get('skip_procurement'):
            return super()._action_launch_stock_rule(
                previous_product_uom_qty=previous_product_uom_qty)

        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')

        handled = self.env['sale.order.line']
        for line in self:
            if not previous_product_uom_qty:
                continue
            if line.state != 'sale' or line.order_id.locked:
                continue
            if line.product_id.type != 'consu':
                continue

            prev_qty = previous_product_uom_qty.get(line.id)
            if prev_qty is None:
                continue

            new_qty = line.product_uom_qty
            # Only interested in a genuine decrease.
            if float_compare(new_qty, prev_qty,
                             precision_digits=precision) >= 0:
                continue

            if line._coa_reduce_draft_moves(new_qty, precision):
                handled |= line

        remaining = self - handled
        if remaining:
            return super(SaleOrderLine, remaining)._action_launch_stock_rule(
                previous_product_uom_qty=previous_product_uom_qty)
        return True

    def _coa_reduce_draft_moves(self, new_qty, precision):
        """Try to absorb the quantity decrease by shrinking not-done outgoing
        moves in place.

        :return: True if the whole decrease was handled here (line must be
                 excluded from the standard launch), False to fall back to
                 standard behaviour.
        """
        self.ensure_one()

        # Any part already delivered -> let standard flow handle it (return).
        if any(m.state == 'done' for m in self.move_ids):
            return False

        delivered = self.qty_delivered
        # New qty below what is already delivered -> a real return is required.
        if float_compare(new_qty, delivered, precision_digits=precision) < 0:
            return False

        outgoing, incoming = self._get_outgoing_incoming_moves(strict=False)
        # If a return move already exists we don't interfere.
        if incoming:
            return False

        editable = outgoing.filtered(
            lambda m: m.state in ('draft', 'confirmed', 'waiting',
                                   'partially_available', 'assigned'))
        if not editable or editable != outgoing:
            # Some outgoing move is in an unexpected state -> stay safe.
            return False

        target_qty = new_qty - delivered  # in the SO line UoM
        current_qty = sum(
            m.product_uom._compute_quantity(
                m.product_uom_qty, self.product_uom, rounding_method='HALF-UP')
            for m in editable
        )

        # Nothing to shrink (already aligned) -> let super short-circuit.
        if float_compare(current_qty, target_qty,
                         precision_digits=precision) <= 0:
            return True

        # Release any reservation before touching quantities.
        reserved = editable.filtered(
            lambda m: m.state in ('assigned', 'partially_available'))
        if reserved:
            reserved._do_unreserve()

        primary = editable.sorted('id')[0]
        others = editable - primary

        # Cancel surplus secondary moves, keep a single move carrying target.
        if others:
            others._action_cancel()

        primary_target = self.product_uom._compute_quantity(
            target_qty, primary.product_uom, rounding_method='HALF-UP')

        if float_compare(primary_target, 0.0, precision_digits=precision) <= 0:
            # Whole remaining qty already delivered elsewhere -> cancel move.
            primary._action_cancel()
        else:
            primary.product_uom_qty = primary_target
            if reserved and primary.state != 'cancel':
                primary._action_assign()

        _logger.info(
            "COA: reduced draft delivery for SO line %s (%s) "
            "to %s %s in place instead of creating a return.",
            self.id, self.order_id.name, target_qty, self.product_uom.name)
        return True
