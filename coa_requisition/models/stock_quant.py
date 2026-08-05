# -*- coding: utf-8 -*-
""" Stock Quant """
from odoo import api, fields, models, _

class StockQuant(models.Model):
    """ inherit Stock Quant """
    _inherit = 'stock.quant'

    hide_set_button = fields.Boolean()