# -*- coding: utf-8 -*-
""" Project Project """
from odoo import api, fields, models, _

class ProjectProject(models.Model):
    """ inherit Project Project """
    _inherit = 'project.project'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    project_manager_id = fields.Many2one('hr.employee', string="Project Manager")
