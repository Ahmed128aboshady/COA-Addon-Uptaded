# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sale_qty_available_display = fields.Char(
        string='المتاح للبيع',
        compute='_compute_sale_stock_display',
    )

    sale_qty_on_hand_display = fields.Char(
        string='في المخزن',
        compute='_compute_sale_stock_display',
    )

    @api.depends('qty_available', 'virtual_available', 'uom_id')
    def _compute_sale_stock_display(self):
        for product in self:
            uom = product.uom_id.name or ''
            on_hand = product.qty_available
            available = product.virtual_available
            product.sale_qty_on_hand_display = f"{on_hand:g} {uom}"
            product.sale_qty_available_display = f"{available:g} {uom}"

    def _search_display_name(self, operator, value):
        """إضافة معلومات المخزون لنتائج البحث لما show_sale_stock موجود في السياق"""
        res = super()._search_display_name(operator, value)
        if self.env.context.get('show_sale_stock'):
            records = self.search(res if isinstance(res, list) else [res])
            return [('id', 'in', records.ids)]
        return res

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None):
        ids = super()._name_search(name, domain, operator, limit, order)
        if not self.env.context.get('show_sale_stock'):
            return ids
        # أعد الـ ids كما هي — الـ display يتحكم فيه name_get
        return ids

    def name_get(self):
        if not self.env.context.get('show_sale_stock'):
            return super().name_get()
        res = []
        for product in self:
            name = product.display_name
            available = product.virtual_available
            uom = product.uom_id.name or ''
            stock_info = f"[{available:g} {uom}]"
            res.append((product.id, f"{name}  {stock_info}"))
        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_qty_available_display = fields.Char(
        string='المتاح للبيع',
        compute='_compute_sale_stock_display_tmpl',
    )

    sale_qty_on_hand_display = fields.Char(
        string='في المخزن',
        compute='_compute_sale_stock_display_tmpl',
    )

    @api.depends('qty_available', 'virtual_available', 'uom_id')
    def _compute_sale_stock_display_tmpl(self):
        for tmpl in self:
            uom = tmpl.uom_id.name or ''
            on_hand = tmpl.qty_available
            available = tmpl.virtual_available
            tmpl.sale_qty_on_hand_display = f"{on_hand:g} {uom}"
            tmpl.sale_qty_available_display = f"{available:g} {uom}"

    def name_get(self):
        if not self.env.context.get('show_sale_stock'):
            return super().name_get()
        res = []
        for tmpl in self:
            name = tmpl.display_name
            available = tmpl.virtual_available
            uom = tmpl.uom_id.name or ''
            stock_info = f"[{available:g} {uom}]"
            res.append((tmpl.id, f"{name}  {stock_info}"))
        return res
