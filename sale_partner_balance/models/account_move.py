from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_previous_balance = fields.Monetary(
        string='Previous Balance',
        compute='_compute_partner_balance',
        currency_field='currency_id',
    )
    partner_current_balance = fields.Monetary(
        string='Current Balance',
        compute='_compute_partner_balance',
        currency_field='currency_id',
    )

    @api.depends('partner_id', 'amount_total', 'state', 'move_type')
    def _compute_partner_balance(self):
        for move in self:
            # فقط لفواتير العملاء وإشعارات الدائن
            if move.partner_id and move.move_type in ('out_invoice', 'out_refund'):
                # الحصول على الشريك التجاري الرئيسي
                commercial_partner = move.partner_id.commercial_partner_id

                # الرصيد السابق = مجموع (مدين - دائن) من قيود حساب المدينين
                # مع استثناء قيود الفاتورة الحالية
                move_lines = self.env['account.move.line'].search([
                    ('partner_id', '=', commercial_partner.id),
                    ('account_id.account_type', '=', 'asset_receivable'),
                    ('parent_state', '=', 'posted'),
                    ('move_id', '!=', move.id),  # استثناء الفاتورة الحالية
                ])
                previous_balance = sum(move_lines.mapped('debit')) - sum(move_lines.mapped('credit'))

                # الرصيد الحالي = السابق + الفاتورة الحالية (أو - لإشعار الدائن)
                if move.move_type == 'out_invoice':
                    current_balance = previous_balance + move.amount_total
                else:  # out_refund - إشعار دائن يُخصم
                    current_balance = previous_balance - move.amount_total

                move.partner_previous_balance = previous_balance
                move.partner_current_balance = current_balance
            else:
                move.partner_previous_balance = 0.0
                move.partner_current_balance = 0.0
