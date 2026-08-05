# -*- coding: utf-8 -*-
""" Account Journal """
from odoo import api, fields, models, _


class AccountJournal(models.Model):
    """ inherit Account Journal """
    _inherit = 'account.journal'

    allow_expense = fields.Boolean()

