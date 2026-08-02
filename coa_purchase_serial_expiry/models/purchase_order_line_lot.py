from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLineLot(models.Model):
    """
    Kept for the notification cron: reads lot expiry data from stock.lot
    linked to PO receipts. The actual data entry is now on the receipt move lines.
    """
    _name = 'purchase.order.line.lot'
    _description = 'Purchase Order Line – Lot & Expiry (legacy link)'
    _order = 'expiry_date asc'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', required=True, ondelete='cascade', index=True,
    )
    purchase_id = fields.Many2one(
        related='purchase_line_id.order_id', store=True, index=True,
    )
    product_id = fields.Many2one(
        related='purchase_line_id.product_id', store=True,
    )
    lot_name = fields.Char(string='Lot / Batch #')
    qty = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one(related='purchase_line_id.product_uom_id')
    expiry_date = fields.Date(string='Expiry Date')
    expiry_status = fields.Selection(
        [('ok', 'Valid'), ('near', 'Expiring Soon'), ('expired', 'Expired')],
        compute='_compute_expiry_status', store=True,
    )
    days_to_expiry = fields.Integer(compute='_compute_expiry_status', store=True)
    notification_sent = fields.Boolean(default=False, copy=False)
    stock_lot_id = fields.Many2one('stock.lot', readonly=True, copy=False)

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
        today = date.today()
        for rec in self:
            if not rec.expiry_date:
                rec.expiry_status = 'ok'
                rec.days_to_expiry = 0
                continue
            delta = (rec.expiry_date - today).days
            rec.days_to_expiry = delta
            rec.expiry_status = 'expired' if delta < 0 else ('near' if delta <= 30 else 'ok')

    @api.model
    def _cron_send_expiry_notifications(self):
        """
        Primary cron: scans stock.lot records linked to POs for expiry alerts.
        Uses our custom expiry_date field on stock.lot.
        """
        notify_before = date.today() + timedelta(days=30)
        lots = self.env['stock.lot'].search([
            ('expiry_date', '!=', False),
            ('expiry_date', '<=', fields.Date.to_string(notify_before)),
            ('expiry_notification_sent', '=', False),
        ])
        for lot in lots:
            lot._send_po_expiry_notification_if_needed()
