# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianLettersOfGuarantee(http.Controller):
#     @http.route('/arabian_letters_of_guarantee/arabian_letters_of_guarantee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_letters_of_guarantee/arabian_letters_of_guarantee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arabian_letters_of_guarantee.listing', {
#             'root': '/arabian_letters_of_guarantee/arabian_letters_of_guarantee',
#             'objects': http.request.env['arabian_letters_of_guarantee.arabian_letters_of_guarantee'].search([]),
#         })

#     @http.route('/arabian_letters_of_guarantee/arabian_letters_of_guarantee/objects/<model("arabian_letters_of_guarantee.arabian_letters_of_guarantee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arabian_letters_of_guarantee.object', {
#             'object': obj
#         })

