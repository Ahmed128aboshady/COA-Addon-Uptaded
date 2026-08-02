# -*- coding: utf-8 -*-
""" Business Items Types """
from odoo import api, fields, models, _
from random import randint

class BusinessItemsTypes(models.Model):
    """ Business Items Types """
    _name = 'business.items.types'
    _description = 'Business Items Types'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    description = fields.Html()
    color = fields.Integer(default=_default_color)
