# -*- coding: utf-8 -*-
from odoo import models


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'coa.duplicate.print.mixin']

    def _coa_duplicate_scope(self):
        return 'stock'
