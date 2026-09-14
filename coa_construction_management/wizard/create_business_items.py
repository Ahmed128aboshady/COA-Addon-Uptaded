# -*- coding: utf-8 -*-
""" Create Business Items """
from odoo import api, fields, models, _


class CreateBusinessItems(models.TransientModel):
    """ Create Business Items """
    _name = 'create.business.items'
    _description = 'Create Business Items'

    create_business_items_lines_ids = fields.One2many(
        'create.business.items.lines', 'create_business_items_id')


    def confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        construction_project = self.env['construction.project'].browse(
            active_id)
        items = []
        for rec in self.create_business_items_lines_ids:
            items.append((0, 0, {'business_item_id': rec.business_item_id.id,
                                 'business_items_types_id': rec.business_items_types_id.id,
                                 'description': rec.description,
                                 'item_code':rec.item_code,
                                 'uom_id': rec.uom_id.id,
                                 'quantity': rec.quantity}))
        self.env['construction.business.items'].sudo().create(
            {'project_id': construction_project.id,
             'project_name': construction_project.project_name,
             'project_number': construction_project.project_number,
             'project_description': construction_project.project_description,
             'project_type_id': construction_project.project_type_id.id,
             'partner_id': construction_project.partner_id.id,
             'project_location': construction_project.project_location,
             'construction_documents_folder_id':construction_project.documents_folder_id.id,
             'construction_business_items_line_ids': items})
        construction_project.state = 'business_items_created'

    class CreateBusinessItemsLines(models.TransientModel):
        """ Create Business Items Lines """
        _name = 'create.business.items.lines'
        _description = 'Create Business Items Lines'
    
        item_code = fields.Char()
        create_business_items_id = fields.Many2one('create.business.items')
        business_item_id = fields.Many2one('detailed.business.items')
        business_items_types_id = fields.Many2one('business.items.types')
        description = fields.Text(translate=True)
        uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
        quantity = fields.Float(default=1)

        @api.onchange('business_item_id')
        def _onchange_business_item_id(self):
            """ business_item_id """
            for rec in self:
                if rec.business_item_id:
                    rec.business_items_types_id = rec.business_item_id.business_items_types_id.id
                    rec.uom_id = rec.business_item_id.uom_id.id
