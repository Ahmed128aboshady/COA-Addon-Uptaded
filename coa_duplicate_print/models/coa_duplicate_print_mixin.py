# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, _

_logger = logging.getLogger(__name__)


class CoaDuplicatePrintMixin(models.AbstractModel):
    """Adds a print counter and duplicate-watermark helpers to a model.

    The counter is incremented by the ir.actions.report override, at real
    print time only (PDF rendering), not when the form is opened.
    """
    _name = 'coa.duplicate.print.mixin'
    _description = 'Duplicate Print Mixin'

    coa_print_count = fields.Integer(
        string='Print Count', default=0, copy=False, readonly=True,
        help='Number of times this document has been printed to PDF.')
    coa_last_print_date = fields.Datetime(
        string='Last Printed On', copy=False, readonly=True)
    coa_last_print_uid = fields.Many2one(
        'res.users', string='Last Printed By', copy=False, readonly=True)

    def _coa_duplicate_scope(self):
        """Which setting scope this model belongs to: 'sale' or 'stock'."""
        return False

    def _coa_duplicate_enabled(self):
        """True if the duplicate watermark applies to this record."""
        self.ensure_one()
        mode = self.env.company.coa_duplicate_print_mode
        if mode == 'none':
            return False
        scope = self._coa_duplicate_scope()
        if not scope:
            return False
        if mode == 'both':
            return True
        return mode == scope

    def _coa_is_duplicate_print(self):
        """True when the current print is a re-print (2nd time or more)."""
        self.ensure_one()
        return bool(
            self._coa_duplicate_enabled() and self.coa_print_count > 1)

    def _coa_duplicate_label(self):
        """Bilingual watermark text, e.g. 'DUPLICATE - مكرر - Copy #2'."""
        self.ensure_one()
        return _('DUPLICATE - مكرر - Copy #%(num)s', num=self.coa_print_count)

    def _coa_register_print(self):
        """Increment the counter on the current request transaction.

        In Odoo 18, the QWeb HTML is rendered entirely server-side inside the
        same database transaction before wkhtmltopdf is invoked.  wkhtmltopdf
        only fetches static assets (CSS, images) via HTTP — it does NOT make
        sub-requests to re-read record data.  Therefore we can safely write on
        env.cr (the main cursor) and the template will see the updated count.

        Writing on the main cursor also avoids the deadlock that would occur if
        a sibling override (e.g. coa_so_date_on_print) writes to the same
        table on env.cr while our separate cursor holds a row lock.

        We use a SQL-level atomic increment (SET col = col + 1) to avoid
        double-counting when the same record ID appears more than once.
        """
        # Deduplicate IDs so we count each distinct document exactly once.
        unique_ids = list(dict.fromkeys(self.ids))  # preserves order, drops duplicates
        if not unique_ids:
            return
        now = fields.Datetime.now()
        uid = self.env.user.id
        table = self.env[self._name]._table
        try:
            self.env.cr.execute(
                f"""
                UPDATE {table}
                   SET coa_print_count    = coa_print_count + 1,
                       coa_last_print_date = %s,
                       coa_last_print_uid  = %s
                 WHERE id = ANY(%s)
                """,
                (now, uid, unique_ids),
            )
        except Exception:
            # Never block printing because of a counter failure.
            _logger.exception(
                "Could not update print count for %s %s",
                self._name, self.ids,
            )
            return
        # Flush stale ORM cache so field reads in the same transaction
        # (including the QWeb template) see the values we just wrote.
        self.invalidate_recordset(
            ['coa_print_count', 'coa_last_print_date', 'coa_last_print_uid'],
            flush=False,
        )

    def action_coa_reset_print_count(self):
        """Reset the counter so the next print is treated as the original."""
        self.sudo().write({
            'coa_print_count': 0,
            'coa_last_print_date': False,
            'coa_last_print_uid': False,
        })
        return True
