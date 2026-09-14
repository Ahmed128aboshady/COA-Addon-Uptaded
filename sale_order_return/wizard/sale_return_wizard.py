from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleReturnWizard(models.TransientModel):
    _name = 'sale.return.wizard'
    _description = 'Sale Order Return Wizard'

    sale_id = fields.Many2one('sale.order', string='Sales Order', required=True)
    line_ids = fields.One2many('sale.return.wizard.line', 'wizard_id', string='Products to Return')
    reason = fields.Char(string='Return Reason')
    create_credit_note = fields.Boolean(
        string='Create Credit Note',
        default=True,
        help='Automatically create a draft credit note for the returned products.',
    )

    # ------------------------------------------------------------------ #
    #  Confirm                                                             #
    # ------------------------------------------------------------------ #

    def action_confirm(self):
        self.ensure_one()

        lines_to_return = self.line_ids.filtered(lambda l: l.quantity > 0)
        if not lines_to_return:
            raise UserError(_('Please set a quantity greater than zero for at least one product.'))

        for line in lines_to_return:
            if line.quantity > line.max_qty:
                raise UserError(_(
                    'The return quantity (%(qty)s) for "%(product)s" cannot exceed '
                    'the delivered quantity (%(max)s).',
                    qty=line.quantity,
                    product=line.product_id.display_name,
                    max=line.max_qty,
                ))

        # ── 1. Create return picking(s) ─────────────────────────────────
        # Use sudo() for all stock operations because salespeople do not
        # have warehouse / inventory access rights.
        lines_by_picking = {}
        for line in lines_to_return:
            lines_by_picking.setdefault(line.picking_id, []).append(line)

        new_pickings = self.env['stock.picking']
        for picking, lines in lines_by_picking.items():
            ctx = {'active_id': picking.id, 'active_model': 'stock.picking'}
            return_wizard = self.env['stock.return.picking'].sudo().with_context(**ctx).create(
                {'picking_id': picking.id}
            )
            for ret_line in return_wizard.product_return_moves:
                matched = next(
                    (l for l in lines if l.product_id == ret_line.product_id), None
                )
                ret_line.quantity = matched.quantity if matched else 0
                if matched:
                    ret_line.to_refund = matched.to_refund

            new_picking = return_wizard._create_return()
            if self.reason:
                new_picking.note = self.reason
            new_pickings |= new_picking

        # ── 2. Optionally create a credit note ──────────────────────────
        credit_note = None
        if self.create_credit_note:
            credit_note = self._create_credit_note(new_pickings)

        # ── 3. Open the credit note if created, else the return picking ─
        if credit_note:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Credit Note'),
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': credit_note.id,
                'target': 'current',
            }

        if len(new_pickings) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Return Transfer'),
                'res_model': 'stock.picking',
                'view_mode': 'form',
                'res_id': new_pickings.id,
                'target': 'current',
            }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Return Transfers'),
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('id', 'in', new_pickings.ids)],
            'target': 'current',
        }

    # ------------------------------------------------------------------ #
    #  Credit note helper                                                  #
    # ------------------------------------------------------------------ #

    def _create_credit_note(self, return_pickings):
        """Create a draft credit note whose quantities are read directly from
        the return picking moves — not from the wizard lines or the sale order
        line demand — so the note always matches exactly what was physically
        returned in the delivery."""
        sale = self.sale_id

        # Aggregate returned qty per product across all return pickings
        # (product_uom_qty is the demanded qty on the return move, set by
        #  stock.return.picking from the wizard's quantities)
        returned_qty = {}   # {product: qty_in_sale_uom}
        for picking in return_pickings:
            for move in picking.move_ids.filtered(lambda m: m.product_uom_qty > 0):
                product = move.product_id
                # Convert from move UoM to sale UoM if they differ
                qty = move.product_uom._compute_quantity(
                    move.product_uom_qty,
                    move.product_id.uom_id,
                )
                returned_qty[product] = returned_qty.get(product, 0.0) + qty

        if not returned_qty:
            return None

        # Build credit note from the sale order's own invoice template so
        # that journal, currency, fiscal position, payment terms, etc. are
        # all inherited correctly.
        invoice_vals = sale._prepare_invoice()
        invoice_vals['move_type'] = 'out_refund'
        invoice_vals['invoice_origin'] = _('Return of %s') % sale.name
        invoice_vals['invoice_line_ids'] = []

        for product, qty in returned_qty.items():
            sale_line = sale.order_line.filtered(
                lambda l: l.product_id == product and not l.display_type
            )[:1]

            if not sale_line:
                continue

            # _prepare_invoice_line gives correct account, taxes, analytic, etc.
            line_vals = sale_line._prepare_invoice_line()
            # Override quantity with the ACTUAL returned qty from the picking
            line_vals['quantity'] = qty
            invoice_vals['invoice_line_ids'].append((0, 0, line_vals))

        if not invoice_vals['invoice_line_ids']:
            return None

        return self.env['account.move'].sudo().create(invoice_vals)


# ------------------------------------------------------------------ #
#  Wizard line                                                         #
# ------------------------------------------------------------------ #

class SaleReturnWizardLine(models.TransientModel):
    _name = 'sale.return.wizard.line'
    _description = 'Sale Order Return Wizard Line'

    wizard_id = fields.Many2one('sale.return.wizard', required=True, ondelete='cascade')

    # Written server-side in action_return() — never sent by the client.
    picking_id = fields.Many2one('stock.picking', string='Delivery')
    product_id = fields.Many2one('product.product', string='Product')
    uom_id = fields.Many2one('uom.uom', string='Unit')
    max_qty = fields.Float(string='Delivered', digits='Product Unit of Measure')

    # Editable by the user
    quantity = fields.Float(string='Return Qty', digits='Product Unit of Measure')
    to_refund = fields.Boolean(
        string='To Refund',
        default=True,
        help='Deduct from invoiced quantity so a credit note can be created.',
    )
