# -*- coding: utf-8 -*-
""" Detailed Business Items """
from odoo import api, fields, models, _
from random import randint

class DetailedBusinessItems(models.Model):
    """ Detailed Business Items """
    _name = 'detailed.business.items'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin',
                'utm.mixin']
    _description = 'Detailed Business Items'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    business_items_types_id = fields.Many2one('business.items.types')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    description = fields.Html(translate=True)
    color = fields.Integer(default=_default_color)

