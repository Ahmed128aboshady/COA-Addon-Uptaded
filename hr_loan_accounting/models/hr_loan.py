from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrLoan(models.Model):
    _inherit = 'hr.loan'

    loan_account_id = fields.Many2one(
        'account.account', string="Loan Account",
        help="Account used to record the loan receivable (debit side).")
    treasury_account_id = fields.Many2one(
        'account.account', string="Treasury Account",
        help="Account used to record the cash/bank disbursement (credit side).")
    journal_id = fields.Many2one(
        'account.journal', string="Journal",
        domain="[('type', 'in', ['bank', 'cash'])]",
        help="Journal used for the loan disbursement entry.")
    move_count = fields.Integer(
        string="Journal Entry Count", compute='_compute_move_count')

    def _compute_move_count(self):
        move_model = self.env['account.move']
        for loan in self:
            loan.move_count = move_model.search_count(
                [('ref', '=', loan.name)])

    def action_approve(self):
        """Approve loan and create a journal entry for the disbursement."""
        res = super().action_approve()
        for loan in self:
            if not loan.journal_id or not loan.loan_account_id or not loan.treasury_account_id:
                raise UserError(_(
                    "Please set the Loan Account, Treasury Account, and "
                    "Journal before approving the loan."))
            move_vals = {
                'journal_id': loan.journal_id.id,
                'date': fields.Date.context_today(self),
                'ref': loan.name,
                'line_ids': [
                    (0, 0, {
                        'name': loan.name,
                        'account_id': loan.loan_account_id.id,
                        'debit': loan.loan_amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {
                        'name': loan.name,
                        'account_id': loan.treasury_account_id.id,
                        'debit': 0.0,
                        'credit': loan.loan_amount,
                    }),
                ],
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
        return res

    def action_view_journal_entries(self):
        """Open journal entries related to this loan."""
        self.ensure_one()
        moves = self.env['account.move'].search([('ref', '=', self.name)])
        action = {
            'name': _('Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', moves.ids)],
            'context': {'default_ref': self.name},
        }
        if len(moves) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = moves.id
        return action
