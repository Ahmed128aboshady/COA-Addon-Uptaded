# -*- coding: utf-8 -*-
""" Advance Payment Guarantee """
from odoo import api, fields, models, _

class LgAdvancePaymentGuarantee(models.Model):
    """ inherit Lg Advance Payment Guarantee """
    _inherit = 'lg.advance.payment.guarantee'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
