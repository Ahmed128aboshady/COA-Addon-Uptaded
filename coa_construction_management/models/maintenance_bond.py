# -*- coding: utf-8 -*-
""" Maintenance Bond """
from odoo import api, fields, models, _

class LgMaintenanceBond(models.Model):
    """ inherit Lg Maintenance Bond """
    _inherit = 'lg.maintenance.bond'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)



