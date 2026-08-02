from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ApprovalRefuseWizard(models.TransientModel):
    _name = 'multi.approval.refuse.wizard'
    _description = 'Approval Refuse Wizard'

    request_id = fields.Many2one('multi.approval.request', string='Approval Request', required=True)
    reason = fields.Text(string='Refusal Reason', required=True)

    def action_refuse(self):
        self.ensure_one()
        self.request_id.action_refuse(self.reason)
        return {'type': 'ir.actions.act_window_close'}
