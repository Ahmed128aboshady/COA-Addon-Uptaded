from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    """
    Extend stock.move.line (the detail line inside a receipt/picking):
    - expiry_date_input  → storekeeper fills this on receipt Detailed Operations
    - Auto lot name generation for tracked products without expiry requirement
    - Blocks validation if product requires expiry but none entered
    """
    _inherit = 'stock.move.line'

    def _action_done(self):
        """
        Auto-generate lot/serial names for incoming receipt lines that are
        tracked but have no lot assigned yet.

        Rules:
        - Products with ``requires_expiry_on_purchase = True`` MUST have a
          lot_name already set (via expiry_date_input flow). If not → block.
        - All other tracked products without a lot receive an auto-generated
          serial/lot number from the ``stock.lot.serial`` sequence.

        This override runs *before* super()._action_done() because that
        method raises an error when it finds tracked lines without a lot_name.
        """
        for ml in self:
            # Safety net: if a tracked incoming line still has no lot by the
            # time _action_done runs, generate one now (last chance before Odoo
            # raises its own "Lot/Serial Number required" error).
            picking_type_code = (
                ml.picking_id.picking_type_code
                if ml.picking_id
                else (ml.move_id.picking_id.picking_type_code if ml.move_id and ml.move_id.picking_id else False)
            )
            if (ml.product_id.tracking in ('lot', 'serial')
                    and picking_type_code == 'incoming'
                    and not ml.lot_id
                    and not ml.lot_name
                    and ml.quantity > 0):

                if ml.product_id.requires_expiry_on_purchase and not ml.expiry_date_input:
                    raise UserError(
                        _('Cannot validate receipt.\n\n'
                          'Product "%s" requires a manual Expiry Date.\n'
                          'Please fill in the Expiry Date in the Detailed Operations tab.')
                        % ml.product_id.display_name
                    )

                ml.lot_name = (
                    self.env['ir.sequence'].next_by_code('stock.lot.serial')
                    or 'LOT/%s' % fields.Datetime.now().strftime('%Y%m%d%H%M%S')
                )
                _logger.info(
                    'Auto lot (action_done safety net): %s for %s',
                    ml.lot_name, ml.product_id.display_name,
                )
        return super()._action_done()

    # ── Expiry date entered directly on the receipt line ──────────────────────
    expiry_date_input = fields.Date(
        string='Expiry Date',
        help='Enter the expiry date printed on this lot/batch. '
             'Saved automatically to the lot record on validation.',
    )

    # ── Read-only expiry from the assigned lot (for deliveries / picks) ────────
    lot_expiry_date = fields.Date(
        related='lot_id.expiry_date',
        string='Lot Expiry Date',
        store=False,
        readonly=True,
    )

    expiry_status = fields.Selection(
        [('ok', 'Valid'), ('near', 'Expiring Soon'), ('expired', 'Expired')],
        string='Expiry Status',
        compute='_compute_expiry_status',
        store=True,
    )
    days_to_expiry = fields.Integer(
        string='Days Left',
        compute='_compute_expiry_status',
        store=True,
    )

    @api.depends('expiry_date_input')
    def _compute_expiry_status(self):
        today = date.today()
        for line in self:
            if not line.expiry_date_input:
                line.expiry_status = 'ok'
                line.days_to_expiry = 0
                continue
            delta = (line.expiry_date_input - today).days
            line.days_to_expiry = delta
            if delta < 0:
                line.expiry_status = 'expired'
            elif delta <= 30:
                line.expiry_status = 'near'
            else:
                line.expiry_status = 'ok'

    @api.onchange('expiry_date_input', 'lot_name', 'lot_id')
    def _onchange_expiry_date(self):
        """
        When user types an expiry date and a lot name on the receipt line:
        - If lot already exists → update its expiry_date
        - If lot doesn't exist yet → will be created on validate
        """
        if self.lot_id and self.expiry_date_input:
            self.lot_id.expiry_date = self.expiry_date_input

    def _create_and_assign_lot(self):
        """
        Called during validation when expiry_date_input is filled.
        Creates the stock.lot with our custom expiry_date.
        If lot_name is not set yet, auto-generates one from the sequence.
        """
        for line in self:
            if not line.expiry_date_input:
                continue
            if not line.lot_id and not line.lot_name:
                # Auto-generate lot name — user filled expiry but left lot blank
                line.lot_name = (
                    self.env['ir.sequence'].next_by_code('stock.lot.serial')
                    or 'LOT/%s' % fields.Datetime.now().strftime('%Y%m%d%H%M%S')
                )
                _logger.info(
                    'Auto lot (create_and_assign): %s for %s',
                    line.lot_name, line.product_id.display_name,
                )
            product = line.product_id
            company = line.company_id or self.env.company

            if line.lot_id:
                # Lot already exists → update expiry date
                line.lot_id.expiry_date = line.expiry_date_input
            elif line.lot_name:
                # Find existing lot or create a new one
                lot = self.env['stock.lot'].search([
                    ('name', '=', line.lot_name),
                    ('product_id', '=', product.id),
                    ('company_id', '=', company.id),
                ], limit=1)
                if not lot:
                    lot = self.env['stock.lot'].create({
                        'name': line.lot_name,
                        'product_id': product.id,
                        'company_id': company.id,
                        'expiry_date': line.expiry_date_input,
                    })
                else:
                    lot.expiry_date = line.expiry_date_input
                line.lot_id = lot.id
