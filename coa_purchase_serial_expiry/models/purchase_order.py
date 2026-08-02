from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # ── Auto Serial ────────────────────────────────────────────────────────────
    serial_number = fields.Char(
        string='Serial #',
        readonly=True,
        copy=False,
        index=True,
    )

    # ── Generate serial on confirm ─────────────────────────────────────────────
    def button_confirm(self):
        for order in self:
            if not order.serial_number:
                order.serial_number = (
                    self.env['ir.sequence'].next_by_code('purchase.order.serial') or '/'
                )
        return super().button_confirm()

