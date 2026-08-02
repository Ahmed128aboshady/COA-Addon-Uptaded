# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from psycopg2 import errors as pg_errors


class StockRuleAuto(models.Model):
    """
    بنضيف على stock.rule:
    - ربط بالكاتجوري
    - نوع الـ rule (مصدرها إيه)
    - منطق الـ pull مع مراعاة الكاتجوري
    """
    _inherit = 'stock.rule'

    category_id = fields.Many2one(
        'product.category',
        string='الكاتجوري',
        index=True,
        ondelete='cascade',
        help='الكاتجوري اللي اتعملت منها الـ rule دي تلقائياً.',
    )

    rule_type = fields.Selection([
        ('mto_mfg',          'MTO - تصنيع'),
        ('mto_custom',       'MTO - لوكيشن مخصص'),
        ('buy_to_loc',       'BUY → لوكيشن الكاتجوري'),
        ('sale_delivery',    'بيع - تسليم'),
        ('purchase_receipt', 'شراء - استلام'),
        ('customer_return',  'مرتجع عميل'),
        ('manual',           'يدوي'),
    ], string='نوع الـ Rule', default='manual')

    # لوكيشنات التصنيع بتتعدّل في mrp.production.action_confirm
    # مش هنا — عشان منتدخلش في الـ procurement system

    def unlink(self):
        """
        لو فيه stock.move مرتبطة بالـ rule دي، بنعمل archive بدل delete
        عشان نتجنب FK constraint violation.
        بنستخدم savepoint عشان الـ transaction تفضل clean بعد الـ failure.
        """
        try:
            with self.env.cr.savepoint():
                return super().unlink()
        except Exception as e:
            err_str = str(e)
            if 'stock_move_rule_id_fkey' in err_str or 'rule_id' in err_str:
                # الـ savepoint اترجع تلقائياً — الـ cursor نضيف دلوقتي
                self.write({'active': False})
                return True
            raise


class StockRouteInherit(models.Model):
    """
    Override unlink على stock.route عشان لو فيه stock.move مرتبطة
    بأي rule فيها، نعمل archive بدل delete.
    """
    _inherit = 'stock.route'

    def unlink(self):
        """
        Archive الـ route ولو مش قادر يمسح بسبب FK على rules.
        """
        try:
            with self.env.cr.savepoint():
                return super().unlink()
        except Exception as e:
            err_str = str(e)
            if 'stock_move_rule_id_fkey' in err_str or 'rule_id' in err_str:
                self.write({'active': False})
                return True
            raise


class StockPickingInherit(models.Model):
    """
    بنعدّل الـ picking عشان يستخدم لوكيشن الكاتجوري في البيع والمرتجعات
    """
    _inherit = 'stock.picking'

    def _get_default_source_location_for_category(self, product, picking_type_code):
        """
        بيرجع الـ source location المناسبة للصنف حسب نوع العملية.
        """
        category = product.categ_id
        if not category:
            return False

        if picking_type_code == 'outgoing' and category.sale_source_location_id:
            return category.sale_source_location_id
        elif picking_type_code == 'incoming' and category.purchase_dest_location_id:
            return category.purchase_dest_location_id
        elif picking_type_code == 'incoming' and category.return_location_id:
            # للمرتجعات - بنحدد بناءً على origin الـ picking
            if self.origin and 'Return' in self.origin:
                return category.return_location_id
        return False


class StockMoveInherit(models.Model):
    """
    بنعدّل الـ stock move عشان يورث لوكيشن الكاتجوري تلقائياً
    """
    _inherit = 'stock.move'

    def _apply_category_location(self):
        """
        بيطبق لوكيشن الكاتجوري على كل move حسب نوع العملية.
        بيتستدعى من onchange ومن create.
        """
        for move in self:
            if not move.product_id or not move.picking_type_id:
                continue

            category = move.product_id.categ_id
            if not category:
                continue

            picking_type_code = move.picking_type_id.code

            if picking_type_code == 'outgoing' and category.sale_source_location_id:
                # بيع عادي (MTS) — اسحب من لوكيشن الكاتجوري
                # MTO بيشتغل عن طريق الـ procurement rules تلقائياً (زي MTO الأصلي)
                move.location_id = category.sale_source_location_id

            elif picking_type_code == 'incoming':
                # كشف المرتجع بشكل موثوق: مصدره customer location (مش بالـ origin string)
                is_return = (
                    move.location_id and move.location_id.usage == 'customer'
                )
                if is_return:
                    if category.return_location_id:
                        move.location_dest_id = category.return_location_id
                elif category.purchase_dest_location_id:
                    move.location_dest_id = category.purchase_dest_location_id

            elif picking_type_code == 'internal':
                # Pick مرحلة التصنيع
                if category.mfg_source_location_id:
                    move.location_id = category.mfg_source_location_id

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        # نطبق فقط على outgoing / incoming — التصنيع بيتعالج من action_confirm
        moves.filtered(
            lambda m: m.picking_type_id and m.picking_type_id.code in ('outgoing', 'incoming')
        )._apply_category_location()
        return moves
