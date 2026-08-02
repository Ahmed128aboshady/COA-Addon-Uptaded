# -*- coding: utf-8 -*-
""" Stock Picking """
from odoo import api, fields, models, _

class StockPicking(models.Model):
    """ inherit Stock Picking """
    _inherit = 'stock.picking'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line')
    project_id = fields.Many2one('project.project')
    project_task_id = fields.Many2one('project.task')



    

