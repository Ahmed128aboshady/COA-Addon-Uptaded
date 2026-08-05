# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class TechnicalReviewRejectWizard(models.TransientModel):
    _name = 'technical.review.reject.wizard'
    _description = 'Technical Review Rejection Wizard'

    review_id = fields.Many2one(
        'technical.review',
        string='Review',
        required=True,
        readonly=True,
        ondelete='cascade',
    )
    rejection_reason = fields.Text(
        string='Rejection Reason',
        required=True,
        help='Explain what needs to be corrected before re-submission.',
    )

    def action_confirm_reject(self):
        self.ensure_one()
        if self.review_id.state not in ('draft', 'in_progress'):
            raise UserError(_('Only draft or in-progress reviews can be rejected.'))
        self.review_id.write({
            'state': 'rejected',
            'rejection_reason': self.rejection_reason,
            'approval_date': fields.Datetime.now(),
        })
        self.review_id.sale_order_id.message_post(
            body=_(
                '❌ Technical Review <b>%s</b> has been <b>rejected</b>.<br/>'
                '<b>Reason:</b> %s'
            ) % (self.review_id.name, self.rejection_reason)
        )
        return {'type': 'ir.actions.act_window_close'}
