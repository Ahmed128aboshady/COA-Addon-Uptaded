# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models, _


class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    lg_bid_bond_id = fields.Many2one('lg.bid.bond')
    lg_performance_bond_id = fields.Many2one('lg.performance.bond')
    lg_advance_payment_guarantee_id = fields.Many2one('lg.advance.payment.guarantee')
    lg_maintenance_bond_id = fields.Many2one('lg.maintenance.bond')

class AccountMoveLine(models.Model):
    """ inherit Account Move Line """
    _inherit = 'account.move.line'

    lg_bid_bond_id = fields.Many2one('lg.bid.bond')
    lg_performance_bond_id = fields.Many2one('lg.performance.bond')
    lg_advance_payment_guarantee_id = fields.Many2one('lg.advance.payment.guarantee')
    lg_maintenance_bond_id = fields.Many2one('lg.maintenance.bond')