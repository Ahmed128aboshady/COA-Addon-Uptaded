from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    return_count = fields.Integer(
        string='Returns',
        compute='_compute_return_count',
    )

    @api.depends('picking_ids', 'picking_ids.state', 'picking_ids.picking_type_code')
    def _compute_return_count(self):
        for order in self:
            order.return_count = len(order._get_return_pickings())

    def _get_return_pickings(self):
        """Return incoming pickings linked to this sale order (i.e. returns)."""
        return self.picking_ids.filtered(
            lambda p: p.picking_type_code == 'incoming'
        )

    def action_return(self):
        """Create the wizard record server-side (with all lines in DB) then open it."""
        self.ensure_one()

        done_pickings = self.picking_ids.filtered(
            lambda p: p.state == 'done' and p.picking_type_code == 'outgoing'
        )
        if not done_pickings:
            raise UserError(_('There are no delivered products to return on this order.'))

        # ── Create the wizard in the DB first ──────────────────────────────
        # This guarantees that line fields (product_id, picking_id, max_qty …)
        # are persisted before the dialog opens.  Odoo's web client does NOT
        # reliably send readonly/invisible fields back when submitting a brand-
        # new wizard form, so we must not rely on default_get + client round-trip.
        #
        # sudo() is used to read stock data because salespeople do not have
        # warehouse / inventory access rights.
        wizard = self.env['sale.return.wizard'].create({'sale_id': self.id})

        line_vals = []
        for picking in done_pickings.sudo():
            for move in picking.move_ids.filtered(
                lambda m: m.state == 'done' and m.product_id.type != 'service'
            ):
                done_qty = sum(move.move_line_ids.mapped('quantity'))
                if done_qty <= 0:
                    continue
                line_vals.append({
                    'wizard_id': wizard.id,
                    'picking_id': picking.id,
                    'product_id': move.product_id.id,
                    'uom_id': move.product_uom.id,
                    'max_qty': done_qty,
                    'quantity': done_qty,
                    'to_refund': True,
                })

        if line_vals:
            self.env['sale.return.wizard.line'].create(line_vals)

        # ── Open the already-saved wizard by ID ────────────────────────────
        return {
            'type': 'ir.actions.act_window',
            'name': _('Return Products'),
            'res_model': 'sale.return.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }

    def action_view_returns(self):
        """Open the return deliveries for this sales order."""
        self.ensure_one()
        return_pickings = self._get_return_pickings()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Returns'),
            'res_model': 'stock.picking',
            'domain': [('id', 'in', return_pickings.ids)],
        }
        if len(return_pickings) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = return_pickings.id
        else:
            action['view_mode'] = 'list,form'
        return action
