from odoo import models, fields, api, _


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'multi.approval.mixin']

    def action_post(self):
        self._check_approval_before_action(trigger='confirm')
        return super().action_post()

    def _on_approval_approved(self):
        super()._on_approval_approved()
        approval_type = self.approval_request_id.type_id
        if approval_type and approval_type.auto_confirm:
            self.with_context(bypass_multi_approval=True).action_post()

    def _on_approval_refused(self):
        super()._on_approval_refused()
        self.message_post(
            body=_('Approval refused. Reason: %s') % (
                self.approval_request_id.refuse_reason or _('No reason provided')
            ),
            message_type='notification',
        )
