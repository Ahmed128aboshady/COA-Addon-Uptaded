# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models, _


class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    incoming_cheque_id = fields.Many2one('incoming.cheque')
    outgoing_cheque_id = fields.Many2one('outgoing.cheque')

class AccountMoveLine(models.Model):
    """ inherit Account Move Line """
    _inherit = 'account.move.line'

    outgoing_cheque_id = fields.Many2one('outgoing.cheque')
    incoming_cheque_id = fields.Many2one('incoming.cheque')
