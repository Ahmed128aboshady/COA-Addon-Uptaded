# -*- coding: utf-8 -*-
""" Construction Project Type """
from odoo import api, fields, models, _
from random import randint


class ConstructionProjectType(models.Model):
    """ Construction Project Type """
    _name = 'construction.project.type'
    _description = 'Construction Project Type'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    description = fields.Html(translate=True)
    color = fields.Integer(default=_default_color)
    contracting_project_classification_id = fields.Many2one('contracting.project.classification')
