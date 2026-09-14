# -*- coding: utf-8 -*-
""" Purchase Report """
from odoo import fields, models, api,_
from odoo.tools.query import Query
from odoo.tools.sql import SQL

class PurchaseReport(models.Model):
    """ inherit Purchase Report """
    _inherit = 'purchase.report'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line')

    project_id = fields.Many2one('project.project')
    project_task_id = fields.Many2one('project.task')
    detailed_boq_id = fields.Many2one(
        'detailed.bill.of.quantities',
        string="Detailed BOQ" , store=True
    )

    def _select(self) -> SQL:
        return SQL(
            """
                %s,
                po.construction_project_id,
                po.project_name,
                po.project_number,
                po.boq_cost_estimation_line_id,
                po.project_id,
                po.project_task_id,
                po.detailed_boq_id
            """, super()._select()
        )




    def _group_by(self) -> SQL:
        return SQL(
            """
                %s,
                po.construction_project_id,
                po.project_name,
                po.project_number,
                po.boq_cost_estimation_line_id,
                po.project_id,
                po.project_task_id,
                po.detailed_boq_id
            """, super()._group_by()
        )


