# -*- coding: utf-8 -*-
""" Construction Requisition """
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ConstructionRequisition(models.Model):
    """ Construction Requisition """
    _name = 'construction.requisition'
    _description = 'Construction Requisition'

    name = fields.Char(default='New')
    date = fields.Date()
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.company)
    description = fields.Html()
    construction_requisition_line_ids = fields.One2many(
        'construction.requisition.line', 'construction_requisition_id')

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('send_to_pm_approve', 'Send To PM Approve'),
                              ('pm_approved', 'PM Approved'),
                              ('pm_rejected', 'PM Rejected'), ('lock', 'Lock')],
                             default='draft', string='Status')

    stock_picking_ids = fields.One2many('stock.picking',
                                        'construction_requisition_id')
    count_picking = fields.Integer(compute='_compute_count_picking', store=True)
    purchase_order_ids = fields.One2many('purchase.order',
                                         'construction_requisition_id')
    count_purchase_order = fields.Integer(
        compute='_compute_count_purchase_order', store=True)
    purchase_requisition_ids = fields.One2many('purchase.requisition',
                                               'construction_requisition_id')
    count_purchase_requisition = fields.Integer(
        compute='_compute_count_purchase_requisition', store=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    @api.depends('purchase_requisition_ids')
    def _compute_count_purchase_requisition(self):
        """ Compute count_picking value """
        for rec in self:
            rec.count_purchase_requisition = len(
                rec.purchase_requisition_ids.ids)

    def action_view_all_purchase_requisition(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "purchase.requisition",
            "domain": [('construction_requisition_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Purchase Agreements"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('purchase_order_ids')
    def _compute_count_purchase_order(self):
        """ Compute count_picking value """
        for rec in self:
            rec.count_purchase_order = len(rec.purchase_order_ids.ids)

    def action_view_all_purchase_order(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "domain": [('construction_requisition_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Purchase Order"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('stock_picking_ids')
    def _compute_count_picking(self):
        """ Compute count_picking value """
        for rec in self:
            rec.count_picking = len(rec.stock_picking_ids.ids)

    def action_view_all_stock_picking(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "domain": [('construction_requisition_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Stock Picking"),
            'view_mode': 'list,form',
        }
        return result


    def transfer(self):
        """ Transfer """
        items = []
        for rec in self.construction_requisition_line_ids:
            if rec.select:
                items.append((0, 0, {'product_id': rec.product_id.id,
                                     'name': rec.name,
                                     'quantity': rec.quantity}))
                rec.select = False
        if items:
            action = \
                self.env.ref(
                    'arabian_requisition.transfer_requisition_order_action').sudo().read()[
                    0]
            action['context'] = {
                'default_transfer_requisition_order_line_ids': items,
                'default_transfer_type': 'transfer'
            }
            action['views'] = [
                (self.env.ref(
                    'arabian_requisition.transfer_requisition_order_form').id,
                 'form')]
            return action
        else:
            raise ValidationError(
                _("Not Record Selected"))

    def purchase(self):
        """ Purchase """

        items = []
        for rec in self.construction_requisition_line_ids:
            if rec.select:
                items.append((0, 0, {'product_id': rec.product_id.id,
                                     'name': rec.name,
                                     'quantity': rec.quantity}))
                rec.select = False
        if items:
            action = \
                self.env.ref(
                    'arabian_requisition.transfer_requisition_order_action').sudo().read()[
                    0]
            action['context'] = {
                'default_transfer_requisition_order_line_ids': items,
                'default_transfer_type': 'purchase'
            }
            action['views'] = [
                (self.env.ref(
                    'arabian_requisition.transfer_requisition_order_form').id,
                 'form')]
            return action
        else:
            raise ValidationError(
                _("Not Record Selected"))

    def lock_order(self):
        """ Lock """
        for rec in self:
            rec.state = 'lock'

    def pm_rejected(self):
        """ Pm Rejected """
        for rec in self:
            rec.state = 'pm_rejected'

    def pm_approved(self):
        """ Pm Approved """
        for rec in self:
            rec.state = 'pm_approved'

    def send_to_pm_approve(self):
        """ Send To Pm Approve """
        for rec in self:
            rec.state = 'send_to_pm_approve'


    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirmed'

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.requisition') or '/'
        return super(ConstructionRequisition, self).create(vals)


class ConstructionRequisitionLine(models.Model):
    """ Construction Requisition Line """
    _name = 'construction.requisition.line'
    _description = 'Construction Requisition Line'

    construction_requisition_id = fields.Many2one('construction.requisition')
    product_id = fields.Many2one('product.product')
    name = fields.Text(string="Description")
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure',
                             related='product_id.uom_id')
    quantity = fields.Float()
    select = fields.Boolean()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.name=rec.product_id.name

    def open_on_hand(self):
        """ Utility method used to add an "Open Parent" button in partner views """
        self.ensure_one()
        address_form_id = self.env.ref(
            'stock.view_stock_quant_tree_inventory_editable').id
        return {'type': 'ir.actions.act_window',
                'res_model': 'stock.quant',
                'context': {'create': 0, 'edit': 0,'hide_set_button':True},
                'domain': [('product_id', '=', self.product_id.id),
                           ('on_hand', '=', True)],
                'view_mode': 'form',
                'views': [(address_form_id, 'list')],
                'target': 'new',
                }
