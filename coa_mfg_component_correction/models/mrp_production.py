from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_open_component_correction(self):
        """فتح Wizard تصحيح المكونات"""
        self.ensure_one()

        if self.state != 'done':
            raise UserError(_('يمكن تصحيح المكونات فقط بعد إتمام أمر التصنيع.'))

        # جمع المكونات المصروفة الفعلية من الـ Stock Moves
        correction_lines = []
        for move in self.move_raw_ids.filtered(lambda m: m.state == 'done' and m.quantity > 0):
            correction_lines.append((0, 0, {
                'product_id': move.product_id.id,
                'product_uom_id': move.product_uom.id,
                'consumed_qty': move.quantity,
                'corrected_qty': move.quantity,
                'move_id': move.id,
                'location_id': move.location_dest_id.id,
                'location_src_id': move.location_id.id,
            }))

        if not correction_lines:
            raise UserError(_('لا توجد مكونات مصروفة لتصحيحها.'))

        wizard = self.env['mrp.component.correction.wizard'].create({
            'production_id': self.id,
            'line_ids': correction_lines,
        })

        return {
            'name': _('تصحيح كميات المكونات'),
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.component.correction.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
