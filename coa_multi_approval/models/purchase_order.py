from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'multi.approval.mixin']

    def button_confirm(self):
        self._check_approval_before_action(trigger='confirm')
        return super().button_confirm()

    def _on_approval_approved(self):
        super()._on_approval_approved()
        approval_type = self.approval_request_id.type_id
        if approval_type and approval_type.auto_confirm:
            self.with_context(bypass_multi_approval=True).button_confirm()

    def _on_approval_refused(self):
        super()._on_approval_refused()
        self.message_post(
            body=_('Approval refused. Reason: %s') % (
                self.approval_request_id.refuse_reason or _('No reason provided')
            ),
            message_type='notification',
        )
