# -*- coding: utf-8 -*-
from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.constrains("quantity", "product_id", "location_id")
    def _check_negative_quantity(self):
        """Block any operation that would drive on-hand quantity below zero.

        Every stock movement in Odoo (manufacturing consumption, deliveries,
        internal transfers, POS, scrap, returns, ...) ultimately writes to
        stock.quant, so this single constraint protects the whole system.

        Exceptions (negative allowed) when ANY of the following is true:
          - the product is not storable (no inventory tracking)
          - the location is not an internal/transit location
              (customer, supplier, production, inventory-loss locations
               are virtual counterparts and MUST be allowed to go negative)
          - "Allow Negative Stock" is checked on the product
          - "Allow Negative Stock" is checked on the product category
          - "Allow Negative Stock" is checked on the location
          - the user belongs to the bypass group
          - context key `skip_negative_stock_check` is set (for controlled
            server-side operations such as inventory adjustments scripts)
        """
        if self.env.context.get("skip_negative_stock_check"):
            return
        if self.env.user.has_group(
            "stock_block_negative.group_negative_stock_bypass"
        ):
            return

        for quant in self:
            if not quant.product_id.is_storable:
                continue
            if quant.location_id.usage not in ("internal", "transit"):
                continue
            # `allow_negative_stock` is restricted to base.group_system, so read
            # it with sudo() — otherwise a regular user's stock move would raise
            # AccessError instead of hitting the intended negative-stock check.
            product_sudo = quant.product_id.sudo()
            if (
                product_sudo.allow_negative_stock
                or product_sudo.categ_id.allow_negative_stock
                or quant.location_id.sudo().allow_negative_stock
            ):
                continue

            rounding = quant.product_uom_id.rounding or 0.00001
            if float_compare(quant.quantity, 0.0, precision_rounding=rounding) < 0:
                if quant.lot_id:
                    message = _(
                        "Operation blocked: it would make the stock of "
                        "product '%(product)s' (lot/serial: %(lot)s) negative "
                        "(%(qty)s %(uom)s) in location '%(location)s'.\n\n"
                        "Please receive/adjust stock first, or ask an "
                        "administrator to allow negative stock for this "
                        "product, category or location.",
                        product=quant.product_id.display_name,
                        lot=quant.lot_id.name,
                        qty=quant.quantity,
                        uom=quant.product_uom_id.name,
                        location=quant.location_id.display_name,
                    )
                else:
                    message = _(
                        "Operation blocked: it would make the stock of "
                        "product '%(product)s' negative (%(qty)s %(uom)s) "
                        "in location '%(location)s'.\n\n"
                        "Please receive/adjust stock first, or ask an "
                        "administrator to allow negative stock for this "
                        "product, category or location.",
                        product=quant.product_id.display_name,
                        qty=quant.quantity,
                        uom=quant.product_uom_id.name,
                        location=quant.location_id.display_name,
                    )
                raise ValidationError(message)
