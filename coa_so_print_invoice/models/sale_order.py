# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_print_invoice_direct(self):
        """Open the direct-print page for this SO's posted customer invoices.

        The heavy lifting (access check + sudo rendering) happens in the
        controller, so Sales users without Accounting access can still
        print invoices linked to their own Sale Orders.
        """
        self.ensure_one()
        invoices = self.sudo().invoice_ids.filtered(
            lambda m: m.move_type in ('out_invoice', 'out_refund')
            and m.state == 'posted'
        )
        if not invoices:
            raise UserError(_(
                "There is no posted invoice on this Sale Order to print yet."
            ))
        return {
            'type': 'ir.actions.act_url',
            'url': '/coa_so_print_invoice/print/%s' % self.id,
            'target': 'new',
        }
