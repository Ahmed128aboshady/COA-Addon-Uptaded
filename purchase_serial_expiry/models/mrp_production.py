from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    serial_number = fields.Char(
        string='Serial #',
        readonly=True,
        copy=False,
        index=True,
    )

    earliest_component_expiry = fields.Date(
        string='Earliest Component Expiry',
        compute='_compute_component_expiry',
        store=False,
    )
    component_expiry_status = fields.Selection(
        [('ok', 'Valid'), ('near', 'Expiring Soon'), ('expired', 'Expired'), ('none', 'No Lots')],
        string='Component Expiry Status',
        compute='_compute_component_expiry',
        store=False,
    )

    @api.depends('move_raw_ids.move_line_ids.lot_id.expiry_date', 'state')
    def _compute_component_expiry(self):
        from datetime import date
        today = date.today()
        for mo in self:
            dates = [
                ml.lot_id.expiry_date
                for move in mo.move_raw_ids
                for ml in move.move_line_ids
                if ml.lot_id and ml.lot_id.expiry_date
            ]
            if not dates:
                mo.earliest_component_expiry = False
                mo.component_expiry_status = 'none'
                continue
            earliest = min(dates)
            mo.earliest_component_expiry = earliest
            delta = (earliest - today).days
            mo.component_expiry_status = (
                'expired' if delta < 0 else ('near' if delta <= 30 else 'ok')
            )

    def action_confirm(self):
        for mo in self:
            if not mo.serial_number:
                mo.serial_number = (
                    self.env['ir.sequence'].next_by_code('mrp.production.serial') or '/'
                )
        return super().action_confirm()

    def action_assign(self):
        """Check Availability: reserve stock then immediately assign FIFO lots
        so lot numbers and expiry dates are visible before the user presses Validate."""
        result = super().action_assign()
        for mo in self.filtered(lambda m: m.state in ('confirmed', 'progress', 'to_close')):
            mo._assign_fifo_lots_to_components()
        return result

    def button_mark_done(self):
        """Before finalising MO, ensure FIFO lots are assigned (safety net)."""
        for mo in self:
            mo._assign_fifo_lots_to_components()
        return super().button_mark_done()

    def _action_generate_immediate_wizard(self):
        for mo in self:
            mo._assign_fifo_lots_to_components()
        return super()._action_generate_immediate_wizard()

    def _assign_fifo_lots_to_components(self):
        """
        For each raw material move line that has no lot assigned yet,
        auto-assign lots in FIFO order:
        - Products with requires_expiry_on_purchase → earliest expiry_date first
        - Other tracked products → oldest lot (by id) first
        """
        self.ensure_one()
        for move in self.move_raw_ids:
            product = move.product_id
            if product.tracking not in ('lot', 'serial'):
                continue

            # Get move lines without a lot assigned
            unassigned = move.move_line_ids.filtered(lambda ml: not ml.lot_id)
            if not unassigned:
                continue

            needed_qty = sum(unassigned.mapped('quantity')) or move.product_uom_qty

            # Find quants for this product at the source location
            quants = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id', 'child_of', move.location_id.id),
                ('quantity', '>', 0),
                ('lot_id', '!=', False),
            ])

            if product.requires_expiry_on_purchase:
                # Sort by our custom expiry_date ASC (FIFO by expiry)
                quants_sorted = quants.sorted(
                    key=lambda q: q.lot_id.expiry_date or '9999-12-31'
                )
            else:
                # Sort by lot id ASC (oldest lot first)
                quants_sorted = quants.sorted(key=lambda q: q.lot_id.id)

            if not quants_sorted:
                continue

            # Delete unassigned lines, rebuild with FIFO lots
            unassigned.unlink()
            remaining = needed_qty

            for quant in quants_sorted:
                if remaining <= 0:
                    break
                take = min(quant.quantity, remaining)
                self.env['stock.move.line'].create({
                    'move_id': move.id,
                    'production_id': self.id,
                    'product_id': product.id,
                    'product_uom_id': move.product_uom.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'lot_id': quant.lot_id.id,
                    'quantity': take,
                })
                remaining -= take
                _logger.info(
                    'FIFO MO: assigned lot %s (expiry: %s) qty %s for %s on MO %s',
                    quant.lot_id.name,
                    quant.lot_id.expiry_date,
                    take,
                    product.display_name,
                    self.name,
                )
