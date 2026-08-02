from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date as date_type
import logging

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    """
    Extend stock.quant for Physical Inventory adjustments:

    inventory_expiry_date  — a standalone Date field shown in the inventory list.

    Behaviour on Apply:
    • Positive diff (adding stock) with no lot:
        → auto-create a new lot (serial from sequence) with inventory_expiry_date
        → mandatory if product has requires_expiry_on_purchase=True
    • Negative diff (reducing stock) with no lot:
        → auto-FIFO: pull from lots sorted by expiry_date ASC (oldest first)
    • Existing lot row:
        → if inventory_expiry_date is changed, sync back to lot.expiry_date
    """
    _inherit = 'stock.quant'

    inventory_expiry_date = fields.Date(
        string='Expiry Date',
        help='• Adding stock (no lot): enter the expiry date — a lot is created automatically.\n'
             '• Reducing stock (no lot): leave empty — the system pulls from the oldest lot (FIFO).\n'
             '• Existing lot row: shows/edits that lot\'s expiry date.',
    )

    def _get_inventory_fields_write(self):
        """Allow inventory_expiry_date to be set when creating/editing quants
        in inventory mode (Physical Inventory). Without this, Odoo raises
        'Quant's creation is restricted' when the column is filled."""
        return super()._get_inventory_fields_write() + ['inventory_expiry_date']

    @api.onchange('lot_id')
    def _onchange_lot_id_prefill_expiry(self):
        """Pre-fill the expiry date field when user selects an existing lot."""
        if self.lot_id and self.lot_id.expiry_date:
            self.inventory_expiry_date = self.lot_id.expiry_date

    def write(self, vals):
        res = super().write(vals)
        # Keep lot.expiry_date in sync when user edits the inventory expiry date
        if vals.get('inventory_expiry_date') and 'lot_id' not in vals:
            for quant in self.filtered(lambda q: q.lot_id):
                quant.lot_id.expiry_date = vals['inventory_expiry_date']
        return res

    def action_apply_inventory(self, date=None):
        """
        Before applying inventory:
        1. No-lot rows with positive diff  → auto-create lot (+ expiry)
        2. No-lot rows with negative diff  → FIFO reduction across existing lots
        3. Lot rows with inventory_expiry_date changed → already synced via write()
        """
        handled_ids = set()

        for quant in self:
            product = quant.product_id
            if not product or product.tracking == 'none':
                continue
            if not quant.inventory_quantity_set:
                continue
            if quant.lot_id:
                # Standard flow handles lot-specific rows
                continue

            diff = quant.inventory_diff_quantity

            # ── Case 1: Adding stock, no lot ──────────────────────────────────
            if diff > 0:
                if product.requires_expiry_on_purchase and not quant.inventory_expiry_date:
                    raise UserError(
                        _('Cannot apply inventory.\n\n'
                          'Product "%s" requires an Expiry Date.\n'
                          'Please fill in the Expiry Date column.')
                        % product.display_name
                    )
                lot_name = (
                    self.env['ir.sequence'].next_by_code('stock.lot.serial')
                    or 'ADJ/%s' % fields.Datetime.now().strftime('%Y%m%d%H%M%S')
                )
                lot = self.env['stock.lot'].create({
                    'name': lot_name,
                    'product_id': product.id,
                    'company_id': quant.company_id.id,
                    'expiry_date': quant.inventory_expiry_date or False,
                })
                # In Odoo 19, lot_id is in _get_forbidden_fields_write() so we
                # must bypass inventory_mode to set it on the quant.
                quant.with_context(inventory_mode=False).write({'lot_id': lot.id})
                _logger.info(
                    'Inventory: auto-created lot %s (expiry %s) for %s',
                    lot_name, quant.inventory_expiry_date, product.display_name,
                )
                # Now has lot_id → standard flow will process it via super()

            # ── Case 2: Reducing stock, no lot → FIFO ─────────────────────────
            elif diff < 0:
                reduction = abs(diff)

                # Find all quants for this product/location with a lot
                lot_quants = self.env['stock.quant'].search([
                    ('product_id', '=', product.id),
                    ('location_id', '=', quant.location_id.id),
                    ('lot_id', '!=', False),
                    ('quantity', '>', 0),
                ])
                # Sort by expiry_date ASC (oldest/nearest expiry first), no expiry → last
                lot_quants_sorted = lot_quants.sorted(
                    key=lambda q: q.lot_id.expiry_date or date_type(9999, 12, 31)
                )

                for lq in lot_quants_sorted:
                    if reduction <= 0:
                        break
                    take = min(lq.quantity, reduction)
                    # Set inventory_quantity on the lot's quant and apply directly
                    lq.inventory_quantity = lq.quantity - take
                    lq._apply_inventory(date)
                    reduction -= take
                    _logger.info(
                        'Inventory FIFO: consumed %.2f from lot %s (expiry %s) for %s',
                        take, lq.lot_id.name, lq.lot_id.expiry_date, product.display_name,
                    )

                if reduction > 0:
                    raise UserError(
                        _('Cannot reduce %.2f units of "%s" — not enough stock across all lots.')
                        % (abs(diff), product.display_name)
                    )

                # Don't pass this no-lot row to the standard flow
                quant.inventory_quantity_set = False
                handled_ids.add(quant.id)

        # Pass all rows except the FIFO-handled ones to the standard flow
        remaining = self.filtered(lambda q: q.id not in handled_ids)
        if remaining:
            return super(StockQuant, remaining).action_apply_inventory(date=date)
        return True
