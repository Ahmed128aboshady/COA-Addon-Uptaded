# -*- coding: utf-8 -*-
# from odoo import http


# class ArabianDigitsNumbers(http.Controller):
#     @http.route('/arabian_digits_numbers/arabian_digits_numbers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/arabian_digits_numbers/arabian_digits_numbers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('arabian_digits_numbers.listing', {
#             'root': '/arabian_digits_numbers/arabian_digits_numbers',
#             'objects': http.request.env['arabian_digits_numbers.arabian_digits_numbers'].search([]),
#         })

#     @http.route('/arabian_digits_numbers/arabian_digits_numbers/objects/<model("arabian_digits_numbers.arabian_digits_numbers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('arabian_digits_numbers.object', {
#             'object': obj
#         })

