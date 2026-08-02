# -*- coding: utf-8 -*-
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coa_date_set_on_print = fields.Boolean(
        string="Date Set On Print",
        copy=False,
        default=False,
        help="Informational flag: True once date_order has been updated by the "
             "print mechanism at least once.",
    )

    def _coa_set_date_on_print(self):
        """Stamp date_order with the current datetime on every print.

        Writes on the MAIN cursor (env.cr) so the QWeb template rendered in the
        same transaction immediately sees the new date_order without needing to
        re-read from the DB.  After the raw SQL write we invalidate the ORM
        cache so field access in the same transaction bypasses the stale cache.

        Using env.cr instead of a separate cursor avoids a DeadLock that would
        occur if coa_duplicate_print's separate-cursor UPDATE were still in
        flight while we tried to lock the same rows.  By the time control
        reaches this method, coa_duplicate_print (higher in the MRO) has
        already committed its separate cursor and released its row locks.
        """
        unique_ids = list(dict.fromkeys(self.ids))
        if not unique_ids:
            return
        now = fields.Datetime.now()
        try:
            self.env.cr.execute(
                """
                UPDATE sale_order
                   SET date_order            = %s,
                       coa_date_set_on_print = true
                 WHERE id = ANY(%s)
                """,
                (now, unique_ids),
            )
        except Exception:
            _logger.exception(
                "Could not stamp print date for sale.order %s", self.ids
            )
            return
        # Clear the ORM cache so the QWeb template reads the value we just
        # wrote rather than the stale value from before this call.
        self.invalidate_recordset(['date_order', 'coa_date_set_on_print'],
                                  flush=False)
