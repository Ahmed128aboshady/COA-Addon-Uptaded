# -*- coding: utf-8 -*-
""" Construction Business Items """
from odoo import api, fields, models, _

class ConstructionBusinessItems(models.Model):
    """ Construction Business Items """
    _name = 'construction.business.items'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin',
                'utm.mixin']
    _description = 'Construction Business Items'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('breakdown_created', 'Breakdown Created'),
    ], string='Status', default='draft')
    name = fields.Char(translate=True, default='New')
    project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    partner_id = fields.Many2one('res.partner', string="Customer")
    project_location = fields.Char(translate=True)
    date = fields.Date(default=fields.Date.today())
    construction_business_items_line_ids = fields.One2many(
        'construction.business.items.line', 'construction_business_items_id')
    count_breakdown = fields.Integer(compute='_compute_count_breakdown',
                                     store=True)
    breakdown_ids = fields.One2many('detailed.bill.of.quantities',
                                    'construction_business_items_id')
    boq_cost_estimation_id = fields.Many2one('boq.cost.estimation')
    boq_documents_folder_id = fields.Many2one('documents.document')
    construction_documents_folder_id = fields.Many2one('documents.document')

    def create_breakdown(self):
        """ Transfer """
        action = \
            self.env.ref(
                'arabian_construction_management.select_detailed_boq_type_action').sudo().read()[
                0]
        action['views'] = [
            (self.env.ref(
                'arabian_construction_management.select_detailed_boq_type_form').id,
             'form')]
        return action





    @api.depends('breakdown_ids')
    def _compute_count_breakdown(self):
        """ Compute count_breakdown value """
        for rec in self:
            rec.count_breakdown = len(rec.breakdown_ids.ids)

    def action_view_all_breakdown(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "detailed.bill.of.quantities",
            "domain": [('construction_business_items_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Breakdown"),
            'view_mode': 'list,form',
        }
        return result

    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirm'

    # def create_breakdown(self):
    #     """ Create Breakdown """
    #     for c in self:
    #         boq_cost_estimation_id = self.env[
    #             'boq.cost.estimation'].sudo().create({
    #             'construction_business_items_id': c.id,
    #             'project_id': c.project_id.id,
    #             'project_name': c.project_name,
    #             'project_number': c.project_number,
    #             'project_description': c.project_description,
    #             'project_type_id': c.project_type_id.id,
    #             'partner_id': c.partner_id.id,
    #             'project_location': c.project_location,
    #             'date': c.date}).id
    #         c.boq_cost_estimation_id = boq_cost_estimation_id
    #
    #     for rec in self.construction_business_items_line_ids:
    #         self.env['detailed.bill.of.quantities'].sudo().create(
    #             {'construction_business_items_id': self.id,
    #              'project_id': self.project_id.id,
    #              'item_code': rec.item_code,
    #              'project_name': self.project_name,
    #              'project_number': self.project_number,
    #              'project_description': self.project_description,
    #              'project_type_id': self.project_type_id.id,
    #              'partner_id': self.partner_id.id,
    #              'project_location': self.project_location,
    #              'boq_cost_estimation_id': self.boq_cost_estimation_id.id,
    #              'business_item_id': rec.business_item_id.id,
    #              'business_items_types_id': rec.business_items_types_id.id,
    #              'description': rec.description, 'uom_id': rec.uom_id.id,
    #              'quantity': rec.quantity})
    #     self.state = 'breakdown_created'

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.business.items') or '/'
            vals['boq_documents_folder_id'] = self.env[
                'documents.document'].create({'name': vals['name'],
                                            'folder_id': vals[
                                                'construction_documents_folder_id']}).id
        return super(ConstructionBusinessItems, self).create(vals)


class ConstructionBusinessItemsLine(models.Model):
    """ Construction Business Items Line """
    _name = 'construction.business.items.line'
    _description = 'Construction Business Items Line'

    construction_business_items_id = fields.Many2one(
        'construction.business.items')
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    name = fields.Char(compute='_compute_description_name', store=True)
    description = fields.Text(translate=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float(default=1)
    item_code = fields.Char()
    boq_documents_folder_id = fields.Many2one('documents.document',
                                              related='construction_business_items_id.boq_documents_folder_id')

    @api.depends('description')
    def _compute_description_name(self):
        """ Compute description_name value """
        for rec in self:
            rec.name = rec.description

    @api.onchange('business_item_id')
    def _onchange_business_item_id(self):
        """ business_item_id """
        for rec in self:
            if rec.business_item_id:
                rec.business_items_types_id = rec.business_item_id.business_items_types_id.id
                rec.uom_id = rec.business_item_id.uom_id.id

    def create(self, vals):
        """ Override create() """
        res = super(ConstructionBusinessItemsLine, self).create(vals)
        for record in res:
            if record.boq_documents_folder_id:
                self.env['documents.document'].create({
                    'name': record.item_code,
                    'folder_id': record.boq_documents_folder_id.id
                })

        return res
