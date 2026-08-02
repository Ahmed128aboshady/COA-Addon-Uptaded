from odoo import models, fields, api, _
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    # ── Custom expiry (replaces Odoo product_expiry.expiration_date) ──────────
    expiry_date = fields.Date(
        string='Expiry Date',
        copy=False,
        index=True,
        help='Custom expiry date stored directly on this lot/serial number.',
    )

    expiry_status = fields.Selection(
        [('ok', 'Valid'), ('near', 'Expiring Soon'), ('expired', 'Expired')],
        string='Expiry Status',
        compute='_compute_expiry_status',
        store=True,
        index=True,
    )
    days_to_expiry = fields.Integer(
        string='Days to Expiry',
        compute='_compute_expiry_status',
        store=True,
    )
    # Track if notification was sent for this lot
    expiry_notification_sent = fields.Boolean(default=False, copy=False)

    # Useful for expiry report grouping/filtering
    product_category_id = fields.Many2one(
        related='product_id.categ_id',
        store=True,
        string='Product Category',
        index=True,
    )

    # Movement history (done move lines for this lot)
    move_line_ids = fields.One2many(
        'stock.move.line', 'lot_id',
        string='Movement History',
        domain=[('state', '=', 'done')],
    )

    # On-hand qty in INTERNAL locations only (excludes Pre/Post-Production virtual locations)
    internal_product_qty = fields.Float(
        string='On Hand Qty',
        compute='_compute_internal_product_qty',
        search='_search_internal_product_qty',
        help='Quantity in internal storage locations only. '
             'Pre-Production and Post-Production virtual locations are excluded.',
    )

    @api.model
    def _real_stock_location_domain(self):
        """
        Returns a domain fragment for stock.quant that counts ONLY real storage
        locations — i.e. internal locations that are NOT MRP staging areas.

        Pre-Production and Post-Production have usage='internal' in Odoo's MRP
        setup, so we must exclude them explicitly by name pattern.
        """
        # Find all MRP staging locations by name (works regardless of warehouse code)
        staging_locations = self.env['stock.location'].search([
            ('usage', '=', 'internal'),
            '|',
            ('complete_name', 'ilike', 'Pre-Production'),
            ('complete_name', 'ilike', 'Post-Production'),
        ])
        domain = [
            ('location_id.usage', '=', 'internal'),
        ]
        if staging_locations:
            domain.append(('location_id', 'not in', staging_locations.ids))
        return domain

    def _compute_internal_product_qty(self):
        """Sum quant quantities in real internal storage locations only.
        Excludes Pre-Production, Post-Production and virtual/production locations."""
        base_domain = self._real_stock_location_domain()
        quant_data = self.env['stock.quant']._read_group(
            domain=base_domain + [('lot_id', 'in', self.ids)],
            groupby=['lot_id'],
            aggregates=['quantity:sum'],
        )
        qty_by_lot = {lot.id: qty for lot, qty in quant_data}
        for lot in self:
            lot.internal_product_qty = qty_by_lot.get(lot.id, 0.0)

    @api.model
    def _search_internal_product_qty(self, operator, value):
        """Enable domain filtering on internal_product_qty.
        Used by the 'In Stock' filter in the expiry report."""
        base_domain = self._real_stock_location_domain()
        quants = self.env['stock.quant'].search(
            base_domain + [('lot_id', '!=', False)]
        )
        qty_by_lot = {}
        for q in quants:
            qty_by_lot[q.lot_id.id] = qty_by_lot.get(q.lot_id.id, 0.0) + q.quantity

        matching_ids = [
            lot_id for lot_id, qty in qty_by_lot.items()
            if self._evaluate_qty(qty, operator, value)
        ]
        return [('id', 'in', matching_ids)]

    @staticmethod
    def _evaluate_qty(qty, operator, value):
        ops = {
            '>':  qty > value,
            '>=': qty >= value,
            '<':  qty < value,
            '<=': qty <= value,
            '=':  qty == value,
            '!=': qty != value,
        }
        return ops.get(operator, False)

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
        today = date.today()
        for lot in self:
            if not lot.expiry_date:
                lot.expiry_status = 'ok'
                lot.days_to_expiry = 0
                continue
            delta = (lot.expiry_date - today).days
            lot.days_to_expiry = delta
            lot.expiry_status = 'expired' if delta < 0 else ('near' if delta <= 30 else 'ok')

    def _send_po_expiry_notification_if_needed(self):
        """
        Find the originating PO(s) for this lot via stock move lines,
        post a notification on them, and mark this lot as notified.
        """
        self.ensure_one()
        if self.expiry_notification_sent:
            return

        # Trace lot → move lines → picking → purchase order
        move_lines = self.env['stock.move.line'].search([
            ('lot_id', '=', self.id),
            ('picking_id.picking_type_code', '=', 'incoming'),
            ('state', '=', 'done'),
        ])
        purchase_orders = move_lines.mapped('picking_id.purchase_id')

        if not purchase_orders:
            self.expiry_notification_sent = True
            return

        template = self.env.ref(
            'purchase_serial_expiry.mail_template_lot_expiry_notification',
            raise_if_not_found=False,
        )

        for po in purchase_orders:
            if template:
                template.with_context(lot=self).send_mail(po.id, force_send=True)

            po.message_post(
                body=_(
                    '<b>⚠️ Lot Expiry Alert</b><br/>'
                    'Product: <b>%(product)s</b><br/>'
                    'Lot / Batch: <b>%(lot)s</b><br/>'
                    'Expiry Date: <b>%(date)s</b> — <b>%(days)s days remaining</b>',
                    product=self.product_id.display_name,
                    lot=self.name,
                    date=self.expiry_date,
                    days=self.days_to_expiry,
                ),
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )
            po.activity_schedule(
                'mail.mail_activity_data_warning',
                date_deadline=self.expiry_date,
                summary=_('Lot %s expiring soon') % self.name,
                note=_(
                    'Lot %(lot)s of %(product)s expires on %(date)s.',
                    lot=self.name,
                    product=self.product_id.display_name,
                    date=self.expiry_date,
                ),
                user_id=po.user_id.id or self.env.uid,
            )

        self.expiry_notification_sent = True
        _logger.info('Expiry notification sent for lot %s', self.name)

    def action_open_moves(self):
        """Open done stock.move.line records for this lot (movement history)."""
        self.ensure_one()
        list_view = self.env.ref(
            'purchase_serial_expiry.view_lot_move_line_history_list',
            raise_if_not_found=False,
        )
        return {
            'name': _('Movements: %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move.line',
            'view_mode': 'list',
            'views': [(list_view.id if list_view else False, 'list')],
            'domain': [('lot_id', '=', self.id), ('state', '=', 'done')],
            'context': {'create': False, 'delete': False},
            'target': 'current',
        }

    @api.model
    def _cron_send_expiry_notifications(self):
        """Daily cron: notify 30 days before expiry."""
        notify_before = date.today() + timedelta(days=30)
        lots = self.search([
            ('expiry_date', '!=', False),
            ('expiry_date', '<=', fields.Date.to_string(notify_before)),
            ('expiry_notification_sent', '=', False),
        ])
        for lot in lots:
            lot._send_po_expiry_notification_if_needed()
