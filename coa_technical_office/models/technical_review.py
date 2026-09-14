# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TechnicalReview(models.Model):
    _name = 'technical.review'
    _description = 'Technical Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        required=True,
        ondelete='restrict',
        tracking=True,
        index=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='sale_order_id.partner_id',
        store=True,
        readonly=True,
        index=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        index=True,
        copy=False,
    )
    reviewer_id = fields.Many2one(
        'res.users',
        string='Reviewer',
        default=lambda self: self.env.user,
        tracking=True,
        index=True,
    )
    review_date = fields.Datetime(
        string='Review Started',
        tracking=True,
        copy=False,
    )
    approval_date = fields.Datetime(
        string='Approved/Rejected On',
        readonly=True,
        copy=False,
        tracking=True,
    )
    notes = fields.Text(string='Technical Notes')
    rejection_reason = fields.Text(
        string='Rejection Reason',
        readonly=True,
        copy=False,
        tracking=True,
    )
    line_ids = fields.One2many(
        'technical.review.line',
        'review_id',
        string='Products to Review',
        copy=True,
    )
    lines_all_reviewed = fields.Boolean(
        string='All Lines Reviewed',
        compute='_compute_lines_all_reviewed',
        store=False,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    # -------------------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('technical.review')
                    or 'New'
                )
        return super().create(vals_list)

    # -------------------------------------------------------------------------
    # Computed
    # -------------------------------------------------------------------------

    @api.depends('line_ids', 'line_ids.line_state')
    def _compute_lines_all_reviewed(self):
        for rec in self:
            if not rec.line_ids:
                rec.lines_all_reviewed = False
            else:
                rec.lines_all_reviewed = all(
                    line.line_state == 'reviewed' for line in rec.line_ids
                )

    # -------------------------------------------------------------------------
    # State transitions
    # -------------------------------------------------------------------------

    def action_start(self):
        """Draft → In Progress"""
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft reviews can be started.'))
        self.write({
            'state': 'in_progress',
            'review_date': fields.Datetime.now(),
        })

    def action_approve(self):
        """In Progress → Approved"""
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError(_('Only in-progress reviews can be approved.'))
            if not rec.lines_all_reviewed:
                raise UserError(
                    _('Please mark all product lines as "Reviewed" before approving review %s.') % rec.name
                )
        self.write({
            'state': 'approved',
            'approval_date': fields.Datetime.now(),
        })
        for rec in self:
            rec.sale_order_id.message_post(
                body=_('✅ Technical Review <b>%s</b> has been <b>approved</b>. '
                       'You may now confirm the sale order.') % rec.name
            )

    def action_reject(self):
        """Open rejection reason wizard"""
        self.ensure_one()
        if self.state not in ('draft', 'in_progress'):
            raise UserError(_('Only draft or in-progress reviews can be rejected.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reject Review'),
            'res_model': 'technical.review.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_review_id': self.id},
        }

    def action_reset_to_draft(self):
        """In Progress / Rejected → Draft"""
        self.filtered(
            lambda r: r.state in ('in_progress', 'rejected')
        ).write({
            'state': 'draft',
            'rejection_reason': False,
            'review_date': False,
            'approval_date': False,
        })

    def action_view_sale_order(self):
        """Navigate back to the linked sale order."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sale Order'),
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
        }
