# -*- coding: utf-8 -*-
""" Subcontractor Attribution Boq """
from odoo import api, fields, models, _


class SubcontractorAttributionBoq(models.TransientModel):
    """ Subcontractor Attribution Boq """
    _name = 'subcontractor.attribution.boq'
    _description = 'Subcontractor Attribution Boq'

    subcontractor_attribution_boq_line_ids = fields.One2many(
        'subcontractor.attribution.boq.line',
        'subcontractor_attribution_boq_id')
    attribution_type = fields.Selection(
        [('complete_boq', 'Complete BOQ'), ('part_boq', 'Part BOQ')],
        default='complete_boq')

    def confirm(self):
        """ Confirm """
        items = []
        active_id = self._context.get('active_id')
        subcontractor = self.env['construction.subcontractor'].browse(active_id)

        for rec in self.subcontractor_attribution_boq_line_ids:
            items.append((0, 0, {
                'construction_business_items_id': rec.construction_business_items_id.id if rec.construction_business_items_id else False,
                'business_item_id': rec.business_item_id.id if rec.business_item_id else False,
                'business_items_types_id': rec.business_items_types_id.id if rec.business_items_types_id else False,
                'product_id': rec.product_id.id if rec.product_id else False,
                'description': rec.description or "No Description",
                'uom_id': rec.uom_id.id if rec.uom_id else False,
                'quantity': rec.quantity or 0.0,
                'rate': rec.rate or 0.0,
                'currency_id': rec.currency_id.id if rec.currency_id else False,
                'total_cost': rec.total_cost or 0.0,
                'boq_cost_estimation_line_id': rec.boq_cost_estimation_line_id.id if rec.boq_cost_estimation_line_id else False,
                'bill_quantities_labour_machines_id': rec.bill_quantities_labour_machines_id.id if rec.bill_quantities_labour_machines_id else False,
                'bill_quantities_overhead_machines_id': rec.bill_quantities_overhead_machines_id.id if rec.bill_quantities_overhead_machines_id else False,
                'bill_quantities_machines_id': rec.bill_quantities_machines_id.id if rec.bill_quantities_machines_id else False,
            }))

        subcontractor.write({
            'construction_subcontractor_lines_ids': items,
            'state': 'attribution_done'
        })


class SubcontractorAttributionBoqLine(models.TransientModel):
    """ Subcontractor Attribution Boq Line """
    _name = 'subcontractor.attribution.boq.line'
    _description = 'Subcontractor Attribution Boq Line'

    subcontractor_attribution_boq_id = fields.Many2one(
        'subcontractor.attribution.boq')
    construction_business_items_id = fields.Many2one(
        'construction.business.items')
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    product_id = fields.Many2one('product.product')
    description = fields.Text(translate=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float(default=1)
    rate = fields.Monetary(currency_field='currency_id', string="Item Price")
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    total_cost = fields.Monetary(currency_field='currency_id',store=True)

    productivity_per_unit_item = fields.Float(
        string="Productivity per unit item/day")
    name = fields.Char(string="Description")
    working_hours = fields.Float()
    unit_price = fields.Monetary(currency_field='currency_id')
    subtotal = fields.Monetary(currency_field='currency_id')
    cost_per_item_unit = fields.Monetary(currency_field='currency_id')
    boq_cost_estimation_line_id = fields.Many2one('boq.cost.estimation.line',
                                                  string="code")
    bill_quantities_labour_machines_id = fields.Many2one(
        'bill.quantities.labour.machines', string="code")
    bill_quantities_overhead_machines_id = fields.Many2one(
        'bill.quantities.overhead')
    bill_quantities_machines_id = fields.Many2one(
        'bill.of.quantities.line')

    determine_quantity = fields.Float()
    construction_subcontractor_lines_id = fields.Many2one('construction.subcontractor.lines')
