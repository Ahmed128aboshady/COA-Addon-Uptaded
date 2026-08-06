from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestAutoSequence(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.categ = cls.env['product.category'].create({'name': 'Zeta Widgets'})

    # ── Products ────────────────────────────────────────────────────────────

    def test_template_form_create(self):
        """Creating from the Products menu (product.template form)."""
        template = self.env['product.template'].create({
            'name': 'From Menu',
            'categ_id': self.categ.id,
        })
        self.assertTrue(template.default_code)
        self.assertEqual(
            template.product_variant_id.default_code, template.default_code)

    def test_template_quick_create_blocked(self):
        """Name-only quick create is refused with a clear message: the user
        must open the full form and pick a category."""
        with self.assertRaises(UserError):
            self.env['product.template'].name_create('Quick Tmpl')

    def test_variant_quick_create_blocked(self):
        """Same for quick create from a product.product popup
        (sale/purchase order line)."""
        with self.assertRaises(UserError):
            self.env['product.product'].name_create('Quick Variant')

    def test_quick_create_with_default_categ(self):
        """Quick create still works when the context provides a category
        (e.g. a view filtered on a category)."""
        pid = self.env['product.product'].with_context(
            default_categ_id=self.categ.id).name_create('Ctx Variant')
        product = self.env['product.product'].browse(pid[0])
        self.assertEqual(product.categ_id, self.categ)
        self.assertTrue(product.default_code)
        self.assertEqual(
            product.product_tmpl_id.default_code, product.default_code)

    def test_variant_full_form_create(self):
        """'Create and edit' popup opening the product.product form."""
        product = self.env['product.product'].create({
            'name': 'Popup Product',
            'categ_id': self.categ.id,
        })
        self.assertTrue(product.default_code)
        self.assertEqual(
            product.product_tmpl_id.default_code, product.default_code)

    def test_manual_code_kept(self):
        template = self.env['product.template'].create({
            'name': 'Manual',
            'categ_id': self.categ.id,
            'default_code': 'MY-CODE',
        })
        self.assertEqual(template.default_code, 'MY-CODE')

    def test_copy_gets_new_code(self):
        template = self.env['product.template'].create({
            'name': 'Original',
            'categ_id': self.categ.id,
        })
        dup = template.copy()
        self.assertTrue(dup.default_code)
        self.assertNotEqual(dup.default_code, template.default_code)

    def test_codes_are_unique_per_categ_sequence(self):
        t1 = self.env['product.template'].create(
            {'name': 'P1', 'categ_id': self.categ.id})
        t2 = self.env['product.template'].create(
            {'name': 'P2', 'categ_id': self.categ.id})
        self.assertNotEqual(t1.default_code, t2.default_code)
        prefix = t1.default_code.rsplit('-', 1)[0]
        self.assertEqual(t2.default_code.rsplit('-', 1)[0], prefix)

    # ── Partners ────────────────────────────────────────────────────────────

    def _seq_prefix(self, code):
        return self.env['ir.sequence'].sudo().search(
            [('code', '=', code)], limit=1).prefix

    def _partner_vals(self, name):
        vals = {'name': name}
        # satisfy tornadoksa_custom_fields' constraint when it is installed
        if 'c_customer_code' in self.env['res.partner']._fields:
            vals['c_customer_code'] = '9990901'
        return vals

    def test_partner_quick_create(self):
        """Quick create from any partner many2one popup."""
        partner = self.env['res.partner'].name_create('Quick Partner')
        partner = self.env['res.partner'].browse(partner[0])
        self.assertTrue(partner.ref)
        self.assertTrue(partner.ref.startswith(self._seq_prefix('res.partner')))

    def test_partner_customer_context(self):
        """Quick create from a customer field (sale order) uses the customer sequence."""
        partner = self.env['res.partner'].with_context(
            res_partner_search_mode='customer').create(
            self._partner_vals('Cust'))
        self.assertTrue(
            partner.ref.startswith(self._seq_prefix('res.partner.customer')))

    def test_partner_vendor_context(self):
        """Quick create from a vendor field (purchase order) uses the vendor sequence."""
        partner = self.env['res.partner'].with_context(
            res_partner_search_mode='supplier').create(
            self._partner_vals('Vend'))
        self.assertTrue(
            partner.ref.startswith(self._seq_prefix('res.partner.vendor')))
