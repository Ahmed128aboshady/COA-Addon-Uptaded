from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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

    @api.depends('partner_id', 'amount_total')
    def _compute_partner_balance(self):
        for order in self:
            if order.partner_id:
                # الحصول على الشريك التجاري الرئيسي
                commercial_partner = order.partner_id.commercial_partner_id

                # الرصيد السابق = مجموع (مدين - دائن) من قيود حساب المدينين
                move_lines = self.env['account.move.line'].search([
                    ('partner_id', '=', commercial_partner.id),
                    ('account_id.account_type', '=', 'asset_receivable'),
                    ('parent_state', '=', 'posted'),
                ])
                previous_balance = sum(move_lines.mapped('debit')) - sum(move_lines.mapped('credit'))

                # الرصيد الحالي = السابق + الطلب الحالي
                current_balance = previous_balance + order.amount_total

                order.partner_previous_balance = previous_balance
                order.partner_current_balance = current_balance
            else:
                order.partner_previous_balance = 0.0
                order.partner_current_balance = 0.0
