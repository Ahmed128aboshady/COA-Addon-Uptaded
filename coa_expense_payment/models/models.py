# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class arabian_expense_payment(models.Model):
#     _name = 'arabian_expense_payment.arabian_expense_payment'
#     _description = 'arabian_expense_payment.arabian_expense_payment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
