from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    stock_location_detail = fields.Char(
        string='Source Location',
        copy=False,
        readonly=True,
    )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        """بعد إنشاء الـ invoice، ننقل الـ location detail للـ invoice lines"""
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for move in moves:
            for inv_line in move.invoice_line_ids:
                sale_line = inv_line.sale_line_ids[:1]
                if sale_line and sale_line.reserved_location_stored:
                    inv_line.stock_location_detail = sale_line.reserved_location_stored
        return moves
