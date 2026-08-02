""" Initialize Sale Order """

from odoo import models


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         - 
    """
    _inherit = 'sale.order'

    def _prepare_confirmation_values(self):
        """ Prepare the sales order confirmation values.

        Note: self can contain multiple records.

        :return: Sales Order confirmation values
        :rtype: dict
        """
        return {
            'state': 'sale',
        }
