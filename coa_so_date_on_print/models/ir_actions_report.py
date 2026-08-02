# -*- coding: utf-8 -*-
import logging

from odoo import models

_logger = logging.getLogger(__name__)

# Sale Order report XML IDs whose printing should stamp date_order.
SO_REPORT_XMLIDS = (
    'sale.action_report_saleorder',
    'sale.action_report_pro_forma_invoice',
)

# Delivery / picking report XML IDs that should also stamp the linked
# sale order's date_order.
DELIVERY_REPORT_XMLIDS = (
    'stock.action_report_delivery',
    'stock.action_report_picking',
)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _coa_is_so_report(self, report_sudo):
        """True if report_sudo is a tracked Sale Order report."""
        if report_sudo.model != 'sale.order':
            return False
        for xmlid in SO_REPORT_XMLIDS:
            rec = self.env.ref(xmlid, raise_if_not_found=False)
            if rec and rec.id == report_sudo.id:
                return True
        return False

    def _coa_is_delivery_report(self, report_sudo):
        """True if report_sudo is a tracked Delivery / Picking report."""
        if report_sudo.model != 'stock.picking':
            return False
        for xmlid in DELIVERY_REPORT_XMLIDS:
            rec = self.env.ref(xmlid, raise_if_not_found=False)
            if rec and rec.id == report_sudo.id:
                return True
        return False

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """Stamp date_order with the current datetime on every print.

        Covers two paths:
          1. Printing the Sale Order directly → stamps date_order on those orders.
          2. Printing a Delivery Slip → finds the linked sale orders via
             picking.sale_id and stamps their date_order.

        The stamp is written on env.cr (the main request transaction) BEFORE
        calling super() so the QWeb renderer — which runs inside super() in
        the same transaction — immediately sees the new date_order value.

        Ordering guarantee: coa_duplicate_print (loaded after this module, so
        higher in the MRO) runs its _render_qweb_pdf first and commits its
        coa_print_count update via a separate cursor before control reaches
        this override.  By the time we write date_order on env.cr the
        separate cursor has committed and released its row lock, so there is
        no deadlock or serialisation conflict.
        """
        if res_ids and not self.env.context.get('coa_skip_date_on_print'):
            report_sudo = self._get_report(report_ref)
            raw_ids = res_ids if isinstance(res_ids, (list, tuple)) else [res_ids]
            ids = list(dict.fromkeys(raw_ids))

            if self._coa_is_so_report(report_sudo):
                orders = self.env['sale.order'].sudo().browse(ids).exists()
                if orders:
                    orders._coa_set_date_on_print()

            elif self._coa_is_delivery_report(report_sudo):
                pickings = self.env['stock.picking'].sudo().browse(ids).exists()
                orders = pickings.sale_id.filtered('id')
                if orders:
                    orders._coa_set_date_on_print()

        return super()._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
