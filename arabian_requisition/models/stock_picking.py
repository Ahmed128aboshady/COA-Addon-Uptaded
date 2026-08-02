# -*- coding: utf-8 -*-
""" Stock Picking """
from odoo import api, fields, models, _


class StockPicking(models.Model):
    """ inherit Stock Picking """
    _inherit = 'stock.picking'

    construction_requisition_id = fields.Many2one('construction.requisition')
