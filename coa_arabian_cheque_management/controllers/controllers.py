# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianChequeManagement(http.Controller):
#     @http.route('/arabian_cheque_management/arabian_cheque_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_cheque_management/arabian_cheque_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arabian_cheque_management.listing', {
#             'root': '/arabian_cheque_management/arabian_cheque_management',
#             'objects': http.request.env['arabian_cheque_management.arabian_cheque_management'].search([]),
#         })

#     @http.route('/arabian_cheque_management/arabian_cheque_management/objects/<model("arabian_cheque_management.arabian_cheque_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arabian_cheque_management.object', {
#             'object': obj
#         })

