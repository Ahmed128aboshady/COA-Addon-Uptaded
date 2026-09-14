# -*- coding: utf-8 -*-
""" Construction Pricing """
from odoo import api, fields, models, _


class ConstructionPricing(models.Model):
    """ Construction Pricing """
    _name = 'construction.pricing'
    _description = 'Construction Pricing'

    name = fields.Char(default='New')
    partner_id = fields.Many2one('res.partner',string="Vendor")
    description = fields.Html()
    date = fields.Date()
    construction_pricing_line_ids = fields.One2many('construction.pricing.line',
                                                    'construction_pricing_id')

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.pricing') or '/'
        return super(ConstructionPricing, self).create(vals)


class ConstructionPricingLine(models.Model):
    """ Construction Pricing Line """
    _name = 'construction.pricing.line'
    _description = 'Construction Pricing Line'

    construction_pricing_id = fields.Many2one('construction.pricing')
    product_id = fields.Many2one('product.product')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float()
