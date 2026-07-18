# -*- coding: utf-8 -*-
from markupsafe import Markup

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request

# The standard customer invoice report. Swap to
# 'account.report_invoice_with_payments' if you want payment info printed.
INVOICE_REPORT_REF = 'account.account_invoices'

PRINT_PAGE = Markup("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>%(title)s</title>
    <style>
        html, body { margin: 0; padding: 0; height: 100%%; }
        iframe { display: block; width: 100%%; height: 100%%; border: none; }
    </style>
</head>
<body>
    <iframe id="coa_invoice_pdf" src="%(pdf_url)s"></iframe>
    <script>
        (function () {
            var frame = document.getElementById('coa_invoice_pdf');
            frame.addEventListener('load', function () {
                // Small delay so the browser PDF viewer finishes rendering,
                // then fire the print dialog directly (no download).
                setTimeout(function () {
                    try {
                        frame.focus();
                        frame.contentWindow.print();
                    } catch (e) {
                        window.print();
                    }
                }, 800);
            });
        })();
    </script>
</body>
</html>""")


class CoaSoPrintInvoice(http.Controller):

    def _get_order_and_invoices(self, order_id):
        """Validate access on the SALE ORDER (not the invoice), then return
        its posted customer invoices with sudo.

        This is what grants Sales users the ability to print: if they can
        read the SO, they can print its invoices - nothing else."""
        order = request.env['sale.order'].browse(order_id)
        if not order.exists():
            return None, None
        try:
            order.check_access('read')
        except AccessError:
            return None, None
        invoices = order.sudo().invoice_ids.filtered(
            lambda m: m.move_type in ('out_invoice', 'out_refund')
            and m.state == 'posted'
        )
        return order, invoices

    @http.route('/coa_so_print_invoice/print/<int:order_id>',
                type='http', auth='user')
    def print_page(self, order_id, **kwargs):
        order, invoices = self._get_order_and_invoices(order_id)
        if order is None:
            return request.not_found()
        if not invoices:
            return request.make_response(
                _("No posted invoice found on this Sale Order."),
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
            )
        html = PRINT_PAGE % {
            'title': _("Print Invoice - %s", order.name),
            'pdf_url': '/coa_so_print_invoice/pdf/%s' % order.id,
        }
        return request.make_response(
            html, headers=[('Content-Type', 'text/html; charset=utf-8')]
        )

    @http.route('/coa_so_print_invoice/pdf/<int:order_id>',
                type='http', auth='user')
    def invoice_pdf(self, order_id, **kwargs):
        order, invoices = self._get_order_and_invoices(order_id)
        if order is None or not invoices:
            return request.not_found()
        pdf_content, _dummy = request.env['ir.actions.report'].sudo(
        )._render_qweb_pdf(INVOICE_REPORT_REF, res_ids=invoices.ids)
        filename = '%s_invoices.pdf' % (order.name or 'invoice')
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            # inline => browser PDF viewer, NOT a download
            ('Content-Disposition', 'inline; filename="%s"' % filename),
        ]
        return request.make_response(pdf_content, headers=headers)
