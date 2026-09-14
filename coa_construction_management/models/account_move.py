# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models, _

class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    interim_invoice_id = fields.Many2one('interim.invoice')
    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line')





