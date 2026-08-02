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
                # sudo(): warehouse users usually have NO access rights on
                # account.move. The invoice adjustment / credit note is a
                # system-triggered action, so we elevate rights here.
                # Traceability is kept: chatter author remains the real user.
                picking.sudo()._coa_handle_return_invoice()
            except Exception as err:
                _logger.warning(
                    "COA: could not process invoice on return for "
                    "picking %s: %s", picking.name, err, exc_info=True)
                # Alert accounting so the return is handled manually
                try:
                    picking.sudo().message_post(
                        body=_(
                            "COA: automatic invoice adjustment for this "
                            "return FAILED (%(error)s). Accounting must "
                            "handle the invoice/credit note manually.",
                            error=err,
                        ),
                        partner_ids=picking.sudo()
                        ._coa_accounting_notify_partners().ids,
                        subtype_xmlid='mail.mt_comment',
                    )
                except Exception:
                    _logger.exception(
                        "COA: could not notify accounting for picking %s",
                        picking.name)
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
    # Helper: accounting users to notify
    # ------------------------------------------------------------------

    def _coa_accounting_notify_partners(self):
        """Partners of ALL internal users having any Accounting access.

        Odoo accounting groups are hierarchical (Manager implies
        Accountant implies Billing...), so we union the base groups to
        catch everyone: Read-only, Billing, Accountant, and Manager.
        """
        group_xmlids = [
            'account.group_account_readonly',
            'account.group_account_invoice',
            'account.group_account_user',
            'account.group_account_manager',
        ]
        users = self.env['res.users']
        for xmlid in group_xmlids:
            group = self.env.ref(xmlid, raise_if_not_found=False)
            if group:
                users |= group.users
        users = users.filtered(lambda u: u.active and not u.share)
        return users.partner_id

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

            # Split pairs by invoice policy on the product
            #
            # 'order'    → invoice is for the committed ORDERED qty.
            #              A return ALWAYS generates a credit note —
            #              we never reduce the draft invoice because it
            #              already reflects the full order commitment.
            #
            # 'delivery' → invoice is for what was actually delivered.
            #              If still draft we reduce it; if posted we CN.
            ordered_pairs  = [(m, sl) for m, sl in pairs
                              if m.product_id.invoice_policy == 'order']
            delivery_pairs = [(m, sl) for m, sl in pairs
                              if m.product_id.invoice_policy != 'order']

            # ── ordered-qty policy ───────────────────────────────────────
            if ordered_pairs:
                source = posted_invoices[0] if posted_invoices else (
                    draft_invoices[0] if draft_invoices else None
                )
                if source:
                    self._coa_create_draft_credit_note(
                        order, source, ordered_pairs, precision)
                else:
                    _logger.info(
                        "COA: No invoice for order %s (ordered-qty) "
                        "– credit note skipped.", order.name)

            # ── delivery policy ──────────────────────────────────────────
            if delivery_pairs:
                if posted_invoices:
                    self._coa_create_draft_credit_note(
                        order, posted_invoices[0], delivery_pairs, precision)
                elif draft_invoices:
                    self._coa_adjust_draft_invoices(
                        draft_invoices, delivery_pairs, precision)
                else:
                    _logger.info(
                        "COA: No invoice for order %s (delivery-qty) "
                        "– skipped.", order.name)

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

        cn_vals = {
            'move_type': 'out_refund',
            'partner_id': order.partner_invoice_id.id,
            'currency_id': source_invoice.currency_id.id,
            'journal_id': source_invoice.journal_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': '%s (%s)' % (self.name, source_invoice.name),
            'invoice_line_ids': invoice_line_vals,
        }
        # Link to source only when it is NOT fully reconciled.
        # Paid / in-payment invoices may trigger reconciliation
        # constraints when set as reversed_entry_id.
        if (source_invoice.state == 'posted'
                and source_invoice.payment_state
                not in ('paid', 'in_payment', 'reversed')):
            cn_vals['reversed_entry_id'] = source_invoice.id

        credit_note = self.env['account.move'].create(cn_vals)

        paid_note = ''
        if source_invoice.payment_state in ('paid', 'in_payment'):
            paid_note = _(
                " Note: the source invoice is already paid — "
                "manual reconciliation may be needed.")

        credit_note.message_post(
            body=_(
                "Draft credit note automatically created (COA) "
                "for stock return %(picking)s – linked to invoice %(invoice)s. "
                "Please review and post it.",
                picking=self.name,
                invoice=source_invoice.name,
            ) + paid_note,
            partner_ids=self._coa_accounting_notify_partners().ids,
            subtype_xmlid='mail.mt_comment',
        )
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
                    invoice.message_post(
                        body=_(
                            "Draft invoice automatically adjusted (COA): "
                            "returned %(qty)s × %(product)s via return "
                            "%(picking)s. Please review before posting.",
                            qty=move.quantity,
                            product=move.product_id.display_name,
                            picking=self.name,
                        ),
                        partner_ids=self._coa_accounting_notify_partners().ids,
                        subtype_xmlid='mail.mt_comment',
                    )
