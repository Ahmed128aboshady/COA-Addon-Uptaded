# -*- coding: utf-8 -*-
import logging

from odoo import _, fields, models
from odoo.tools import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        """After the picking is done:
        - If the linked Sale Order has a POSTED invoice  → create a draft Credit Note.
        - If the linked Sale Order has only a DRAFT invoice → reduce its quantities.
        """
        res = super()._action_done()
        for picking in self:
            try:
                picking._coa_handle_return_invoice()
            except Exception as err:
                _logger.warning(
                    "COA: could not process invoice on return for "
                    "picking %s: %s", picking.name, err, exc_info=True)
        return res

    # ------------------------------------------------------------------
    # Helper: resolve Sale Order from a return move (multi-delivery safe)
    # ------------------------------------------------------------------

    def _coa_resolve_order_and_sale_line(self, move):
        """
        Return (sale.order, sale.order.line | empty) for a return move.

        Lookup priority (most-reliable first):

          1. sale_id on the ORIGINAL delivery picking
             → always set by Odoo regardless of backorders / split deliveries.
          2. sale_line_id on the original delivery move
          3. sale_line_id on the return move itself
          4. Fallback: match product in the order lines

        This handles the common case where a second delivery (backorder) has
        its move.sale_line_id empty because the line was already fulfilled
        by an earlier delivery.
        """
        orig_move = move.origin_returned_move_id

        # ── 1. Sale Order via the original delivery picking ──────────────
        order = orig_move.picking_id.sale_id if orig_move else False

        # ── 2-3. Sale Order via sale_line_id ────────────────────────────
        if not order:
            sale_line = orig_move.sale_line_id or move.sale_line_id
            order = sale_line.order_id if sale_line else False

        if not order:
            return False, False

        # ── Sale line: try direct link first, then product match ─────────
        sale_line = (
            (orig_move.sale_line_id if orig_move else False)
            or move.sale_line_id
            or order.order_line.filtered(
                lambda l, m=move: l.product_id == m.product_id
            )[:1]
        )

        return order, sale_line

    # ------------------------------------------------------------------
    # Main dispatcher
    # ------------------------------------------------------------------

    def _coa_handle_return_invoice(self):
        self.ensure_one()

        return_moves = self.move_ids.filtered(
            lambda m: m.origin_returned_move_id
            and m.state == 'done'
            and m.quantity > 0
        )
        if not return_moves:
            return

        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')

        # Group return moves by sale order
        order_moves = {}
        for move in return_moves:
            order, sale_line = self._coa_resolve_order_and_sale_line(move)
            if not order:
                _logger.info(
                    "COA: no Sale Order found for return move %s "
                    "(product: %s) in picking %s – skipped.",
                    move.id, move.product_id.display_name, self.name)
                continue
            if order.id not in order_moves:
                order_moves[order.id] = {'order': order, 'pairs': []}
            order_moves[order.id]['pairs'].append((move, sale_line))

        for data in order_moves.values():
            order = data['order']
            pairs = data['pairs']

            posted_invoices = order.invoice_ids.filtered(
                lambda inv: inv.state == 'posted'
                and inv.move_type == 'out_invoice'
            )
            draft_invoices = order.invoice_ids.filtered(
                lambda inv: inv.state == 'draft'
                and inv.move_type == 'out_invoice'
            )

            if posted_invoices:
                self._coa_create_draft_credit_note(
                    order, posted_invoices[0], pairs, precision)
            elif draft_invoices:
                self._coa_adjust_draft_invoices(
                    draft_invoices, pairs, precision)
            else:
                _logger.info(
                    "COA: No invoice found for order %s on return %s – skipped.",
                    order.name, self.name)

    # ------------------------------------------------------------------
    # Case 1 – Posted invoice  →  create draft Credit Note
    # ------------------------------------------------------------------

    def _coa_create_draft_credit_note(self, order, source_invoice,
                                      pairs, precision):
        """Create a DRAFT credit note for the returned products."""
        invoice_line_vals = []

        for move, sale_line in pairs:
            # Try to match a line in the source invoice
            inv_lines = source_invoice.invoice_line_ids.filtered(
                lambda l, m=move: l.product_id == m.product_id
                and not float_is_zero(l.quantity, precision_digits=precision)
            )

            if inv_lines:
                inv_line = inv_lines[0]
                qty_in_line_uom = move.product_uom._compute_quantity(
                    move.quantity, inv_line.product_uom_id)
                line_vals = {
                    'product_id': move.product_id.id,
                    'quantity': qty_in_line_uom,
                    'product_uom_id': inv_line.product_uom_id.id,
                    'price_unit': inv_line.price_unit,
                    'discount': inv_line.discount,
                    'tax_ids': [(6, 0, inv_line.tax_ids.ids)],
                    'account_id': inv_line.account_id.id,
                    'name': inv_line.name or move.product_id.display_name,
                }
                if sale_line:
                    line_vals['sale_line_ids'] = [(4, sale_line.id)]
                invoice_line_vals.append((0, 0, line_vals))
            else:
                # Fallback: product not found on invoice – use product defaults
                product = move.product_id.with_context(
                    lang=order.partner_id.lang)
                line_vals = {
                    'product_id': product.id,
                    'quantity': move.quantity,
                    'product_uom_id': move.product_uom.id,
                    'price_unit': product.lst_price,
                    'name': product.display_name,
                }
                if sale_line:
                    line_vals['sale_line_ids'] = [(4, sale_line.id)]
                invoice_line_vals.append((0, 0, line_vals))

        if not invoice_line_vals:
            return

        credit_note = self.env['account.move'].create({
            'move_type': 'out_refund',
            'partner_id': order.partner_invoice_id.id,
            'currency_id': source_invoice.currency_id.id,
            'journal_id': source_invoice.journal_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.name,
            'reversed_entry_id': source_invoice.id,
            'invoice_line_ids': invoice_line_vals,
        })

        credit_note.message_post(body=_(
            "Draft credit note automatically created (COA) "
            "for stock return %(picking)s – linked to invoice %(invoice)s.",
            picking=self.name,
            invoice=source_invoice.name,
        ))
        source_invoice.message_post(body=_(
            "A draft credit note %(cn)s was automatically created (COA) "
            "following stock return %(picking)s.",
            cn=credit_note.name,
            picking=self.name,
        ))
        _logger.info(
            "COA: created draft credit note %s for return picking %s",
            credit_note.name, self.name)

    # ------------------------------------------------------------------
    # Case 2 – Draft invoice  →  reduce quantities
    # ------------------------------------------------------------------

    def _coa_adjust_draft_invoices(self, draft_invoices, pairs, precision):
        """Reduce line quantities on DRAFT invoices for returned products."""
        for move, sale_line in pairs:
            remaining = move.quantity

            for invoice in draft_invoices:
                if float_is_zero(remaining, precision_digits=precision):
                    break

                # Match by sale_line if available, otherwise by product only
                if sale_line:
                    inv_lines = invoice.invoice_line_ids.filtered(
                        lambda l, m=move, sl=sale_line:
                        l.product_id == m.product_id
                        and sl in l.sale_line_ids
                        and l.quantity > 0
                    )
                    # Fallback to product-only match if sale_line match fails
                    if not inv_lines:
                        inv_lines = invoice.invoice_line_ids.filtered(
                            lambda l, m=move:
                            l.product_id == m.product_id
                            and l.quantity > 0
                        )
                else:
                    inv_lines = invoice.invoice_line_ids.filtered(
                        lambda l, m=move:
                        l.product_id == m.product_id
                        and l.quantity > 0
                    )

                if not inv_lines:
                    continue

                adjusted = False
                for line in inv_lines:
                    if float_is_zero(remaining, precision_digits=precision):
                        break

                    remaining_in_line_uom = move.product_uom._compute_quantity(
                        remaining, line.product_uom_id)
                    if float_compare(remaining_in_line_uom, 0,
                                     precision_digits=precision) <= 0:
                        break

                    reduce_qty = min(line.quantity, remaining_in_line_uom)
                    new_qty = line.quantity - reduce_qty

                    reduced_in_move_uom = line.product_uom_id._compute_quantity(
                        reduce_qty, move.product_uom)
                    remaining -= reduced_in_move_uom

                    if float_is_zero(new_qty, precision_digits=precision):
                        line.unlink()
                    else:
                        line.quantity = new_qty
                    adjusted = True

                if adjusted:
                    invoice.message_post(body=_(
                        "Draft invoice automatically adjusted (COA): "
                        "returned %(qty)s × %(product)s via return %(picking)s.",
                        qty=move.quantity,
                        product=move.product_id.display_name,
                        picking=self.name,
                    ))
