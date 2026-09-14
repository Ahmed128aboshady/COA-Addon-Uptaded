# -*- coding: utf-8 -*-
""" Purchase Order """
from odoo import fields, models, api
from odoo.tools.query import Query
from odoo.tools.sql import SQL


class PurchaseOrder(models.Model):
    """ inherit Purchase Order """
    _inherit = 'purchase.order'

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

    @api.onchange('construction_project_id')
    def _onchange_construction_project(self):
        """ construction_project_id """
        for rec in self:
            if rec.construction_project_id:
                rec.project_name=rec.construction_project_id.project_name
                rec.project_number=rec.construction_project_id.project_number

# class PurchaseReport(models.Model):
#     _inherit = 'purchase.report'
#
#     detailed_boq_id = fields.Many2one('detailed.bill.of.quantities', string="Detailed BOQ", readonly=True,store=True)
#
#     def _select(self) -> SQL:
#         return SQL(
#             """
#                 SELECT
#                     po.id as order_id,
#                     min(l.id) as id,
#                     po.date_order as date_order,
#                     po.state,
#                     po.date_approve,
#                     po.dest_address_id,
#                     po.partner_id as partner_id,
#                     po.detailed_boq_id as detailed_boq_id,
#                     po.user_id as user_id,
#                     po.company_id as company_id,
#                     po.fiscal_position_id as fiscal_position_id,
#                     l.product_id,
#                     p.product_tmpl_id,
#                     t.categ_id as category_id,
#                     c.currency_id,
#                     t.uom_id as product_uom,
#                     extract(epoch from age(po.date_approve,po.date_order))/(24*60*60)::decimal(16,2) as delay,
#                     extract(epoch from age(l.date_planned,po.date_order))/(24*60*60)::decimal(16,2) as delay_pass,
#                     count(*) as nbr_lines,
#                     sum(l.price_total / COALESCE(po.currency_rate, 1.0))::decimal(16,2) * account_currency_table.rate as price_total,
#                     (sum(l.product_qty * l.price_unit / COALESCE(po.currency_rate, 1.0))/NULLIF(sum(l.product_qty/line_uom.factor*product_uom.factor),0.0))::decimal(16,2) * account_currency_table.rate as price_average,
#                     partner.country_id as country_id,
#                     partner.commercial_partner_id as commercial_partner_id,
#                     sum(p.weight * l.product_qty/line_uom.factor*product_uom.factor) as weight,
#                     sum(p.volume * l.product_qty/line_uom.factor*product_uom.factor) as volume,
#                     sum(l.price_subtotal / COALESCE(po.currency_rate, 1.0))::decimal(16,2) * account_currency_table.rate as untaxed_total,
#                     sum(l.product_qty / line_uom.factor * product_uom.factor) as qty_ordered,
#                     sum(l.qty_received / line_uom.factor * product_uom.factor) as qty_received,
#                     sum(l.qty_invoiced / line_uom.factor * product_uom.factor) as qty_billed,
#                     case when t.purchase_method = 'purchase'
#                          then sum(l.product_qty / line_uom.factor * product_uom.factor) - sum(l.qty_invoiced / line_uom.factor * product_uom.factor)
#                          else sum(l.qty_received / line_uom.factor * product_uom.factor) - sum(l.qty_invoiced / line_uom.factor * product_uom.factor)
#                     end as qty_to_be_billed
#             """,
#         )
#
#     def _from(self) -> SQL:
#         return SQL(
#             """
#             FROM
#             purchase_order_line l
#                 join purchase_order po on (l.order_id=po.id)
#                 join res_partner partner on po.partner_id = partner.id
#                     left join product_product p on (l.product_id=p.id)
#                         left join product_template t on (p.product_tmpl_id=t.id)
#                 left join res_company C ON C.id = po.company_id
#                 left join uom_uom line_uom on (line_uom.id=l.product_uom)
#                 left join uom_uom product_uom on (product_uom.id=t.uom_id)
#                 left join %(currency_table)s ON account_currency_table.company_id = po.company_id
#             """,
#             currency_table=self.env['res.currency']._get_simple_currency_table(self.env.companies),
#         )
#
#
#     def _group_by(self) -> SQL:
#         return SQL(
#             """
#             GROUP BY
#                 po.company_id,
#                 po.user_id,
#                 po.partner_id,
#                 po.detailed_boq_id,
#                 line_uom.factor,
#                 c.currency_id,
#                 l.price_unit,
#                 po.date_approve,
#                 l.date_planned,
#                 l.product_uom,
#                 po.dest_address_id,
#                 po.fiscal_position_id,
#                 l.product_id,
#                 p.product_tmpl_id,
#                 t.categ_id,
#                 po.date_order,
#                 po.state,
#                 line_uom.uom_type,
#                 line_uom.category_id,
#                 t.uom_id,
#                 t.purchase_method,
#                 line_uom.id,
#                 product_uom.factor,
#                 partner.country_id,
#                 partner.commercial_partner_id,
#                 po.id,
#                 account_currency_table.rate
#             """,
#         )


class PurchaseOrderLine(models.Model):
    """ inherit Purchase Order Line """
    _inherit = 'purchase.order.line'

    construction_project_id = fields.Many2one('construction.project',related='order_id.construction_project_id', store=True)
    project_name = fields.Char(translate=True,related='order_id.project_name', store=True)
    project_number = fields.Char(translate=True,related='order_id.project_number', store=True)
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',related='order_id.boq_cost_estimation_line_id', store=True)

    project_id = fields.Many2one('project.project',related='order_id.project_id', store=True)
    project_task_id = fields.Many2one('project.task',related='order_id.project_task_id', store=True)
    detailed_boq_id = fields.Many2one(
        'detailed.bill.of.quantities',
        string="Detailed BOQ" ,related='order_id.detailed_boq_id', store=True
    )






