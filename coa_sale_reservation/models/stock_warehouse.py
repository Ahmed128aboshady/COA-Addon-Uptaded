# -*- coding: utf-8 -*-
from odoo import fields, models, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    is_reservation = fields.Boolean(
        string='Reservation Operation',
        help='Technical flag: this outgoing operation type is used for '
             'customer reservations created from Sales Orders.')


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    reservation_picking_type_id = fields.Many2one(
        'stock.picking.type', string='Reservation Operation Type',
        copy=False, check_company=True)

    def _get_reservation_picking_type(self):
        """Return the reservation operation type of this warehouse,
        creating it on the fly the first time it is needed."""
        self.ensure_one()
        if self.reservation_picking_type_id and self.reservation_picking_type_id.active:
            return self.reservation_picking_type_id

        PickingType = self.env['stock.picking.type'].sudo()
        picking_type = PickingType.with_context(active_test=False).search([
            ('warehouse_id', '=', self.id),
            ('is_reservation', '=', True),
        ], limit=1)
        if picking_type:
            if not picking_type.active:
                picking_type.active = True
        else:
            out_type = self.out_type_id
            picking_type = PickingType.create({
                'name': _('حجز (Reservation)'),
                'code': 'outgoing',
                'sequence_code': 'RES',
                'warehouse_id': self.id,
                'company_id': self.company_id.id,
                'default_location_src_id':
                    out_type.default_location_src_id.id or self.lot_stock_id.id,
                'default_location_dest_id':
                    out_type.default_location_dest_id.id,
                'return_picking_type_id': self.in_type_id.id,
                'is_reservation': True,
                'sequence': (out_type.sequence or 0) + 1,
                'show_operations': out_type.show_operations,
                'use_create_lots': out_type.use_create_lots,
                'use_existing_lots': out_type.use_existing_lots,
                'print_label': out_type.print_label,
            })
        self.sudo().reservation_picking_type_id = picking_type
        return picking_type
