# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WizardFixRoutes(models.TransientModel):
    """
    Wizard لتشخيص وإصلاح مشكلة Routes لأصناف محددة أو كل الأصناف
    بيحل مشكلة: "No rule has been found to replenish X in Y"
    """
    _name = 'wizard.fix.routes'
    _description = 'معالج تشخيص وإصلاح Routes'

    mode = fields.Selection([
        ('all_categories', 'كل الكاتجوريات'),
        ('selected_category', 'كاتجوري محددة'),
        ('selected_product', 'صنف محدد'),
    ], string='نطاق الإصلاح', default='selected_product', required=True)

    category_id = fields.Many2one('product.category', string='الكاتجوري')
    product_id = fields.Many2one('product.product', string='الصنف')

    # نتيجة التشخيص
    diagnosis_result = fields.Text('نتيجة التشخيص', readonly=True)
    diagnosed = fields.Boolean(default=False)

    # خيارات الإصلاح
    fix_sale = fields.Boolean('تحديث Rules البيع', default=True)
    fix_return = fields.Boolean('تحديث Rules المرتجعات', default=True)
    fix_purchase = fields.Boolean('تحديث Rules الشراء', default=True)
    fix_bom_locations = fields.Boolean('تحديث لوكيشنات BOM', default=True)

    def action_diagnose(self):
        """تشخيص المشكلة"""
        self.ensure_one()
        lines = []

        if self.mode == 'selected_product' and self.product_id:
            lines = self._diagnose_product(self.product_id)
        elif self.mode == 'selected_category' and self.category_id:
            lines = self._diagnose_category(self.category_id)
        else:
            cats = self.env['product.category'].search([
                '|', ('mfg_source_location_id', '!=', False),
                ('sale_source_location_id', '!=', False),
            ])
            for cat in cats:
                lines.append(f'--- {cat.name} ---')
                lines.extend(self._diagnose_category(cat))

        self.diagnosis_result = '\n'.join(lines)
        self.diagnosed = True
        return {'type': 'ir.actions.act_window', 'res_model': self._name,
                'res_id': self.id, 'view_mode': 'form', 'target': 'new'}

    def _diagnose_product(self, product):
        lines = [f'🔍 تشخيص الصنف: {product.display_name}']
        template = product.product_tmpl_id
        category = product.categ_id

        # فحص الكاتجوري
        lines.append(f'📂 الكاتجوري: {category.name}')
        if category.mfg_source_location_id:
            lines.append(f'✅ لوكيشن التصنيع: {category.mfg_source_location_id.complete_name}')
        else:
            lines.append('❌ لوكيشن التصنيع: غير محدد')

        # فحص الـ routes على الصنف
        product_routes = template.route_ids.mapped('name')
        lines.append(f'🛣️  Routes على الصنف: {", ".join(product_routes) or "لا يوجد"}')

        mto_route = self.env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)

        if mto_route and mto_route not in template.route_ids:
            lines.append('❌ MTO route مش موجودة على الصنف!')
        else:
            lines.append('✅ MTO route موجودة')

        if buy_route and buy_route not in template.route_ids:
            lines.append('❌ BUY route مش موجودة على الصنف!')
        else:
            lines.append('✅ BUY route موجودة')

        # فحص الـ Stock Rules للكاتجوري
        cat_rules = self.env['stock.rule'].search([('category_id', '=', category.id)])
        if cat_rules:
            lines.append(f'✅ Stock Rules للكاتجوري: {len(cat_rules)} rules')
            for r in cat_rules:
                lines.append(f'   → [{r.rule_type}] {r.name}')
        else:
            lines.append('❌ مفيش Stock Rules مخصصة للكاتجوري دي!')

        # فحص المورد
        suppliers = template.seller_ids
        if not suppliers:
            lines.append('⚠️  الصنف مالوش مورد محدد في Vendors - BUY مش هيشتغل!')
        else:
            lines.append(f'✅ الموردين: {", ".join(suppliers.mapped("partner_id.name"))}')

        # التشخيص النهائي
        lines.append('')
        lines.append('--- الحل ---')
        if not category.mfg_source_location_id:
            lines.append('1️⃣  حدد لوكيشن التصنيع في الكاتجوري')
        if mto_route and mto_route not in template.route_ids:
            lines.append('2️⃣  أضف MTO route على الصنف')
        if buy_route and buy_route not in template.route_ids:
            lines.append('3️⃣  أضف BUY route على الصنف')
        if not cat_rules:
            lines.append('4️⃣  اضغط "إصلاح" عشان تعمل Stock Rules للكاتجوري')

        return lines

    def _diagnose_category(self, category):
        lines = [f'📂 الكاتجوري: {category.name}']
        if category.mfg_source_location_id:
            lines.append(f'  ✅ لوكيشن تصنيع: {category.mfg_source_location_id.complete_name}')
        else:
            lines.append('  ❌ لوكيشن تصنيع: غير محدد')

        cat_rules = self.env['stock.rule'].search([('category_id', '=', category.id)])
        lines.append(f'  Rules: {len(cat_rules)}')

        products_count = self.env['product.template'].search_count([('categ_id', '=', category.id)])
        lines.append(f'  أصناف: {products_count}')
        return lines

    def action_fix(self):
        """تنفيذ الإصلاح"""
        self.ensure_one()

        fixed_count = 0

        # تحديد الكاتجوريات المستهدفة
        if self.mode == 'all_categories':
            categories = self.env['product.category'].search([])
            products = self.env['product.product'].search([])
        elif self.mode == 'selected_category' and self.category_id:
            categories = self.category_id
            products = self.env['product.product'].search([('categ_id', '=', self.category_id.id)])
        elif self.mode == 'selected_product' and self.product_id:
            categories = self.product_id.categ_id
            products = self.product_id
        else:
            raise UserError('اختار كاتجوري أو صنف الأول!')

        # 1. تحديث Stock Rules (بيع / مرتجعات / شراء فقط — مش تصنيع)
        for cat in categories:
            if any([self.fix_sale, self.fix_return, self.fix_purchase]):
                cat._sync_stock_rules()
                fixed_count += 1

        # 2. تحديث لوكيشنات BOM
        if self.fix_bom_locations:
            boms = self.env['mrp.bom'].search([
                ('product_tmpl_id.product_variant_ids', 'in', products.ids),
            ])
            for bom in boms:
                bom.action_sync_bom_locations()

        msg = (
            f'تم الإصلاح بنجاح!\n'
            f'✅ كاتجوريات تم تحديثها: {fixed_count}\n'
            f'ℹ️  لوكيشنات التصنيع بتتطبق تلقائياً عند تأكيد أمر التصنيع.'
        )

        self.diagnosis_result = msg
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '✅ تم الإصلاح',
                'message': msg,
                'type': 'success',
                'sticky': True,
            }
        }
