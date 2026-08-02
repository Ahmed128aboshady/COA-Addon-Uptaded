from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'multi.approval.mixin']

    # ── Auto-submit approval on create (on_save trigger) ────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if self.env.context.get('bypass_multi_approval'):
            return records
        for record in records:
            approval_type = record._get_approval_type(trigger='on_save')
            if approval_type and approval_type.stage_ids:
                record._auto_submit_approval(approval_type)
        return records

    def _auto_submit_approval(self, approval_type):
        """Create and submit an approval request automatically (no UI return)."""
        # Skip if already has an active request
        if self.approval_request_id and self.approval_request_id.state in ('pending', 'approved'):
            return
        request = self.env['multi.approval.request'].create({
            'name': '/',
            'type_id': approval_type.id,
            'res_model': self._name,
            'res_id': self.id,
            'res_name': self.display_name,
        })
        self.approval_request_id = request
        request.action_submit()

    # ── Block: Confirm ───────────────────────────────────────────────────────
    def action_confirm(self):
        self._check_approval_before_action(trigger='confirm')
        return super().action_confirm()

    # ── Block: Send by Email ─────────────────────────────────────────────────
    def action_quotation_send(self):
        self._check_approval_before_action(trigger='send')
        return super().action_quotation_send()

    # ── Block: Print PDF ─────────────────────────────────────────────────────
    def action_print_quotation(self):
        """Called from our custom Print button — checks approval before printing."""
        self._check_approval_before_action(trigger='print')
        return self.env.ref('sale.action_report_saleorder').report_action(self)

    # ── Callbacks ────────────────────────────────────────────────────────────
    def _on_approval_approved(self):
        super()._on_approval_approved()
        approval_type = self.approval_request_id.type_id
        if approval_type and approval_type.auto_confirm and approval_type.trigger == 'confirm':
            self.with_context(bypass_multi_approval=True).action_confirm()

    def _on_approval_refused(self):
        super()._on_approval_refused()
        self.message_post(
            body=_('Approval refused. Reason: %s') % (
                self.approval_request_id.refuse_reason or _('No reason provided')
            ),
            message_type='notification',
        )
