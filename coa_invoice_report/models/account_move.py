from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_contract_value = fields.Float(string='Contract Value', default=0.0)
    x_claim_percent = fields.Float(string='Claim %', default=100.0)
    x_advance_percent = fields.Float(string='Advance %', default=0.0)
    x_retention_percent = fields.Float(string='Retention %', default=0.0)

    x_claim_amount = fields.Monetary(string='Claim Amount', compute='_compute_claim_values', currency_field='currency_id', store=True)
    x_advance_amount = fields.Monetary(string='Advance Amount', compute='_compute_claim_values', currency_field='currency_id', store=True)
    x_net_amount = fields.Monetary(string='Net Amount', compute='_compute_claim_values', currency_field='currency_id', store=True)
    x_retention_amount = fields.Monetary(string='Retention Amount', compute='_compute_claim_values', currency_field='currency_id', store=True)
    x_net_required = fields.Monetary(string='Net Required Amount', compute='_compute_claim_values', currency_field='currency_id', store=True)

    @api.depends('amount_untaxed', 'amount_tax', 'x_contract_value', 'x_claim_percent', 'x_advance_percent', 'x_retention_percent')
    def _compute_claim_values(self):
        for move in self:
            total = move.amount_untaxed
            
            # Claim Amount
            claim_pc = move.x_claim_percent if move.x_claim_percent else 100.0
            claim_amount = total * (claim_pc / 100.0)
            move.x_claim_amount = claim_amount
            
            # Advance Amount (if contract total is set, calculate on contract total, else on claim)
            adv_pc = move.x_advance_percent if move.x_advance_percent else 0.0
            if move.x_contract_value > 0:
                advance_amount = move.x_contract_value * (adv_pc / 100.0)
            else:
                advance_amount = claim_amount * (adv_pc / 100.0)
            move.x_advance_amount = advance_amount
            
            # Retention Amount (typically 5% of claim)
            ret_pc = move.x_retention_percent if move.x_retention_percent else 0.0
            retention_amount = claim_amount * (ret_pc / 100.0)
            move.x_retention_amount = retention_amount
            
            # Net Amount = Claim - Advance - Retention
            net_amount = claim_amount - advance_amount - retention_amount
            move.x_net_amount = net_amount
            
            # Net Required = Net + VAT
            move.x_net_required = net_amount + move.amount_tax
