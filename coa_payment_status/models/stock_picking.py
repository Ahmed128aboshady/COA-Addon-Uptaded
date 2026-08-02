from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    payment_status = fields.Selection(
        selection=[
            ('not_invoiced', 'Not Invoiced'),
            ('not_paid', 'Not Paid'),
            ('in_payment', 'In Payment'),
            ('partial', 'Partially Paid'),
            ('paid', 'Paid'),
            ('reversed', 'Reversed'),
        ],
        string='Payment Status',
        compute='_compute_payment_status',
        store=True,
    )

    @api.depends(
        'sale_id.invoice_ids.payment_state',
        'sale_id.invoice_ids.state',
        'purchase_id.invoice_ids.payment_state',
        'purchase_id.invoice_ids.state',
    )
    def _compute_payment_status(self):
        for picking in self:
            # Collect posted invoices from sale or purchase order
            if picking.sale_id:
                invoices = picking.sale_id.invoice_ids.filtered(
                    lambda inv: inv.state == 'posted'
                )
            elif picking.purchase_id:
                invoices = picking.purchase_id.invoice_ids.filtered(
                    lambda inv: inv.state == 'posted'
                )
            else:
                invoices = self.env['account.move']

            if not invoices:
                picking.payment_status = 'not_invoiced'
                continue

            states = invoices.mapped('payment_state')

            if all(s == 'paid' for s in states):
                picking.payment_status = 'paid'
            elif all(s == 'reversed' for s in states):
                picking.payment_status = 'reversed'
            elif 'in_payment' in states:
                picking.payment_status = 'in_payment'
            elif any(s in ('paid', 'partial', 'in_payment') for s in states):
                picking.payment_status = 'partial'
            else:
                picking.payment_status = 'not_paid'
