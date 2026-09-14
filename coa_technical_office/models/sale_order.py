# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    technical_review_id = fields.Many2one(
        'technical.review',
        string='Technical Review',
        readonly=True,
        copy=False,
        ondelete='set null',
        index=True,
    )
    technical_state = fields.Selection(
        related='technical_review_id.state',
        string='Technical Review Status',
        store=True,
        readonly=True,
    )
    requires_technical_review = fields.Boolean(
        string='Requires Technical Review',
        default=True,
        help='When enabled, this order must be approved by the Technical Office '
             'before it can be confirmed.',
    )

    # -------------------------------------------------------------------------
    # Override confirm: block until review is approved
    # -------------------------------------------------------------------------

    def action_confirm(self):
        for order in self:
            if order.requires_technical_review and order.technical_state != 'approved':
                msg = _(
                    'Order "%s" requires Technical Office approval before confirmation.'
                ) % order.name
                if not order.technical_review_id:
                    msg += _('\n\nPlease click "Request Technical Review" first.')
                else:
                    status_labels = {
                        'draft': _('Draft'),
                        'in_progress': _('In Progress'),
                        'rejected': _('Rejected'),
                    }
                    current = status_labels.get(order.technical_state, order.technical_state)
                    msg += _('\n\nCurrent review status: %s') % current
                    if order.technical_state == 'rejected':
                        reason = order.technical_review_id.rejection_reason or ''
                        msg += _('\n\nRejection reason: %s') % reason
                raise UserError(msg)
        return super().action_confirm()

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def action_send_to_technical(self):
        """
        Create a technical.review for this SO (with one line per product),
        or open the existing one if it already exists.
        """
        self.ensure_one()

        # If active review exists (not rejected), just open it
        if (
            self.technical_review_id
            and self.technical_review_id.state not in ('rejected',)
        ):
            return {
                'type': 'ir.actions.act_window',
                'name': _('Technical Review'),
                'res_model': 'technical.review',
                'view_mode': 'form',
                'res_id': self.technical_review_id.id,
            }

        # Build one review line per storable/consumable product line
        review_line_vals = []
        for line in self.order_line:
            # Skip section/note lines and service products
            if line.display_type:
                continue
            if not line.product_id:
                continue
            if line.product_id.type == 'service':
                continue

            # Try to find an existing BOM for this product
            bom = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                '|',
                ('product_id', '=', False),
                ('product_id', '=', line.product_id.id),
                ('company_id', 'in', [self.company_id.id, False]),
            ], limit=1)

            review_line_vals.append({
                'sale_line_id': line.id,
                'bom_id': bom.id if bom else False,
                'line_state': 'pending',
            })

        if not review_line_vals:
            raise UserError(_(
                'No storable/consumable products found in this order. '
                'Technical review is only needed for physical products.'
            ))

        review = self.env['technical.review'].create({
            'sale_order_id': self.id,
            'company_id': self.company_id.id,
            'line_ids': [(0, 0, v) for v in review_line_vals],
        })
        self.technical_review_id = review.id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Technical Review'),
            'res_model': 'technical.review',
            'view_mode': 'form',
            'res_id': review.id,
        }

    def action_view_technical_review(self):
        """Open the linked technical review from the smart button."""
        self.ensure_one()
        if not self.technical_review_id:
            raise UserError(_('No technical review linked to this order.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Technical Review'),
            'res_model': 'technical.review',
            'view_mode': 'form',
            'res_id': self.technical_review_id.id,
        }
