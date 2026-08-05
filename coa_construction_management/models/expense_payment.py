# -*- coding: utf-8 -*-
""" Expense Payment """
from odoo import api, fields, models, _

class ExpensePayment(models.Model):
    """ inherit Expense Payment """
    _inherit = 'expense.payment'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',string="Business Item")