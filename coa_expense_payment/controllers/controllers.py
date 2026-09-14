# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianExpensePayment(http.Controller):
#     @http.route('/arabian_expense_payment/arabian_expense_payment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_expense_payment/arabian_expense_payment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arabian_expense_payment.listing', {
#             'root': '/arabian_expense_payment/arabian_expense_payment',
#             'objects': http.request.env['arabian_expense_payment.arabian_expense_payment'].search([]),
#         })

#     @http.route('/arabian_expense_payment/arabian_expense_payment/objects/<model("arabian_expense_payment.arabian_expense_payment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arabian_expense_payment.object', {
#             'object': obj
#         })
