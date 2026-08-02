# -*- coding: utf-8 -*-
""" Account Move """
from odoo import api, fields, models, _


class AccountMove(models.Model):
    """ inherit Account Move """
    _inherit = 'account.move'

    expense_payment_id = fields.Many2one('expense.payment')


class AccountMoveLine(models.Model):
    """ inherit Account Move Line """
    _inherit = 'account.move.line'
    memo = fields.Char(string="Description")
    employee_id = fields.Many2one(
        'hr.employee')
    expense_payment_id = fields.Many2one('expense.payment')
    expense_payment_line_id = fields.Many2one('expense.payment.line')
