# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpBomLine(models.Model):
    """
    بنضيف على BOM line:
    - حقل source location بيورث من الكاتجوري تلقائياً
    - ممكن يتغير يدوياً على كل component
    """
    _inherit = 'mrp.bom.line'

    # لوكيشن المصدر للـ component ده في الـ BOM
    source_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن السحب',
        domain=[('usage', '=', 'internal')],
        help='اللوكيشن اللي هيتسحب منه الـ component ده أثناء التصنيع.\n'
             'بيورث تلقائياً من كاتجوري الصنف، وممكن تغيره يدوياً.',
        compute='_compute_source_location',
        store=True,
        readonly=False,
    )

    # لتتبع إذا كان المستخدم عدّله يدوياً
    source_location_manual = fields.Boolean(
        'لوكيشن يدوي؟',
        default=False,
        help='لو True، مش هيتعدّل تلقائياً من الكاتجوري.',
    )

    category_source_location_id = fields.Many2one(
        'stock.location',
        string='لوكيشن الكاتجوري (للعرض)',
        related='product_id.categ_id.mfg_source_location_id',
        readonly=True,
    )

    @api.depends('product_id', 'product_id.categ_id', 'product_id.categ_id.mfg_source_location_id')
    def _compute_source_location(self):
        for line in self:
            # لو المستخدم عدّل يدوياً، ما تتغيرش
            if line.source_location_manual and line.source_location_id:
                continue
            # ورّث من الكاتجوري
            if line.product_id and line.product_id.categ_id.mfg_source_location_id:
                line.source_location_id = line.product_id.categ_id.mfg_source_location_id
            else:
                line.source_location_id = False

    @api.onchange('source_location_id')
    def _onchange_source_location_manual(self):
        """لما المستخدم يغير اللوكيشن يدوياً، نفلّغ العلم"""
        # لو اتغير عن قيمة الكاتجوري → manual
        category_loc = self.product_id.categ_id.mfg_source_location_id if self.product_id else False
        if self.source_location_id and self.source_location_id != category_loc:
            self.source_location_manual = True
        elif not self.source_location_id:
            self.source_location_manual = False

    def action_reset_to_category_location(self):
        """زر: إرجع لوكيشن الكاتجوري"""
        for line in self:
            line.source_location_manual = False
            line._compute_source_location()


class MrpBom(models.Model):
    """
    بنضيف على BOM نفسه:
    - زر لإعادة ضبط كل لوكيشنات الـ components من الكاتجوري
    - عرض ملخص اللوكيشنات
    """
    _inherit = 'mrp.bom'

    has_multi_location_components = fields.Boolean(
        'مكونات من لوكيشنات متعددة؟',
        compute='_compute_has_multi_location',
    )

    unique_source_locations = fields.Char(
        'اللوكيشنات المستخدمة',
        compute='_compute_has_multi_location',
    )

    @api.depends('bom_line_ids.source_location_id')
    def _compute_has_multi_location(self):
        for bom in self:
            locs = bom.bom_line_ids.mapped('source_location_id')
            bom.has_multi_location_components = len(locs) > 1
            if locs:
                bom.unique_source_locations = ' | '.join(locs.mapped('complete_name'))
            else:
                bom.unique_source_locations = 'الافتراضي'

    def action_sync_bom_locations(self):
        """إعادة ضبط كل لوكيشنات الـ BOM من الكاتجوري"""
        for bom in self:
            for line in bom.bom_line_ids:
                line.source_location_manual = False
            bom.bom_line_ids._compute_source_location()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'تم',
                'message': 'تم تحديث لوكيشنات كل المكونات من الكاتجوري.',
                'type': 'success',
                'sticky': False,
            }
        }


class MrpProductionInherit(models.Model):
    """
    بنعدّل أمر التصنيع عشان يستخدم لوكيشنات الكاتجوري.

    مراحل التصنيع:
    - 1 مرحلة  (mrp_one_step): المكونات تتسحب مباشرة في move_raw_ids
    - 2 مراحل  (pbm):         Pick → Manufacture
    - 3 مراحل  (pbm_sam):     Pick → Manufacture → Store

    في 2/3 مراحل: اللوكيشن الصح هو على Pick picking (pbm_type_id)
    مش على move_raw_ids اللي بتبدأ من Pre-Production.
    """
    _inherit = 'mrp.production'

    def action_confirm(self):
        """
        بنطبق اللوكيشنات بعد الـ confirm عشان Pick pickings تكون اتعملت.
        """
        res = super().action_confirm()
        for production in self:
            production._apply_bom_component_locations()
        return res

    def _apply_bom_component_locations(self):
        """
        يطبق لوكيشن الكاتجوري (أو BOM line) على الـ moves الصح:
        - 1 مرحلة  → move_raw_ids مباشرة
        - 2/3 مراحل → moves الـ Pick picking (pbm_type_id)
        """
        self.ensure_one()
        wh = self.warehouse_id
        is_multi_step = wh and wh.manufacture_steps in ('pbm', 'pbm_sam')

        # خريطة: product_id → source_location من BOM line (فاضية لو مفيش BOM)
        bom_line_map = {}
        if self.bom_id:
            bom_line_map = {
                line.product_id.id: line.source_location_id
                for line in self.bom_id.bom_line_ids
                if line.source_location_id
            }

        def _get_source_loc(move):
            """Priority: BOM line location > Category location"""
            loc = bom_line_map.get(move.product_id.id)
            if not loc:
                loc = move.product_id.categ_id.mfg_source_location_id
            return loc

        if is_multi_step:
            # ── 2/3 مراحل: عدّل Pick picking moves ──────────────────────
            pick_pickings = self.picking_ids.filtered(
                lambda p: p.picking_type_id == wh.pbm_type_id
                and p.state not in ('done', 'cancel')
            )
            for move in pick_pickings.move_ids:
                source_loc = _get_source_loc(move)
                if source_loc:
                    move.location_id = source_loc
            # حدّث لوكيشن الـ picking header لو كل moves من نفس المكان
            for picking in pick_pickings:
                locs = picking.move_ids.mapped('location_id')
                if len(locs) == 1:
                    picking.location_id = locs
        else:
            # ── 1 مرحلة: عدّل move_raw_ids مباشرة ───────────────────────
            for move in self.move_raw_ids:
                source_loc = _get_source_loc(move)
                if source_loc:
                    move.location_id = source_loc

    def write(self, vals):
        res = super().write(vals)
        # لو الـ BOM اتغير بعد الـ confirm، حدّث اللوكيشنات
        if 'bom_id' in vals:
            for production in self.filtered(
                lambda p: p.state in ('confirmed', 'progress')
            ):
                production._apply_bom_component_locations()
        return res
