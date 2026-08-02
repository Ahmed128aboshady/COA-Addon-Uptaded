# -*- coding: utf-8 -*-
""" Project Task """
from odoo import api, fields, models, _

class ProjectTask(models.Model):
    """ inherit Project Task """
    _inherit = 'project.task'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    project_manager_id = fields.Many2one('hr.employee', string="Project Manager")
    boq_cost_estimation_id = fields.Many2one('boq.cost.estimation')
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    description = fields.Text(translate=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float(default=1)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',string="Business Item")
    allocated_hours = fields.Float(string="Allocated Hours", digits=(16, 0))
    effective_hours = fields.Float( digits=(16, 0))
    remaining_hours = fields.Float( digits=(16, 0))


class AccountAnalyticLine(models.Model):
    """ inherit Project Task """
    _inherit = 'account.analytic.line'

    unit_amount = fields.Float( digits=(16, 0))