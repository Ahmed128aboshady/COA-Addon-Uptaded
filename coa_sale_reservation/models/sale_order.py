# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_reservation = fields.Boolean(
        string='حجز (Reservation)', copy=False, tracking=True,
        help='When checked, the transfer generated on confirmation will be '
             'created under the dedicated "Reservation" operation type '
             'instead of the standard Delivery, and the stock will be '
             'reserved immediately.')

    def _action_confirm(self):
        res = super()._action_confirm()
        # Force-reserve the stock of reservation pickings right away so
        # the reserved goods cannot be taken by other orders/pickings.
        for order in self.filtered('is_reservation'):
            pickings = order.picking_ids.filtered(
                lambda p: p.picking_type_id.is_reservation
                and p.state in ('confirmed', 'waiting', 'assigned'))
            if pickings:
                pickings.action_assign()
        return res
