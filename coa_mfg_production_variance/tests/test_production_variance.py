# -*- coding: utf-8 -*-
"""
Tests for coa_mfg_production_variance.

Key notes for Odoo 19 compatibility:
- mrp.production.state is a stored computed field; call self.env.flush_all()
  before querying the SQL view to ensure DB reflects ORM changes.
- button_mark_done() may open a backorder wizard when qty_producing != product_qty;
  use with_context(skip_backorder=True) to suppress it in tests.
- mrp_production has a DB check constraint (qty_positive) preventing product_qty <= 0.
"""
import base64

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestProductionVariance(TransactionCase):
    """Tests for the COA Production Variance report module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        # A consumable product — no BOM needed for simple MO tests.
        cls.product = cls.env['product.product'].create({
            'name': 'Variance Test Product',
            'type': 'consu',
            'uom_id': cls.uom_unit.id,
        })

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _make_mo(self, product_qty=10.0):
        """Create and confirm an MO; return it ready for production."""
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': product_qty,
            'product_uom_id': self.uom_unit.id,
        })
        mo.action_confirm()
        return mo

    def _get_line(self, mo):
        """Return the variance view record(s) for a given MO.

        Flushes all pending ORM writes to the DB first so that the SQL view
        (which reads the mrp_production.state stored computed column) reflects
        the latest ORM state.
        """
        self.env.flush_all()
        return self.env['coa.mfg.production.variance'].search(
            [('production_id', '=', mo.id)])

    def _mark_done(self, mo, qty_producing):
        """Set qty_producing and mark the MO as done.

        Uses skip_backorder=True so that partial production (qty_producing !=
        product_qty) does not open the backorder wizard.
        """
        mo.qty_producing = qty_producing
        if mo.product_uom_id.compare(qty_producing, mo.product_qty) == 0:
            # Exact quantity: no backorder wizard is shown.
            mo.button_mark_done()
        else:
            # Under- or over-produced: skip the backorder dialog.
            mo.with_context(skip_backorder=True).button_mark_done()

    # ------------------------------------------------------------------
    # 1.  SQL view: cancelled MOs are excluded
    # ------------------------------------------------------------------
    def test_cancelled_mo_excluded(self):
        """Cancelled MOs must not appear in the variance view."""
        mo = self._make_mo()
        mo.action_cancel()
        self.assertFalse(
            self._get_line(mo),
            "A cancelled MO must be excluded from the variance view.",
        )

    # ------------------------------------------------------------------
    # 2.  SQL view: confirmed MO shows 0 produced qty
    # ------------------------------------------------------------------
    def test_confirmed_mo_zero_produced(self):
        """A confirmed-but-not-yet-produced MO must appear with produced_qty = 0."""
        mo = self._make_mo(product_qty=10.0)
        line = self._get_line(mo)
        self.assertEqual(len(line), 1, "Exactly one variance line expected.")
        self.assertAlmostEqual(line.planned_qty, 10.0)
        self.assertAlmostEqual(line.produced_qty, 0.0)
        self.assertAlmostEqual(line.variance_qty, -10.0)
        self.assertAlmostEqual(line.variance_percent, -100.0)

    # ------------------------------------------------------------------
    # 3.  SQL view: under-produced MO
    # ------------------------------------------------------------------
    def test_under_produced(self):
        """Produce less than planned: variance must be negative."""
        mo = self._make_mo(product_qty=10.0)
        self._mark_done(mo, 7.0)
        line = self._get_line(mo)
        self.assertEqual(len(line), 1)
        self.assertAlmostEqual(line.planned_qty, 10.0)
        self.assertAlmostEqual(line.produced_qty, 7.0, places=2)
        self.assertAlmostEqual(line.variance_qty, -3.0, places=2)
        self.assertAlmostEqual(line.variance_percent, -30.0, places=2)

    # ------------------------------------------------------------------
    # 4.  SQL view: fully produced MO
    # ------------------------------------------------------------------
    def test_fully_produced(self):
        """Produce exactly planned qty: variance must be 0."""
        mo = self._make_mo(product_qty=10.0)
        self._mark_done(mo, 10.0)
        line = self._get_line(mo)
        self.assertEqual(len(line), 1)
        self.assertAlmostEqual(line.planned_qty, 10.0)
        self.assertAlmostEqual(line.produced_qty, 10.0, places=2)
        self.assertAlmostEqual(line.variance_qty, 0.0, places=2)
        self.assertAlmostEqual(line.variance_percent, 0.0, places=2)

    # ------------------------------------------------------------------
    # 5.  SQL view: over-produced MO
    # ------------------------------------------------------------------
    def test_over_produced(self):
        """Produce more than planned: variance must be positive."""
        mo = self._make_mo(product_qty=10.0)
        self._mark_done(mo, 12.0)
        line = self._get_line(mo)
        self.assertEqual(len(line), 1)
        self.assertAlmostEqual(line.planned_qty, 10.0)
        self.assertAlmostEqual(line.produced_qty, 12.0, places=2)
        self.assertAlmostEqual(line.variance_qty, 2.0, places=2)
        self.assertAlmostEqual(line.variance_percent, 20.0, places=2)

    # ------------------------------------------------------------------
    # 6.  action_open_production returns the correct window action
    # ------------------------------------------------------------------
    def test_action_open_production(self):
        """action_open_production must return an act_window pointing to the MO."""
        mo = self._make_mo(product_qty=5.0)
        line = self._get_line(mo)
        self.assertEqual(len(line), 1)
        action = line.action_open_production()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'mrp.production')
        self.assertEqual(action['res_id'], mo.id)
        self.assertEqual(action['view_mode'], 'form')

    # ------------------------------------------------------------------
    # 7.  Wizard: state_filter='done' returns only done MOs
    # ------------------------------------------------------------------
    def test_wizard_state_filter_done(self):
        """Wizard with state_filter='done' must only include 'done' MOs."""
        mo_done = self._make_mo(product_qty=5.0)
        self._mark_done(mo_done, 5.0)

        mo_confirmed = self._make_mo(product_qty=5.0)  # stays confirmed

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'done',
            'variance_filter': 'all',
        })
        self.env.flush_all()
        domain = wizard._get_domain()
        self.assertIn(('state', '=', 'done'), domain)
        lines = self.env['coa.mfg.production.variance'].search(domain)
        prod_ids = lines.mapped('production_id').ids
        self.assertIn(mo_done.id, prod_ids)
        self.assertNotIn(mo_confirmed.id, prod_ids)

    # ------------------------------------------------------------------
    # 8.  Wizard: variance_filter='under' returns only under-produced MOs
    # ------------------------------------------------------------------
    def test_wizard_variance_filter_under(self):
        """variance_filter='under' must only return under-produced lines."""
        mo_under = self._make_mo(product_qty=10.0)
        self._mark_done(mo_under, 6.0)

        mo_over = self._make_mo(product_qty=10.0)
        self._mark_done(mo_over, 12.0)

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'all',
            'variance_filter': 'under',
        })
        self.env.flush_all()
        lines = wizard._get_lines()
        prod_ids = lines.mapped('production_id').ids
        self.assertIn(mo_under.id, prod_ids)
        self.assertNotIn(mo_over.id, prod_ids)

    # ------------------------------------------------------------------
    # 9.  Wizard: variance_filter='over' returns only over-produced MOs
    # ------------------------------------------------------------------
    def test_wizard_variance_filter_over(self):
        """variance_filter='over' must only return over-produced lines."""
        mo_under = self._make_mo(product_qty=10.0)
        self._mark_done(mo_under, 6.0)

        mo_over = self._make_mo(product_qty=10.0)
        self._mark_done(mo_over, 12.0)

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'all',
            'variance_filter': 'over',
        })
        self.env.flush_all()
        lines = wizard._get_lines()
        prod_ids = lines.mapped('production_id').ids
        self.assertNotIn(mo_under.id, prod_ids)
        self.assertIn(mo_over.id, prod_ids)

    # ------------------------------------------------------------------
    # 10.  Wizard: variance_filter='with_variance' excludes zero-variance MOs
    # ------------------------------------------------------------------
    def test_wizard_variance_filter_with_variance(self):
        """variance_filter='with_variance' must exclude zero-variance lines."""
        mo_exact = self._make_mo(product_qty=5.0)
        self._mark_done(mo_exact, 5.0)

        mo_under = self._make_mo(product_qty=10.0)
        self._mark_done(mo_under, 8.0)

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'all',
            'variance_filter': 'with_variance',
        })
        self.env.flush_all()
        lines = wizard._get_lines()
        prod_ids = lines.mapped('production_id').ids
        self.assertNotIn(mo_exact.id, prod_ids)
        self.assertIn(mo_under.id, prod_ids)

    # ------------------------------------------------------------------
    # 11.  Wizard: _get_totals computes aggregated variance correctly
    # ------------------------------------------------------------------
    def test_wizard_get_totals(self):
        """_get_totals must compute the aggregated planned/produced/variance correctly."""
        mo1 = self._make_mo(product_qty=10.0)
        self._mark_done(mo1, 8.0)

        mo2 = self._make_mo(product_qty=10.0)
        self._mark_done(mo2, 12.0)

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'done',
            'variance_filter': 'all',
            'product_ids': [(6, 0, [self.product.id])],
        })
        self.env.flush_all()
        lines = wizard._get_lines()
        totals = wizard._get_totals(lines)

        total_planned = sum(lines.mapped('planned_qty'))
        total_produced = sum(lines.mapped('produced_qty'))
        self.assertAlmostEqual(totals['planned'], total_planned)
        self.assertAlmostEqual(totals['produced'], total_produced)
        self.assertAlmostEqual(totals['variance'], total_produced - total_planned)
        if total_planned:
            expected_pct = (total_produced - total_planned) / total_planned * 100.0
            self.assertAlmostEqual(totals['percent'], expected_pct, places=4)

    # ------------------------------------------------------------------
    # 12.  Wizard: empty result raises UserError for PDF and Excel
    # ------------------------------------------------------------------
    def test_wizard_no_data_raises_user_error(self):
        """Print PDF/Excel with no matching data must raise UserError."""
        # Create a product that has no MOs at all.
        empty_product = self.env['product.product'].create({
            'name': 'No MO Product',
            'type': 'consu',
        })
        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'done',
            'variance_filter': 'all',
            'product_ids': [(6, 0, [empty_product.id])],
        })
        with self.assertRaises(UserError):
            wizard.action_print_pdf()
        with self.assertRaises(UserError):
            wizard.action_export_xlsx()

    # ------------------------------------------------------------------
    # 13.  Wizard: Excel export produces a valid XLSX binary
    # ------------------------------------------------------------------
    def test_wizard_excel_export(self):
        """Excel export must return an act_url action with a populated XLSX binary."""
        mo = self._make_mo(product_qty=5.0)
        self._mark_done(mo, 3.0)
        self.env.flush_all()

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'all',
            'variance_filter': 'all',
            'product_ids': [(6, 0, [self.product.id])],
        })
        action = wizard.action_export_xlsx()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertTrue(wizard.xlsx_file, "xlsx_file binary must not be empty.")
        # A valid XLSX (ZIP) file starts with the PK magic bytes.
        raw = base64.b64decode(wizard.xlsx_file)
        self.assertTrue(raw[:2] == b'PK',
                        "xlsx_file must be a valid XLSX/ZIP archive.")

    # ------------------------------------------------------------------
    # 14.  Wizard: action_open_view returns a filtered window action
    # ------------------------------------------------------------------
    def test_wizard_action_open_view(self):
        """action_open_view must return an act_window with the wizard's domain applied."""
        mo = self._make_mo(product_qty=5.0)
        self._mark_done(mo, 5.0)
        self.env.flush_all()

        wizard = self.env['coa.production.variance.wizard'].create({
            'state_filter': 'done',
            'variance_filter': 'all',
            'product_ids': [(6, 0, [self.product.id])],
        })
        action = wizard.action_open_view()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'coa.mfg.production.variance')
        self.assertIn(('state', '=', 'done'), action['domain'])
        self.assertIn(('product_id', 'in', [self.product.id]), action['domain'])
