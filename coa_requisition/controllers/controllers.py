# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianRequisition(http.Controller):
#     @http.route('/arabian_requisition/arabian_requisition', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_requisition/arabian_requisition/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arabian_requisition.listing', {
#             'root': '/arabian_requisition/arabian_requisition',
#             'objects': http.request.env['arabian_requisition.arabian_requisition'].search([]),
#         })

#     @http.route('/arabian_requisition/arabian_requisition/objects/<model("arabian_requisition.arabian_requisition"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arabian_requisition.object', {
#             'object': obj
#         })

