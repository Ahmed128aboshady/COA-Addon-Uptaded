# -*- coding: utf-8 -*-
""" Purchase Order """
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    """ inherit Purchase Order """
    _inherit = 'purchase.order'
    
    construction_requisition_id = fields.Many2one('construction.requisition')