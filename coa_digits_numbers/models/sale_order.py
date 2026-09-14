from odoo import models, fields, api,_
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#
#     @api.model
#     def create(self, vals):
#         if 'amount_total' in vals:
#             vals['amount_total'] = int(vals['amount_total'])
#
#         if 'amount_untaxed' in vals:
#             vals['amount_untaxed'] = int(vals['amount_untaxed'])
#
#         if 'amount_tax' in vals:
#             vals['amount_tax'] = int(vals['amount_tax'])
#
#         return super(SaleOrder, self).create(vals)
#
#     def write(self, vals):
#         if 'amount_total' in vals:
#             vals['amount_total'] = int(vals['amount_total'])
#
#         if 'amount_untaxed' in vals:
#             vals['amount_untaxed'] = int(vals['amount_untaxed'])
#
#         if 'amount_tax' in vals:
#             vals['amount_tax'] = int(vals['amount_tax'])
#
#         return super(SaleOrder, self).write(vals)




# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#     price_subtotal = fields.Monetary(
#         string='Subtotal',
#         currency_field='currency_id',
#         readonly=True,
#         store=True,
#         digits=(16, 0)
#     )

    # @api.model
    # def create(self, vals):
    #     if 'product_uom_qty' in vals:
    #         vals['product_uom_qty'] = int(vals['product_uom_qty'])
    #
    #     if 'price_unit' in vals:
    #         vals['price_unit'] = int(vals['price_unit'])
    #
    #     if 'price_subtotal' in vals:
    #         try:
    #             vals['price_subtotal'] = int(float(vals['price_subtotal']))
    #         except:
    #             pass
    #
    #     return super().create(vals)
    #
    # def write(self, vals):
    #     if 'product_uom_qty' in vals:
    #         vals['product_uom_qty'] = int(vals['product_uom_qty'])
    #
    #     if 'price_unit' in vals:
    #         vals['price_unit'] = int(vals['price_unit'])
    #
    #     if 'price_subtotal' in vals:
    #         try:
    #             vals['price_subtotal'] = int(float(vals['price_subtotal']))
    #         except:
    #             pass
    #
    #     return super().write(vals)


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    rounding = fields.Float(
        string='Rounding Factor',
        digits=(12, 0),
        default=1.0,
        help="The rounding factor to be used when rounding amounts."
    )


    def write(self, vals):
        if 'rounding' in vals:
            for record in self:
                try:
                    return super(ResCurrency, record).write(vals)
                except UserError:
                    self.env.cr.execute("""
                        UPDATE res_currency
                        SET rounding = %s
                        WHERE id = %s
                    """, (vals['rounding'], record.id))

            return True

        return super(ResCurrency, self).write(vals)


