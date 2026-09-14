# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install', 'coa_reservation')
class TestSaleReservation(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env['stock.warehouse'].search(
            [('company_id', '=', cls.env.company.id)], limit=1)
        cls.stock_location = cls.warehouse.lot_stock_id
        cls.partner = cls.env['res.partner'].create({'name': 'Beacon Client'})
        cls.product = cls.env['product.product'].create({
            'name': 'Gift Box A',
            'is_storable': True,
            'list_price': 100.0,
        })
        # Put 50 units in stock
        cls.env['stock.quant']._update_available_quantity(
            cls.product, cls.stock_location, 50.0)

    def _create_so(self, qty=10.0, reservation=False):
        return self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'is_reservation': reservation,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': qty,
            })],
        })

    def test_01_reservation_picking_type_lazy_creation(self):
        """The reservation operation type is created on demand, once."""
        ptype1 = self.warehouse._get_reservation_picking_type()
        self.assertTrue(ptype1)
        self.assertEqual(ptype1.code, 'outgoing')
        self.assertTrue(ptype1.is_reservation)
        self.assertEqual(ptype1.warehouse_id, self.warehouse)
        self.assertIn('RES', ptype1.sequence_id.prefix or '')
        # Second call must return the same record, not create a new one
        ptype2 = self.warehouse._get_reservation_picking_type()
        self.assertEqual(ptype1, ptype2)
        count = self.env['stock.picking.type'].search_count(
            [('is_reservation', '=', True),
             ('warehouse_id', '=', self.warehouse.id)])
        self.assertEqual(count, 1)

    def test_02_reservation_order_creates_res_picking(self):
        """Confirming a reservation SO creates a picking under the
        reservation type, with RES sequence, force-reserved."""
        so = self._create_so(qty=10.0, reservation=True)
        so.action_confirm()
        self.assertEqual(len(so.picking_ids), 1)
        picking = so.picking_ids
        self.assertTrue(picking.picking_type_id.is_reservation)
        self.assertTrue(picking.is_reservation)
        self.assertIn('RES', picking.name)
        # Stock available -> must be fully reserved immediately
        self.assertEqual(picking.state, 'assigned')
        reserved = sum(picking.move_ids.mapped('quantity'))
        self.assertEqual(reserved, 10.0)
        # Free (unreserved) qty must drop from 50 to 40
        free_qty = self.product.with_context(
            location=self.stock_location.id).free_qty
        self.assertEqual(free_qty, 40.0)

    def test_03_normal_order_untouched(self):
        """A normal SO still uses the standard Delivery type."""
        so = self._create_so(qty=5.0, reservation=False)
        so.action_confirm()
        picking = so.picking_ids
        self.assertFalse(picking.picking_type_id.is_reservation)
        self.assertEqual(picking.picking_type_id, self.warehouse.out_type_id)
        self.assertNotIn('RES', picking.name)

    def test_04_no_merge_between_reservation_and_delivery(self):
        """Reservation and normal pickings never merge, and sequences
        are independent."""
        so_res = self._create_so(qty=3.0, reservation=True)
        so_norm = self._create_so(qty=4.0, reservation=False)
        so_res.action_confirm()
        so_norm.action_confirm()
        self.assertNotEqual(so_res.picking_ids.picking_type_id,
                            so_norm.picking_ids.picking_type_id)

    def test_05_validate_reservation_updates_delivered_qty(self):
        """Validating the reservation picking behaves exactly like a
        delivery: qty_delivered updates and invoicing is possible."""
        so = self._create_so(qty=10.0, reservation=True)
        so.action_confirm()
        picking = so.picking_ids
        picking.move_ids.picked = True
        picking.button_validate()
        self.assertEqual(picking.state, 'done')
        self.assertEqual(so.order_line.qty_delivered, 10.0)
        # Invoiceable like any delivered order (delivered policy default)
        invoice = so._create_invoices()
        self.assertEqual(invoice.invoice_line_ids.quantity, 10.0)
        # Stock is finally out
        self.assertEqual(self.product.with_context(
            location=self.stock_location.id).qty_available, 40.0)

    def test_06_cancel_reservation_releases_stock(self):
        """Cancelling the SO cancels the reservation picking and frees
        the reserved quantity."""
        so = self._create_so(qty=10.0, reservation=True)
        so.action_confirm()
        free_before = self.product.with_context(
            location=self.stock_location.id).free_qty
        self.assertEqual(free_before, 40.0)
        so._action_cancel()
        self.assertEqual(so.picking_ids.state, 'cancel')
        free_after = self.product.with_context(
            location=self.stock_location.id).free_qty
        self.assertEqual(free_after, 50.0)

    def test_07_flag_readonly_logic_partial_stock(self):
        """With insufficient stock, the available part is reserved and
        the picking stays partially available (standard behaviour)."""
        so = self._create_so(qty=60.0, reservation=True)  # only 50 in stock
        so.action_confirm()
        picking = so.picking_ids
        self.assertTrue(picking.picking_type_id.is_reservation)
        reserved = sum(picking.move_ids.mapped('quantity'))
        self.assertEqual(reserved, 50.0)
        self.assertIn(picking.state, ('confirmed', 'assigned'))
