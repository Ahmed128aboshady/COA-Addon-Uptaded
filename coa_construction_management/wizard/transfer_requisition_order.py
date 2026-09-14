# -*- coding: utf-8 -*-
""" Transfer Requisition Order """
from odoo import api, fields, models, _

class TransferRequisitionOrder(models.TransientModel):
    """ Transfer Requisition Order """
    _inherit = 'transfer.requisition.order'
    _description = 'Transfer Requisition Order'

    def confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        requisition = self.env['construction.requisition'].browse(
            active_id)
        items = []
        if self.transfer_type=='transfer':
            for rec in self.transfer_requisition_order_line_ids:
                items.append((0, 0,
                              {'product_id': rec.product_id.id, 'name': rec.name,
                               'location_id': self.location_id.id,
                               'location_dest_id': self.location_dest_id.id,
                               'product_uom_qty': rec.quantity}))
            self.env['stock.picking'].sudo().create(
                {'picking_type_id': self.picking_type_id.id,
                 'location_id': self.location_id.id,
                 'location_dest_id': self.location_dest_id.id,
                 'construction_project_id': requisition.construction_project_id.id,
                 'project_name': requisition.project_name,
                 'project_number': requisition.project_number,
                 'project_id': requisition.project_id.id,
                 'project_task_id': requisition.project_task_id.id,
                 'boq_cost_estimation_line_id': requisition.boq_cost_estimation_line_id.id,
                 'construction_requisition_id': requisition.id,
                 'move_ids_without_package':items})
        elif self.transfer_type=='purchase':
            if self.requisition_type=='tender':
                for rec in self.transfer_requisition_order_line_ids:
                    items.append((0, 0,
                                  {'product_id': rec.product_id.id,
                                   'product_uom_id': rec.uom_id.id,
                                   'product_qty': rec.quantity}))


                    self.env['purchase.requisition'].create({
                        'construction_requisition_id':requisition.id,
                        'vendor_id':self.partner_id.id,
                        'construction_project_id': requisition.construction_project_id.id,
                        'project_name': requisition.project_name,
                        'project_number': requisition.project_number,
                        'project_id': requisition.project_id.id,
                        'project_task_id': requisition.project_task_id.id,
                        'boq_cost_estimation_line_id': requisition.boq_cost_estimation_line_id.id,
                        'line_ids':items

                    })


            elif self.requisition_type=='purchase':
                for rec in self.transfer_requisition_order_line_ids:
                    items.append((0, 0,
                                  {'product_id': rec.product_id.id,
                                   'product_uom': rec.uom_id.id,
                                   'product_qty': rec.quantity}))


                    self.env['purchase.order'].create({
                        'partner_id':self.partner_id.id,
                        'construction_requisition_id':requisition.id,
                        'construction_project_id': requisition.construction_project_id.id,
                        'project_name': requisition.project_name,
                        'project_number': requisition.project_number,
                        'project_id': requisition.project_id.id,
                        'project_task_id': requisition.project_task_id.id,
                        'boq_cost_estimation_line_id': requisition.boq_cost_estimation_line_id.id,
                        'order_line':items

                    })
