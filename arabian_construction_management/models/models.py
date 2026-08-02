# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class arabian_construction_managment(models.Model):
#     _name = 'arabian_construction_managment.arabian_construction_managment'
#     _description = 'arabian_construction_managment.arabian_construction_managment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

