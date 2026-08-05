# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models, _

class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'