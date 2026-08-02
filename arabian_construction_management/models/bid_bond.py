# -*- coding: utf-8 -*-
""" Bid Bond """
from odoo import api, fields, models, _


class LgBidBond(models.Model):
    """ inherit Lg Bid Bond """
    _inherit = 'lg.bid.bond'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
