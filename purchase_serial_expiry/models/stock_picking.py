from odoo import models, api, fields, _
from odoo.exceptions import UserError
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code == 'incoming':
                # ── 1. Auto-generate lot names first (before any checks) ───────
                #    This ensures the expiry check can reference the lot name,
                #    and the user sees a meaningful lot in the error message.
                picking._auto_generate_lot_names()
                # ── 2. Block if product requires expiry but it's missing ───────
                picking._check_expiry_required()
                # ── 3. Create/update lots with our custom expiry date ──────────
                for ml in picking.move_line_ids:
                    if ml.expiry_date_input:
                        ml._create_and_assign_lot()

            elif picking.picking_type_code in ('outgoing', 'internal'):
                # ── 4. Auto-sort move lines FIFO before validate ───────────────
                picking._sort_move_lines_fifo()

        # Do NOT skip _sanity_check — our override (below) generates missing lot
        # names BEFORE super()._sanity_check() runs, so the check will pass.
        return super().button_validate()

    def _auto_generate_lot_names(self):
        """
        Generate lot names early (before _check_expiry_required) for all
        tracked incoming move lines that still have no lot_id / lot_name.
        This makes lot numbers visible in error messages and in Detailed Ops.
        """
        self.ensure_one()
        for ml in self.move_line_ids:
            if (ml.product_id.tracking in ('lot', 'serial')
                    and not ml.lot_id and not ml.lot_name
                    and ml.quantity > 0):
                ml.lot_name = (
                    self.env['ir.sequence'].next_by_code('stock.lot.serial')
                    or 'LOT/%s' % fields.Datetime.now().strftime('%Y%m%d%H%M%S')
                )
                _logger.info(
                    'Auto lot (early): %s for %s on %s',
                    ml.lot_name, ml.product_id.display_name, self.name,
                )

    def _sanity_check(self, separate_pickings=True):
        """
        Before running the standard sanity check, auto-generate lot/serial names
        for incoming move lines that:
          - belong to a tracked product
          - do NOT require manual expiry entry
          - have no lot_id and no lot_name yet
          - have a quantity > 0 (done or demand)

        We check BOTH move_line_ids (Detailed Operations rows) and fall back
        to move_ids demand so that immediate-transfer receipts (where the user
        never opened Detailed Operations) are also handled.

        This runs BEFORE super()._sanity_check(), so the standard lot check
        will find the auto-generated lot_name and pass.
        """
        for picking in self.filtered(lambda p: p.picking_type_code == 'incoming'):
            # ── Detailed Operations rows ──────────────────────────────────────
            for ml in picking.move_line_ids:
                if (ml.product_id.tracking in ('lot', 'serial')
                        and not ml.lot_id
                        and not ml.lot_name
                        and ml.quantity > 0):
                    ml.lot_name = (
                        self.env['ir.sequence'].next_by_code('stock.lot.serial')
                        or 'LOT/%s' % fields.Datetime.now().strftime('%Y%m%d%H%M%S')
                    )
                    _logger.info(
                        'Auto lot (sanity, ml): %s for %s on %s',
                        ml.lot_name, ml.product_id.display_name, picking.name,
                    )

            # ── Moves without detail lines yet (immediate transfer) ───────────
            # Odoo will create move lines from these demands; pre-create them
            # now so the sanity check and lot assignment both work.
            # NOTE: we generate lot names for ALL tracked products, including
            # requires_expiry_on_purchase ones — the user only needs to fill
            # in the expiry date; the lot name is pre-filled automatically.
            for move in picking.move_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
                if move.product_id.tracking not in ('lot', 'serial'):
                    continue
                if move.move_line_ids:
                    continue  # already handled above
                # No move lines at all → create one with auto lot
                qty = move.product_uom_qty
                if qty <= 0:
                    continue
                lot_name = (
                    self.env['ir.sequence'].next_by_code('stock.lot.serial')
                    or 'LOT/%s' % fields.Datetime.now().strftime('%Y%m%d%H%M%S')
                )
                self.env['stock.move.line'].create({
                    'move_id': move.id,
                    'picking_id': picking.id,
                    'product_id': move.product_id.id,
                    'product_uom_id': move.product_uom.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'quantity': qty,
                    'lot_name': lot_name,
                })
                _logger.info(
                    'Auto lot (sanity, move): %s for %s on %s',
                    lot_name, move.product_id.display_name, picking.name,
                )

        return super()._sanity_check(separate_pickings)

    def action_assign(self):
        """
        After standard reservation, apply FIFO lot ordering for tracked products
        in outgoing/internal pickings (deliveries, component picks for MO, etc.).
        Products with requires_expiry_on_purchase are sorted by expiry_date ASC.
        Other tracked products are sorted by lot id ASC (oldest lot first).
        """
        result = super().action_assign()
        for picking in self.filtered(
                lambda p: p.picking_type_code in ('outgoing', 'internal')
                and p.state in ('assigned', 'partially_available')):
            picking._sort_move_lines_fifo()
        return result

    # ── Block validation if required expiry date is missing ───────────────────
    def _check_expiry_required(self):
        self.ensure_one()
        missing = []
        for ml in self.move_line_ids:
            if not ml.product_id.requires_expiry_on_purchase:
                continue
            # Allow if expiry already on the lot or entered on this line
            if ml.expiry_date_input or (ml.lot_id and ml.lot_id.expiry_date):
                continue
            missing.append(
                '• %s (Lot: %s)' % (
                    ml.product_id.display_name,
                    ml.lot_name or (ml.lot_id.name if ml.lot_id else _('no lot')),
                )
            )
        if missing:
            raise UserError(
                _('Cannot validate receipt. The following products require an Expiry Date:\n\n%s\n\n'
                  'Please fill in the Expiry Date in the Detailed Operations tab.')
                % '\n'.join(missing)
            )

    # ── FIFO sort: reorder Detailed Operations by lot expiry ASC ─────────────
    def _sort_move_lines_fifo(self):
        """
        For each stock.move, redistribute quantities across lots using FIFO:
        - Products with requires_expiry_on_purchase → sorted by expiry_date ASC
        - Other tracked products → sorted by lot.id ASC (oldest lot first)

        Rules:
        • Respects the move's source location — uses exact quant location in each
          new move line so the system never changes the location silently.
        • If no lots exist in the source location, leaves existing move lines
          untouched (does NOT create lines with a different location).
        • Replaces existing move lines only when FIFO quants are found.
        """
        self.ensure_one()
        for move in self.move_ids:
            product = move.product_id
            if product.tracking not in ('lot', 'serial'):
                continue
            if move.state == 'done':
                continue

            existing_mls = move.move_line_ids
            if not existing_mls:
                continue

            needed_qty = move.product_uom_qty
            location = move.location_id

            # ── Search only in the move's source location (and its children).
            #    We will use quant.location_id.id (the real sub-location) when
            #    creating each move line — this prevents silent location changes.
            quants = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id', 'child_of', location.id),
                ('location_id.usage', '=', 'internal'),
                ('quantity', '>', 0),
                ('lot_id', '!=', False),
            ])

            if not quants:
                # No lots available in source location → leave as-is
                _logger.info(
                    'FIFO: no lots found in %s for %s on %s — skipping',
                    location.display_name, product.display_name, self.name,
                )
                continue

            if product.requires_expiry_on_purchase:
                quants_sorted = quants.sorted(
                    key=lambda q: q.lot_id.expiry_date or date(9999, 12, 31)
                )
            else:
                quants_sorted = quants.sorted(key=lambda q: q.lot_id.id)

            remaining = needed_qty
            ml_vals_list = []
            for quant in quants_sorted:
                if remaining <= 0:
                    break
                take = min(quant.quantity, remaining)
                ml_vals_list.append({
                    'move_id': move.id,
                    'product_id': product.id,
                    'product_uom_id': move.product_uom.id,
                    # ↓ actual sub-location where the lot physically sits
                    'location_id': quant.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'lot_id': quant.lot_id.id,
                    'quantity': take,
                    'picking_id': self.id,
                })
                remaining -= take
                _logger.info(
                    'FIFO: lot %s (expiry %s) qty %.2f from %s for %s on %s',
                    quant.lot_id.name, quant.lot_id.expiry_date,
                    take, quant.location_id.display_name,
                    product.display_name, self.name,
                )

            if ml_vals_list:
                existing_mls.unlink()
                self.env['stock.move.line'].create(ml_vals_list)
