# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianSoInvoiceReport(http.Controller):
#     @http.route('/arabian_so_invoice_report/arabian_so_invoice_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_so_invoice_report/arabian_so_invoice_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('coa_so_invoice_report.listing', {
#             'root': '/arabian_so_invoice_report/arabian_so_invoice_report',
#             'objects': http.request.env['coa_so_invoice_report.arabian_so_invoice_report'].search([]),
#         })

#     @http.route('/arabian_so_invoice_report/arabian_so_invoice_report/objects/<model("coa_so_invoice_report.arabian_so_invoice_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('coa_so_invoice_report.object', {
#             'object': obj
#         })

