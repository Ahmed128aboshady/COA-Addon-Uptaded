# -*- coding: utf-8 -*-
""" Select Detailed Boq Type"""
from odoo import api, fields, models, _


class SelectDetailedBoqType(models.TransientModel):
    """ Select Detailed Boq Type """
    _name = 'select.detailed.boq.type'
    _description = 'Select Detailed Boq Type'

    detailed_boq_type = fields.Selection(
        [('single_order', 'Single Order'), ('multi_orders', 'Multi Orders')],
        string="Detailed BOQ Type", default='single_order')

    def create_breakdown(self):
        """ Create Breakdown """
        active_id = self._context.get('active_id')
        construction_business_items = self.env[
            'construction.business.items'].browse(active_id)
        for c in construction_business_items:
            boq_cost_estimation_id = self.env[
                'boq.cost.estimation'].sudo().create({
                'construction_business_items_id': c.id,
                'project_id': c.project_id.id,
                'project_name': c.project_name,
                'project_number': c.project_number,
                'project_description': c.project_description,
                'project_type_id': c.project_type_id.id,
                'partner_id': c.partner_id.id,
                'project_location': c.project_location,
                'date': c.date
            }).id
            c.boq_cost_estimation_id = boq_cost_estimation_id
        if self.detailed_boq_type == 'multi_orders':
            for rec in construction_business_items.construction_business_items_line_ids:
                self.env['detailed.bill.of.quantities'].sudo().create(
                    {
                        'construction_business_items_id': construction_business_itemsع.id,
                        'project_id': construction_business_items.project_id.id,
                        'detailed_boq_type': self.detailed_boq_type,
                        'item_code': rec.item_code,
                        'project_name': construction_business_items.project_name,
                        'project_number': construction_business_items.project_number,
                        'project_description': construction_business_items.project_description,
                        'project_type_id': construction_business_items.project_type_id.id,
                        'partner_id': construction_business_items.partner_id.id,
                        'project_location': construction_business_items.project_location,
                        'boq_cost_estimation_id': construction_business_items.boq_cost_estimation_id.id,
                        'business_item_id': rec.business_item_id.id,
                        'business_items_line_ids': [(6, 0,
                                                     construction_business_items.construction_business_items_line_ids.ids)],
                        'business_items_types_id': rec.business_items_types_id.id,
                        'description': rec.description, 'uom_id': rec.uom_id.id,
                        'quantity': rec.quantity
                    })
        elif self.detailed_boq_type == 'single_order':
            items = []
            for rec in construction_business_items.construction_business_items_line_ids:
                items.append((0, 0,
                              {
                                  'business_item_id': rec.business_item_id.id,
                                  'business_items_types_id': rec.business_items_types_id.id,
                                  'description': rec.description,
                                  'item_code': rec.item_code
                              }))
            self.env['detailed.bill.of.quantities'].sudo().create(
                {
                    'construction_business_items_id': construction_business_items.id,
                    'project_id': construction_business_items.project_id.id,
                    'project_name': construction_business_items.project_name,
                    'detailed_boq_type': self.detailed_boq_type,
                    'project_number': construction_business_items.project_number,
                    'project_description': construction_business_items.project_description,
                    'project_type_id': construction_business_items.project_type_id.id,
                    'partner_id': construction_business_items.partner_id.id,
                    'project_location': construction_business_items.project_location,
                    'boq_cost_estimation_id': construction_business_items.boq_cost_estimation_id.id,
                    'bill_of_quantities_line_ids': items,
                    'business_items_line_ids': [(6, 0,
                                                 construction_business_items.construction_business_items_line_ids.ids)],

                })
        construction_business_items.state = 'breakdown_created'
