# -*- coding: utf-8 -*-
""" Construction Requisition """
from odoo import api, fields, models, _


class ConstructionRequisition(models.Model):
    """ inherit Construction Requisition """
    _inherit = 'construction.requisition'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_id = fields.Many2one('project.project')
    project_task_id = fields.Many2one('project.task')
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',
                                                  string="Business Item")

    @api.onchange('construction_project_id')
    def _onchange_construction_project_id(self):
        """ construction_project_id """
        if self.construction_project_id:
            project=self.env['project.project'].search(
                [('construction_project_id', '=', self.construction_project_id.id)],limit=1)
            if project:
                self.project_id = project.id
        self.project_name = self.construction_project_id.project_number
        self.project_number = self.construction_project_id.project_name

