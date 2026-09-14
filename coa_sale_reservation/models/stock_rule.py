# -*- coding: utf-8 -*-
from odoo import fields, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_dest_id, name, origin, company_id,
                               values):
        """Swap the outgoing picking type with the warehouse reservation
        type when the source Sales Order is flagged as a reservation.

        Done at procurement time (before the picking exists) so the
        picking is created directly with the RES/ sequence and is never
        merged with standard deliveries."""
        move_values = super()._get_stock_move_values(
            product_id, product_qty, product_uom, location_dest_id, name,
            origin, company_id, values)

        group = values.get('group_id')
        sale_order = group.sale_id if group else False
        if (sale_order and sale_order.is_reservation
                and self.picking_type_id.code == 'outgoing'
                and not self.picking_type_id.is_reservation):
            warehouse = self.picking_type_id.warehouse_id or self.warehouse_id
            if warehouse:
                reservation_type = warehouse._get_reservation_picking_type()
                move_values['picking_type_id'] = reservation_type.id
        return move_values


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def write(self, vals):
        """Do not block invoice confirmation when a completed transfer is
        included in a picking-type update.

        Odoo forbids changing ``picking_type_id`` after a picking is done.
        For completed pickings we keep the original operation type and apply
        any other values normally. Non-completed pickings are still updated.
        """
        if 'picking_type_id' in vals:
            done_pickings = self.filtered(lambda p: p.state == 'done')
            open_pickings = self - done_pickings

            if done_pickings:
                done_vals = dict(vals)
                done_vals.pop('picking_type_id', None)
                if done_vals:
                    super(StockPicking, done_pickings).write(done_vals)

            if open_pickings:
                super(StockPicking, open_pickings).write(vals)

            return True

        return super().write(vals)

    is_reservation = fields.Boolean(
        related='picking_type_id.is_reservation', store=True,
        string='Is Reservation')
