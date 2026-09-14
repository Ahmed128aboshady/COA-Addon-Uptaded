from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class MrpComponentCorrectionWizard(models.TransientModel):
    _name = 'mrp.component.correction.wizard'
    _description = 'Wizard تصحيح كميات مكونات التصنيع'

    production_id = fields.Many2one(
        'mrp.production',
        string='أمر التصنيع',
        required=True,
        readonly=True,
    )
    line_ids = fields.One2many(
        'mrp.component.correction.wizard.line',
        'wizard_id',
        string='المكونات',
    )

    def action_confirm_correction(self):
        """تنفيذ التصحيح: إرجاع الفرق للمخزن وتصحيح التكلفة"""
        self.ensure_one()

        lines_to_correct = self.line_ids.filtered(
            lambda l: l.corrected_qty < l.consumed_qty
        )

        if not lines_to_correct:
            raise UserError(_('لا يوجد فرق في الكميات يستوجب التصحيح.\nتأكد أن الكمية المصححة أقل من الكمية المصروفة.'))

        for line in lines_to_correct:
            if line.corrected_qty < 0:
                raise UserError(_('الكمية المصححة لـ %s لا يمكن أن تكون سالبة.') % line.product_id.display_name)

            diff_qty = line.consumed_qty - line.corrected_qty
            _logger.info(
                'MFG Correction: MO=%s | Product=%s | Consumed=%s | Corrected=%s | Diff=%s',
                self.production_id.name,
                line.product_id.display_name,
                line.consumed_qty,
                line.corrected_qty,
                diff_qty,
            )
            # 1) إنشاء حركة مرتجع للمخزن (تُعيد المخزون الفعلي وتصحح قيد المحاسبة للمنتجات المخزنية)
            self._create_return_picking(line, diff_qty)
            # 2) تعديل كمية الحركة الأصلية في أمر التصنيع لتعكس الكمية الصحيحة
            self._update_original_move_qty(line)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('تم التصحيح بنجاح'),
                'message': _('تم إرجاع الكميات الزائدة للمخزن وتصحيح التكلفة.'),
                'type': 'success',
                'sticky': False,
            }
        }

    def _create_return_picking(self, line, diff_qty):
        """إنشاء Return Picking لإرجاع الفرق للمخزن الأصلي"""
        # موقع الإنتاج (مصدر الإرجاع) → المخزن الأصلي (وجهة الإرجاع)
        src_location = line.location_id      # موقع الإنتاج
        dest_location = line.location_src_id  # المخزن الأصلي

        picking_type = self._get_return_picking_type(dest_location)

        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': src_location.id,
            'location_dest_id': dest_location.id,
            'origin': _('تصحيح تصنيع: %s') % self.production_id.name,
        })

        move = self.env['stock.move'].create({
            'description_picking_manual': _('إرجاع: %s') % line.product_id.display_name,
            'product_id': line.product_id.id,
            'product_uom_qty': diff_qty,
            'product_uom': line.product_uom_id.id,
            'picking_id': picking.id,
            'location_id': src_location.id,
            'location_dest_id': dest_location.id,
            'origin': self.production_id.name,
            'origin_returned_move_id': line.move_id.id,
        })

        # تأكيد الـ picking (يؤكد الـ moves المرتبطة تلقائياً)
        picking.action_confirm()

        # إنشاء move lines يدوياً (موقع الإنتاج virtual لا يحتوي على مخزون فعلي)
        # picked=True ضروري في Odoo 19 حتى لا يتم إلغاء الحركة في _action_done
        if not move.move_line_ids:
            self.env['stock.move.line'].create({
                'move_id': move.id,
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom_id.id,
                'quantity': diff_qty,
                'location_id': src_location.id,
                'location_dest_id': dest_location.id,
                'picked': True,
            })
        else:
            for ml in move.move_line_ids:
                ml.quantity = diff_qty
                ml.picked = True

        # التحقق بدون إنشاء بادون (cancel_backorder يمنع ظهور مربع حوار البادون)
        picking.with_context(cancel_backorder=True)._action_done()

        _logger.info(
            'Return Picking Created: %s | Move: %s',
            picking.name,
            move.reference,
        )

        return picking

    def _update_original_move_qty(self, line):
        """تحديث كمية الحركة الأصلية في أمر التصنيع لتعكس الكمية الصحيحة"""
        move = line.move_id.sudo()
        corrected_qty = line.corrected_qty

        # تحديث كميات move lines بحيث يعكس المجموع الكمية المصححة
        total_in_lines = sum(move.move_line_ids.mapped('quantity'))
        if total_in_lines > 0:
            ratio = corrected_qty / total_in_lines
            for ml in move.move_line_ids:
                ml.quantity = ml.quantity * ratio
        else:
            # لا توجد move lines، نضيف واحدة بالكمية المصححة
            self.env['stock.move.line'].sudo().create({
                'move_id': move.id,
                'product_id': move.product_id.id,
                'product_uom_id': move.product_uom.id,
                'quantity': corrected_qty,
                'location_id': move.location_id.id,
                'location_dest_id': move.location_dest_id.id,
                'picked': True,
            })

        # تحديث الكمية على الحركة نفسها (product_uom_qty = الكمية المطلوبة)
        move.write({
            'product_uom_qty': corrected_qty,
        })

        _logger.info(
            'Updated original move qty: MO=%s | Product=%s | New qty=%s',
            self.production_id.name,
            line.product_id.display_name,
            corrected_qty,
        )

    def _get_return_picking_type(self, dest_location):
        """إيجاد نوع الـ Picking المناسب للإرجاع"""
        # البحث عن Internal Transfer type في نفس الـ warehouse
        warehouse = self.env['stock.warehouse'].search(
            [('lot_stock_id', 'parent_of', dest_location.id)],
            limit=1
        )

        if warehouse:
            return warehouse.int_type_id

        # fallback: أي internal type
        picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'internal')],
            limit=1
        )

        if not picking_type:
            raise UserError(_('لم يتم العثور على نوع عملية مخزنية مناسب للإرجاع.'))

        return picking_type


class MrpComponentCorrectionWizardLine(models.TransientModel):
    _name = 'mrp.component.correction.wizard.line'
    _description = 'سطر تصحيح مكون التصنيع'

    wizard_id = fields.Many2one(
        'mrp.component.correction.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string='المنتج',
        required=True,
        readonly=True,
    )
    product_uom_id = fields.Many2one(
        'uom.uom',
        string='وحدة القياس',
        readonly=True,
    )
    move_id = fields.Many2one(
        'stock.move',
        string='حركة المخزن الأصلية',
        readonly=True,
    )
    location_id = fields.Many2one(
        'stock.location',
        string='موقع الإنتاج',
        readonly=True,
    )
    location_src_id = fields.Many2one(
        'stock.location',
        string='المخزن الأصلي',
        readonly=True,
    )
    consumed_qty = fields.Float(
        string='الكمية المصروفة',
        readonly=True,
        digits='Product Unit of Measure',
    )
    corrected_qty = fields.Float(
        string='الكمية الفعلية المستخدمة',
        digits='Product Unit of Measure',
    )
    diff_qty = fields.Float(
        string='الفارق (يُرجع للمخزن)',
        compute='_compute_diff_qty',
        digits='Product Unit of Measure',
    )

    @api.depends('consumed_qty', 'corrected_qty')
    def _compute_diff_qty(self):
        for line in self:
            line.diff_qty = line.consumed_qty - line.corrected_qty
