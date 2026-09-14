# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianConstructionManagment(http.Controller):
#     @http.route('/arabian_construction_managment/arabian_construction_managment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_construction_managment/arabian_construction_managment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arabian_construction_managment.listing', {
#             'root': '/arabian_construction_managment/arabian_construction_managment',
#             'objects': http.request.env['arabian_construction_managment.arabian_construction_managment'].search([]),
#         })

#     @http.route('/arabian_construction_managment/arabian_construction_managment/objects/<model("arabian_construction_managment.arabian_construction_managment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arabian_construction_managment.object', {
#             'object': obj
#         })

