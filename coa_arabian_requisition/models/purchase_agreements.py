# -*- coding: utf-8 -*-
""" Purchase Agreements """
from odoo import api, fields, models, _


class PurchaseRequisition(models.Model):
    """ inherit Purchase Requisition """
    _inherit = 'purchase.requisition'

    construction_requisition_id = fields.Many2one('construction.requisition')
