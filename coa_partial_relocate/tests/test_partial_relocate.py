# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPartialRelocate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env['stock.warehouse'].search(
            [('company_id', '=', cls.env.company.id)], limit=1)
        cls.stock_loc = cls.warehouse.lot_stock_id
        cls.dest_loc = cls.env['stock.location'].create({
            'name': 'COA Shelf B',
            'usage': 'internal',
            'location_id': cls.stock_loc.location_id.id,
        })
        cls.product = cls.env['product.product'].create({
            'name': 'COA Metal Pen',
            'is_storable': True,
        })
        cls.env['stock.quant']._update_available_quantity(
            cls.product, cls.stock_loc, 100.0)
        cls.quant = cls.env['stock.quant'].search([
            ('product_id', '=', cls.product.id),
            ('location_id', '=', cls.stock_loc.id),
        ], limit=1)

    def _open_wizard(self, quants):
        action = quants.action_stock_quant_relocate()
        return self.env['stock.quant.relocate'].with_context(
            **action['context']).create({
                'dest_location_id': self.dest_loc.id,
            })

    def _qty(self, location):
        return self.env['stock.quant']._get_available_quantity(
            self.product, location)

    def test_01_lines_are_populated_with_free_qty_default(self):
        wizard_vals = self.env['stock.quant.relocate'].with_context(
            default_quant_ids=self.quant.ids).default_get(
                ['quant_ids', 'line_ids'])
        self.assertTrue(wizard_vals.get('line_ids'))
        self.assertEqual(
            wizard_vals['line_ids'][0][2]['qty_to_relocate'], 100.0)

    def test_02_partial_relocate_moves_only_requested_qty(self):
        wizard = self._open_wizard(self.quant)
        wizard.line_ids.qty_to_relocate = 40.0
        wizard.action_relocate_quants()
        self.assertEqual(self._qty(self.stock_loc), 60.0)
        self.assertEqual(self._qty(self.dest_loc), 40.0)

    def test_03_full_qty_uses_native_flow(self):
        wizard = self._open_wizard(self.quant)
        wizard.line_ids.qty_to_relocate = 100.0
        wizard.action_relocate_quants()
        self.assertEqual(self._qty(self.stock_loc), 0.0)
        self.assertEqual(self._qty(self.dest_loc), 100.0)

    def test_04_cannot_exceed_free_qty(self):
        wizard = self._open_wizard(self.quant)
        wizard.line_ids.qty_to_relocate = 150.0
        with self.assertRaises(UserError):
            wizard.action_relocate_quants()

    def test_05_reserved_qty_is_protected(self):
        # Reserve 30 units through an outgoing move.
        move = self.env['stock.move'].create({
            'name': 'Reserve 30',
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 30.0,
            'location_id': self.stock_loc.id,
            'location_dest_id': self.env.ref(
                'stock.stock_location_customers').id,
        })
        move._action_confirm()
        move._action_assign()
        self.assertEqual(self.quant.reserved_quantity, 30.0)

        # Default proposed qty must be the free qty (70).
        wizard_vals = self.env['stock.quant.relocate'].with_context(
            default_quant_ids=self.quant.ids).default_get(
                ['quant_ids', 'line_ids'])
        self.assertEqual(
            wizard_vals['line_ids'][0][2]['qty_to_relocate'], 70.0)

        # Trying to move more than the free qty must fail.
        wizard = self._open_wizard(self.quant)
        wizard.line_ids.qty_to_relocate = 80.0
        with self.assertRaises(UserError):
            wizard.action_relocate_quants()

        # Moving exactly the free qty must succeed and keep the
        # reservation untouched in the source location.
        wizard = self._open_wizard(self.quant)
        wizard.line_ids.qty_to_relocate = 70.0
        wizard.action_relocate_quants()
        self.assertEqual(self._qty(self.dest_loc), 70.0)
        self.assertEqual(self.quant.reserved_quantity, 30.0)
        self.assertEqual(move.state, 'assigned')

    def test_06_all_zero_lines_raise(self):
        wizard = self._open_wizard(self.quant)
        wizard.line_ids.qty_to_relocate = 0.0
        with self.assertRaises(UserError):
            wizard.action_relocate_quants()
