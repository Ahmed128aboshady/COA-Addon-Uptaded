from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    secondary_quantity = fields.Float(
        'Secondary Quantity', digits='Product Unit', default=0.0,
        help="Quantity in the secondary unit of measure.")
    secondary_reserved_quantity = fields.Float(
        'Secondary Reserved Quantity', digits='Product Unit', default=0.0,
        readonly=True)
    secondary_available_quantity = fields.Float(
        'Secondary Available Quantity',
        compute='_compute_secondary_available_quantity',
        digits='Product Unit')
    secondary_uom_id = fields.Many2one(
        related='product_id.secondary_uom_id', string='Secondary UoM')
    has_secondary_uom = fields.Boolean(
        related='product_id.has_secondary_uom')

    # Inventory fields for secondary UoM
    secondary_inventory_quantity = fields.Float(
        'Secondary Counted', digits='Product Unit',
        help="Counted quantity in the secondary unit of measure.")
    secondary_inventory_diff_quantity = fields.Float(
        'Secondary Difference', compute='_compute_secondary_inventory_diff_quantity',
        store=True, readonly=True, digits='Product Unit')

    @api.depends('secondary_quantity', 'secondary_reserved_quantity')
    def _compute_secondary_available_quantity(self):
        for quant in self:
            quant.secondary_available_quantity = quant.secondary_quantity - quant.secondary_reserved_quantity

    @api.depends('secondary_inventory_quantity', 'secondary_quantity')
    def _compute_secondary_inventory_diff_quantity(self):
        for quant in self:
            quant.secondary_inventory_diff_quantity = quant.secondary_inventory_quantity - quant.secondary_quantity

    def _get_inventory_fields_write(self):
        fields = super()._get_inventory_fields_write()
        fields += ['secondary_inventory_quantity', 'secondary_inventory_diff_quantity']
        return fields

    @api.model
    def _update_secondary_quantity(self, product_id, location_id, secondary_quantity,
                                   lot_id=None, package_id=None, owner_id=None):
        """Update the secondary quantity on quants, similar to _update_available_quantity
        but for the independent secondary UoM.
        """
        if not secondary_quantity or not product_id.has_secondary_uom:
            return
        self = self.sudo()
        quants = self._gather(product_id, location_id, lot_id=lot_id,
                              package_id=package_id, owner_id=owner_id, strict=True)
        if quants:
            quant = quants[0]
            quant.write({
                'secondary_quantity': quant.secondary_quantity + secondary_quantity,
            })
        else:
            # If no quant found, create one (rare case where secondary moves
            # happen before primary quant exists)
            self.create({
                'product_id': product_id.id,
                'location_id': location_id.id,
                'lot_id': lot_id and lot_id.id,
                'package_id': package_id and package_id.id,
                'owner_id': owner_id and owner_id.id,
                'secondary_quantity': secondary_quantity,
            })

    def _apply_inventory(self, date=None):
        """After standard inventory application, also apply secondary quantity differences."""
        # Capture secondary diffs before super resets things
        secondary_diffs = {}
        for quant in self:
            if quant.has_secondary_uom and quant.secondary_inventory_diff_quantity:
                secondary_diffs[quant.id] = quant.secondary_inventory_diff_quantity

        res = super()._apply_inventory(date=date)

        # Apply secondary diffs directly to quants
        for quant in self:
            diff = secondary_diffs.get(quant.id, 0.0)
            if diff:
                quant.sudo().write({
                    'secondary_quantity': quant.secondary_quantity + diff,
                })
                quant.secondary_inventory_quantity = 0.0

        return res
