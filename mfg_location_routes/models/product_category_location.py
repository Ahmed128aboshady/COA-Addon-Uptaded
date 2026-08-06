# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductCategoryLocation(models.Model):
    """
    بنضيف على الكاتجوري:
    - لوكيشن المصدر في التصنيع (Pick stage)
    - لوكيشن الوجهة بعد التصنيع
    - لوكيشن المصدر في البيع
    - لوكيشن المرتجعات
    - زر لإنشاء الـ stock rules تلقائياً
    """
    _inherit = 'product.category'

    # ============================================================
    # MANUFACTURING LOCATIONS
    # ============================================================
    mfg_source_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن سحب مكونات التصنيع',
        domain=[('usage', '=', 'internal')],
        help='اللوكيشن اللي هيتسحب منه المكونات في مرحلة Pick أثناء التصنيع.\n'
             'لو فاضي، هيستخدم الـ WH/Stock الافتراضي.',
        tracking=True,
    )
    mfg_dest_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن تخزين المنتج النهائي',
        domain=[('usage', '=', 'internal')],
        help='اللوكيشن اللي هيترحل ليه المنتج النهائي بعد التصنيع.\n'
             'لو فاضي، هيستخدم الـ WH/Stock الافتراضي.',
        tracking=True,
    )
    mfg_wip_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن قيد التصنيع (WIP)',
        domain=[('usage', '=', 'internal')],
        help='اللوكيشن اللي هيتحول ليه المواد في مرحلة Production.\n'
             'اختياري - لو مش محدد هيستخدم Virtual Production Location.',
        tracking=True,
    )

    # ============================================================
    # SALES LOCATIONS
    # ============================================================
    sale_source_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن سحب البيع (Make to Stock)',
        domain=[('usage', '=', 'internal')],
        help='اللوكيشن اللي هيتسحب منه الصنف عند البيع العادي (من الرصيد).',
        tracking=True,
    )
    mto_source_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن MTO (Replenish on Order)',
        domain=[('usage', '=', 'internal')],
        help='لوكيشن مخصص للـ MTO — لما تحدده هيتعمل Route تعمل بالظبط زي\n'
             '"Replenish on Order (MTO)" بس هتسحب من اللوكيشن ده مش من WH/Stock.\n'
             'مفيد لو عندك مخزن مخصص للأصناف اللي بتتأمر على الطلب.',
        tracking=True,
    )
    mto_route_id = fields.Many2one(
        'stock.route',
        string='Route MTO المخصصة',
        readonly=True,
        help='الـ Route المخصصة للـ MTO اللي اتعملت تلقائياً للكاتجوري دي.',
    )

    # ============================================================
    # RETURN / RECEIPT LOCATIONS
    # ============================================================
    return_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن مرتجعات المبيعات',
        domain=[('usage', '=', 'internal')],
        help='المخزن اللي هيرجعله الصنف لما العميل يرجعه (Sales Return).\n'
             'بيتطبق تلقائياً على كل أصناف الكاتجوري دي.',
        tracking=True,
    )
    purchase_dest_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن استلام الشراء (Receipt)',
        domain=[('usage', '=', 'internal')],
        help='اللوكيشن اللي هيتخزن فيه الصنف عند استلام أمر الشراء.',
        tracking=True,
    )

    # ============================================================
    # ROUTE CONFIGURATION
    # ============================================================
    auto_create_rules = fields.Boolean(
        string='إنشاء Rules تلقائياً',
        default=True,
        help='لو مفعّل، هيعمل Stock Rules تلقائياً لكل warehouse عند الحفظ.',
    )
    mfg_route_id = fields.Many2one(
        'stock.route',
        string='Route التصنيع المخصصة',
        readonly=True,
        help='الـ Route المخصصة للتصنيع اللي اتعملت تلقائياً للكاتجوري دي.',
    )
    rule_ids = fields.One2many(
        'stock.rule',
        'category_id',
        string='Stock Rules المرتبطة',
    )
    rule_count = fields.Integer(
        'عدد الـ Rules',
        compute='_compute_rule_count',
    )

    def _compute_rule_count(self):
        for rec in self:
            rec.rule_count = len(rec.rule_ids)

    # ============================================================
    # ONCHANGE: تحذير لو اللوكيشن مش صح
    # ============================================================
    @api.onchange('mfg_source_location_id')
    def _onchange_mfg_source_location(self):
        if self.mfg_source_location_id:
            loc = self.mfg_source_location_id
            if loc.usage != 'internal':
                return {
                    'warning': {
                        'title': 'تحذير',
                        'message': 'اللوكيشن المختار مش Internal Location!\nلازم يكون Internal عشان الـ stock moves تشتغل صح.',
                    }
                }

    # ============================================================
    # WRITE: إنشاء rules تلقائياً عند الحفظ
    # ============================================================
    def write(self, vals):
        res = super().write(vals)
        location_fields = {
            'mfg_source_location_id', 'mfg_dest_location_id',
            'sale_source_location_id', 'mto_source_location_id',
            'return_location_id', 'purchase_dest_location_id',
            'auto_create_rules',
        }
        if location_fields.intersection(vals.keys()):
            for rec in self:
                if rec.auto_create_rules:
                    rec._sync_stock_rules()
        return res

    # ============================================================
    # CORE: إنشاء / تحديث Stock Rules
    # ============================================================
    def _sync_stock_rules(self):
        """
        بيعمل أو بيحدّث:
        - Route التصنيع المخصصة (3 rules: Pick → Manufacture → Store)
        - Sale delivery rules
        - Purchase receipt rules
        - Return rules
        """
        self.ensure_one()
        StockRule = self.env['stock.rule']
        warehouses = self.env['stock.warehouse'].search([])

        # Manufacturing: route كاملة بـ 3 rules
        self._create_or_update_mfg_route()

        # MTO: route مخصصة زي "Replenish on Order"
        self._create_or_update_mto_route()

        for wh in warehouses:
            self._create_or_update_sale_rules(wh, StockRule)
            self._create_or_update_purchase_rules(wh, StockRule)
            self._create_or_update_return_rules(wh, StockRule)

    def _create_or_update_mfg_route(self):
        """
        ينشئ أو يحدّث route مخصصة للتصنيع تطابق هيكل:
        "Pick components, manufacture and then store products (3 steps)"
        لكن بلوكيشنات الكاتجوري المخصصة.

        Rules:
          1. Pick:        mfg_source_location_id → Pre-Production  (pull / make_to_stock)
          2. Manufacture: Pre-Production → Production               (pull / make_to_order)
          3. Store:       Post-Production → mfg_dest_location_id   (push / make_to_order)
        """
        self.ensure_one()
        if not self.mfg_source_location_id:
            return

        Route    = self.env['stock.route']
        StockRule = self.env['stock.rule']
        warehouses = self.env['stock.warehouse'].search([])

        route_name = f'{self.name}: تصنيع مخصص (3 مراحل)'

        # ── إنشاء أو تحديث الـ Route ───────────────────────────────
        if self.mfg_route_id:
            route = self.mfg_route_id
            route.name = route_name
        else:
            route = Route.create({
                'name': route_name,
                'product_categ_selectable': True,
                'product_selectable': True,   # تظهر على المنتجات زي MTO
                'warehouse_selectable': False,
                'sequence': 10,
            })
            # اكتب mfg_route_id باستخدام sudo لتجنب أي conflict مع الـ write الحالي
            self.env['product.category'].browse(self.id).write({
                'mfg_route_id': route.id,
            })
            # طبّق الـ route على الكاتجوري
            self.route_ids = [(4, route.id)]

        # ── أنشئ أو حدّث الـ Rules لكل warehouse (update-in-place بدل delete) ──
        src_loc  = self.mfg_source_location_id
        dest_loc = self.mfg_dest_location_id

        prod_loc = self.env['stock.location'].search(
            [('usage', '=', 'production')], limit=1
        )

        for wh in warehouses:
            if wh.manufacture_steps not in ('pbm', 'pbm_sam'):
                continue
            if not wh.pbm_type_id or not wh.pbm_loc_id:
                continue

            wh_dest_loc   = dest_loc or wh.lot_stock_id
            post_prod_loc = wh.sam_loc_id if wh.sam_loc_id else wh.lot_stock_id

            # تعريف كل rule بـ key فريد: (route_id, warehouse_id, sequence)
            rules_spec = [
                # Rule 0: Manufacture Trigger — ينشئ MO تلقائياً
                {
                    'seq': 10,
                    'vals': {
                        'name': f'{wh.code}: Stock (Manufacture - {self.name})',
                        'route_id': route.id,
                        'action': 'manufacture',
                        'procure_method': 'make_to_order',
                        'location_src_id': False,
                        'location_dest_id': wh_dest_loc.id,
                        'picking_type_id': wh.manu_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'manual',
                        'sequence': 10,
                        'active': True,
                    },
                },
                # Rule 1: Pick — من لوكيشن الكاتجوري → Pre-Production
                {
                    'seq': 15,
                    'vals': {
                        'name': f'{wh.code}: {src_loc.name} → Pre-Production',
                        'route_id': route.id,
                        'action': 'pull',
                        'procure_method': 'make_to_order',
                        'location_src_id': src_loc.id,
                        'location_dest_id': wh.pbm_loc_id.id,
                        'picking_type_id': wh.pbm_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'mto_mfg',
                        'sequence': 15,
                        'active': True,
                    },
                },
                # Rule 2: Manufacture — Pre-Production → Production
                {
                    'seq': 20,
                    'vals': {
                        'name': f'{wh.code}: Pre-Production → Production',
                        'route_id': route.id,
                        'action': 'pull',
                        'procure_method': 'make_to_order',
                        'location_src_id': wh.pbm_loc_id.id,
                        'location_dest_id': prod_loc.id if prod_loc else wh.lot_stock_id.id,
                        'picking_type_id': wh.manu_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'manual',
                        'sequence': 20,
                        'active': True,
                    },
                },
                # Rule 3: Store — Post-Production → لوكيشن التخزين
                {
                    'seq': 25,
                    'vals': {
                        'name': f'{wh.code}: Post-Production → {wh_dest_loc.name}',
                        'route_id': route.id,
                        'action': 'push',
                        'procure_method': 'make_to_order',
                        'location_src_id': post_prod_loc.id,
                        'location_dest_id': wh_dest_loc.id,
                        'picking_type_id': wh.sam_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'manual',
                        'sequence': 25,
                        'active': True,
                    },
                },
            ]

            for spec in rules_spec:
                # ابحث في active و archived معاً (active_test=False)
                existing = StockRule.with_context(active_test=False).search([
                    ('route_id', '=', route.id),
                    ('warehouse_id', '=', wh.id),
                    ('sequence', '=', spec['seq']),
                ], limit=1)
                if existing:
                    existing.write(spec['vals'])  # يشمل active=True → يُعيد التفعيل
                else:
                    StockRule.create(spec['vals'])

    def _create_or_update_mto_route(self):
        """
        ينشئ أو يحدّث route تعمل بالظبط زي "Replenish on Order (MTO)"
        بس بدل WH/Stock بنستخدم mto_source_location_id.

        نفس rules الـ MTO الأصلية:
          src → Customers       (Delivery Orders  / pull / make_to_order)
          src → Production      (Manufacturing    / pull / make_to_order)
          src → Pre-Production  (Pick Components  / pull / make_to_order) — لو فيه 3 مراحل

        الـ route بتتضاف على الكاتجوري تلقائياً (product_categ_selectable)
        فكل أصناف الكاتجوري بيورثوها من غير إضافة يدوية.
        """
        self.ensure_one()
        if not self.mto_source_location_id:
            return

        Route    = self.env['stock.route']
        StockRule = self.env['stock.rule']
        warehouses = self.env['stock.warehouse'].search([])

        customer_loc = self.env.ref('stock.stock_location_customers', raise_if_not_found=False)
        if not customer_loc:
            return

        route_name = f'{self.name}: توريد على الطلب - {self.mto_source_location_id.name}'

        # ── إنشاء أو تحديث الـ Route ──────────────────────────────
        if self.mto_route_id:
            route = self.mto_route_id
            route.name = route_name
        else:
            route = Route.create({
                'name': route_name,
                'product_categ_selectable': True,   # تظهر ع الكاتجوري
                'product_selectable':       True,   # تظهر ع المنتج
                'warehouse_selectable':     False,
                'sequence': 5,
            })
            self.env['product.category'].browse(self.id).write({'mto_route_id': route.id})
            self.route_ids = [(4, route.id)]   # تطبيق على الكاتجوري تلقائياً

        src = self.mto_source_location_id

        for wh in warehouses:
            # ── الـ rules التي سنبنيها (seq فريد لكل rule في الـ warehouse) ──
            rules_spec = []

            # Rule 1: src → Customers  (Delivery)
            if wh.out_type_id:
                rules_spec.append({
                    'seq': 20,
                    'vals': {
                        'name': f'{wh.code}: {src.name} → Customers (MTO)',
                        'route_id': route.id,
                        'action': 'pull',
                        'procure_method': 'make_to_order',
                        'location_src_id': src.id,
                        'location_dest_id': customer_loc.id,
                        'picking_type_id': wh.out_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'mto_custom',
                        'sequence': 20,
                        'active': True,
                    },
                })

            # Rule 2: src → Production  (Manufacturing مباشر — 1 مرحلة)
            prod_loc = self.env['stock.location'].search(
                [('usage', '=', 'production')], limit=1
            )
            if wh.manu_type_id and prod_loc:
                rules_spec.append({
                    'seq': 21,
                    'vals': {
                        'name': f'{wh.code}: {src.name} → Production (MTO)',
                        'route_id': route.id,
                        'action': 'pull',
                        'procure_method': 'make_to_order',
                        'location_src_id': src.id,
                        'location_dest_id': prod_loc.id,
                        'picking_type_id': wh.manu_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'mto_custom',
                        'sequence': 21,
                        'active': True,
                    },
                })

            # Rule 3: src → Pre-Production  (Pick Components — 2/3 مراحل)
            if wh.manufacture_steps in ('pbm', 'pbm_sam') and wh.pbm_type_id and wh.pbm_loc_id:
                rules_spec.append({
                    'seq': 22,
                    'vals': {
                        'name': f'{wh.code}: {src.name} → Pre-Production (MTO)',
                        'route_id': route.id,
                        'action': 'pull',
                        'procure_method': 'make_to_order',
                        'location_src_id': src.id,
                        'location_dest_id': wh.pbm_loc_id.id,
                        'picking_type_id': wh.pbm_type_id.id,
                        'warehouse_id': wh.id,
                        'category_id': self.id,
                        'rule_type': 'mto_custom',
                        'sequence': 22,
                        'active': True,
                    },
                })

            # ── update-in-place بدل delete ─────────────────────────
            for spec in rules_spec:
                existing = StockRule.with_context(active_test=False).search([
                    ('route_id', '=', route.id),
                    ('warehouse_id', '=', wh.id),
                    ('sequence', '=', spec['seq']),
                ], limit=1)
                if existing:
                    existing.write(spec['vals'])
                else:
                    StockRule.create(spec['vals'])

    def _create_or_update_mfg_rules(self, wh, StockRule):
        """Kept for compatibility — التصنيع بيتعالج في _create_or_update_mfg_route."""
        return

    def _create_or_update_sale_rules(self, wh, StockRule):
        """Rule للبيع: Delivery من لوكيشن البيع"""
        if not self.sale_source_location_id:
            return

        source_loc = self.sale_source_location_id
        sale_route = wh.route_ids.filtered(lambda r: 'delivery' in r.name.lower() or 'ship' in r.name.lower())[:1]
        if not sale_route:
            sale_route = self.env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
        if not sale_route:
            return

        existing = StockRule.search([
            ('category_id', '=', self.id),
            ('warehouse_id', '=', wh.id),
            ('rule_type', '=', 'sale_delivery'),
        ], limit=1)

        vals = {
            'name': f'[{self.name}] بيع من {source_loc.complete_name}',
            'route_id': sale_route.id,
            'action': 'pull',
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'location_src_id': source_loc.id,
            'warehouse_id': wh.id,
            'category_id': self.id,
            'rule_type': 'sale_delivery',
            'procure_method': 'make_to_stock',
            'picking_type_id': wh.out_type_id.id,
            'sequence': 20,
            'active': True,
        }
        if existing:
            existing.write(vals)
        else:
            StockRule.create(vals)

    def _create_or_update_purchase_rules(self, wh, StockRule):
        """Rule للشراء: استلام في لوكيشن الكاتجوري"""
        if not self.purchase_dest_location_id:
            return

        dest_loc = self.purchase_dest_location_id
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if not buy_route:
            return

        existing = StockRule.search([
            ('category_id', '=', self.id),
            ('warehouse_id', '=', wh.id),
            ('rule_type', '=', 'purchase_receipt'),
        ], limit=1)

        vals = {
            'name': f'[{self.name}] استلام شراء → {dest_loc.complete_name}',
            'route_id': buy_route.id,
            'action': 'pull',
            'location_dest_id': dest_loc.id,
            'location_src_id': self.env.ref('stock.stock_location_suppliers').id,
            'warehouse_id': wh.id,
            'category_id': self.id,
            'rule_type': 'purchase_receipt',
            'procure_method': 'make_to_order',
            'picking_type_id': wh.in_type_id.id,
            'sequence': 15,
            'active': True,
        }
        if existing:
            existing.write(vals)
        else:
            StockRule.create(vals)

    def _create_or_update_return_rules(self, wh, StockRule):
        """Rule للمرتجع: استلام في لوكيشن المرتجعات"""
        if not self.return_location_id:
            return

        return_loc = self.return_location_id
        existing = StockRule.search([
            ('category_id', '=', self.id),
            ('warehouse_id', '=', wh.id),
            ('rule_type', '=', 'customer_return'),
        ], limit=1)

        # Route المرتجعات
        return_route = wh.route_ids.filtered(
            lambda r: 'return' in r.name.lower() or 'مرتجع' in r.name
        )[:1]
        if not return_route:
            return_route = self.env['stock.route'].search([
                ('name', 'ilike', 'return'),
            ], limit=1)
        if not return_route:
            return

        vals = {
            'name': f'[{self.name}] مرتجع → {return_loc.complete_name}',
            'route_id': return_route.id,
            'action': 'pull',
            'location_dest_id': return_loc.id,
            'location_src_id': self.env.ref('stock.stock_location_customers').id,
            'warehouse_id': wh.id,
            'category_id': self.id,
            'rule_type': 'customer_return',
            'procure_method': 'make_to_stock',
            'picking_type_id': wh.in_type_id.id,
            'sequence': 25,
            'active': True,
        }
        if existing:
            existing.write(vals)
        else:
            StockRule.create(vals)

    # ============================================================
    # ACTION BUTTONS
    # ============================================================
    def action_sync_rules(self):
        """زر يدوي لتحديث الـ rules"""
        for rec in self:
            rec._sync_stock_rules()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'تم بنجاح',
                'message': f'تم تحديث Stock Rules للكاتجوري "{self.name}" بنجاح!',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_view_rules(self):
        return {
            'name': f'Stock Rules - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.rule',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }

    def action_delete_rules(self):
        """أرشفة كل Stock Rules والـ Routes المخصصة للكاتجوري دي
        (archive بدل delete عشان stock moves مرتبطة بالـ rules)"""
        for rec in self:
            rules_count = len(rec.rule_ids)
            # أرشفة الـ rules — unlink يفشل لو فيه stock moves مرتبطة
            try:
                rec.rule_ids.unlink()
            except Exception:
                rec.rule_ids.write({'active': False})

            # Route التصنيع
            if rec.mfg_route_id:
                rec.route_ids = [(3, rec.mfg_route_id.id)]
                try:
                    rec.mfg_route_id.unlink()
                except Exception:
                    rec.mfg_route_id.write({'active': False})
                rec.mfg_route_id = False

            # Route MTO
            if rec.mto_route_id:
                rec.route_ids = [(3, rec.mto_route_id.id)]
                try:
                    rec.mto_route_id.unlink()
                except Exception:
                    rec.mto_route_id.write({'active': False})
                rec.mto_route_id = False
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'تم',
                'message': f'تم أرشفة {rules_count} Stock Rule والـ Route المخصصة للكاتجوري "{self.name}".',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_diagnose_routes(self):
        """تشخيص مشكلة الـ routes للكاتجوري دي"""
        self.ensure_one()
        issues = []
        suggestions = []

        # فحص لوكيشن التصنيع
        if not self.mfg_source_location_id:
            issues.append('❌ لوكيشن سحب التصنيع مش محدد')
            suggestions.append('حدد "لوكيشن سحب مكونات التصنيع" في تبويب Locations')
        else:
            issues.append(f'✅ لوكيشن التصنيع: {self.mfg_source_location_id.complete_name}')

        # فحص لوكيشن البيع
        if not self.sale_source_location_id:
            issues.append('⚠️  لوكيشن البيع مش محدد - هيستخدم الافتراضي')
        else:
            issues.append(f'✅ لوكيشن البيع: {self.sale_source_location_id.complete_name}')

        # فحص الـ rules
        if not self.rule_ids:
            issues.append('❌ مفيش Stock Rules متعملة للكاتجوري دي')
            suggestions.append('اضغط زر "تحديث Rules" عشان تعملها تلقائياً')
        else:
            issues.append(f'✅ عدد الـ Rules: {len(self.rule_ids)}')

        # فحص MTO route على الـ rules
        mto_rules = self.rule_ids.filtered(lambda r: r.rule_type == 'mto_mfg')
        buy_rules = self.rule_ids.filtered(lambda r: r.rule_type == 'buy_to_loc')

        if not mto_rules:
            issues.append('❌ مفيش MTO Rule للكاتجوري دي')
        if not buy_rules:
            issues.append('❌ مفيش BUY Rule بيوصل للـ source location')

        # فحص الأصناف في الكاتجوري دي
        products_in_cat = self.env['product.template'].search([('categ_id', '=', self.id)])
        issues.append(f'📦 عدد الأصناف في الكاتجوري: {len(products_in_cat)}')

        # بناء الرسالة
        msg = '\n'.join(issues)
        if suggestions:
            msg += '\n\n--- توصيات ---\n' + '\n'.join(suggestions)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': f'تشخيص Routes - {self.name}',
                'message': msg,
                'type': 'warning' if issues else 'success',
                'sticky': True,
            }
        }
