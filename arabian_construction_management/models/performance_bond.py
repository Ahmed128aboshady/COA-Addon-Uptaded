# -*- coding: utf-8 -*-
""" Performance Bond """
from odoo import api, fields, models, _

class LgPerformanceBond(models.Model):
    """ inherit Lg Performance Bond """
    _inherit = 'lg.performance.bond'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
