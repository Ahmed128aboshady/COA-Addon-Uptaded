from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class PettyCashApprover(models.Model):
    """Petty Cash Approver Settings - Multi-level Approval"""
    _name = 'petty.cash.approver'
    _description = 'Petty Cash Approver'
    _order = 'level, sequence, id'

    level = fields.Integer(
        string='Approval Level', default=1, required=True,
        help='Level 1 approves first, then Level 2, etc.'
    )
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(
        string='Role / Position', required=True,
        help='e.g. Finance Manager, General Manager'
    )
    approval_type = fields.Selection([
        ('custody', 'Custody Approval'),
        ('expense', 'Expense Approval'),
        ('both', 'Both'),
    ], string='Approval Type', required=True, default='both')
    user_ids = fields.Many2many(
        'res.users',
        'petty_cash_approver_users_rel',
        'approver_id', 'user_id',
        string='Approvers',
        required=True,
        domain="[('share', '=', False)]",
    )
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company
    )
    notes = fields.Text(string='Notes')

    @api.constrains('user_ids')
    def _check_users(self):
        for rec in self:
            if not rec.user_ids:
                raise ValidationError(_('At least one approver must be specified!'))

    @api.constrains('level')
    def _check_level(self):
        for rec in self:
            if rec.level < 1:
                raise ValidationError(_('Approval level must be 1 or greater!'))

    def _get_approvers_for_type(self, approval_type):
        """Return all approver users for a given type (all levels)"""
        records = self._get_records_for_type(approval_type)
        return records.mapped('user_ids')

    def _get_records_for_type(self, approval_type):
        """Return approver records for a given type, ordered by level"""
        return self.search([
            ('active', '=', True),
            ('approval_type', 'in', [approval_type, 'both']),
            '|',
            ('company_id', '=', self.env.company.id),
            ('company_id', '=', False),
        ], order='level, sequence, id')

    def _get_first_level(self, approval_type):
        """Return the lowest approval level for a given type"""
        records = self._get_records_for_type(approval_type)
        if not records:
            return 0
        return min(records.mapped('level'))

    def _get_approvers_at_level(self, approval_type, level):
        """Return approvers at a specific level"""
        return self.search([
            ('active', '=', True),
            ('approval_type', 'in', [approval_type, 'both']),
            ('level', '=', level),
            '|',
            ('company_id', '=', self.env.company.id),
            ('company_id', '=', False),
        ])

    def _get_next_level(self, approval_type, current_level):
        """Return the next level after current_level, or False if none"""
        records = self._get_records_for_type(approval_type)
        all_levels = sorted(set(records.mapped('level')))
        if current_level not in all_levels:
            return False
        idx = all_levels.index(current_level)
        if idx + 1 < len(all_levels):
            return all_levels[idx + 1]
        return False
