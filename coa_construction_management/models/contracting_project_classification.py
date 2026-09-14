# -*- coding: utf-8 -*-
""" Contracting Project Classification """
from odoo import api, fields, models, _
from random import randint


class ContractingProjectClassification(models.Model):
    """ Contracting Project Classification """
    _name = 'contracting.project.classification'
    _description = 'Contracting Project Classification'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    description = fields.Html(translate=True)
    color = fields.Integer(default=_default_color)

