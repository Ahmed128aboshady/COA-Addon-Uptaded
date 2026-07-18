# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'coa.duplicate.print.mixin']

    def _coa_duplicate_scope(self):
        return 'sale'
