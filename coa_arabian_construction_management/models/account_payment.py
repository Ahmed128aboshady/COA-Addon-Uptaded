# -*- coding: utf-8 -*-
""" Account Payment """
from odoo import api, fields, models, _

class AccountPayment(models.Model):
    """ inherit Account Payment """
    _inherit = 'account.payment'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',string="Business Item")