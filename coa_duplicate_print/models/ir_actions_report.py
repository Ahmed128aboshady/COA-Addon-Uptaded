# -*- coding: utf-8 -*-
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """Increment the print counter of the printed records.

        Done here (and not in _render_qweb_html) so the counter only moves on
        a real PDF print. The increment happens BEFORE the rendering so the
        QWeb template sees the up-to-date value: the 2nd print reads
        coa_print_count == 2 and shows the watermark.
        """
        if res_ids and not self.env.context.get('coa_skip_print_count'):
            report_sudo = self._get_report(report_ref)
            model_name = report_sudo.model
            Model = self.env.get(model_name)
            if (
                Model is not None
                and isinstance(Model, models.BaseModel)
                and 'coa_print_count' in Model._fields
            ):
                raw_ids = res_ids if isinstance(res_ids, (list, tuple)) else [res_ids]
                # Deduplicate while preserving order (duplicate IDs in the URL
                # would otherwise inflate the counter).
                ids = list(dict.fromkeys(raw_ids))
                records = Model.browse(ids).exists()
                # Only count records whose scope is enabled in settings.
                to_count = records.filtered(
                    lambda r: r._coa_duplicate_enabled())
                if to_count:
                    # _coa_register_print uses a separate cursor that commits
                    # immediately, so wkhtmltopdf sub-requests (new
                    # transactions) will see the updated count when they
                    # render the template.
                    to_count._coa_register_print()
                    # Clear the ORM in-process cache so any in-transaction
                    # reads also reflect the newly committed values.
                    to_count.invalidate_recordset([
                        'coa_print_count',
                        'coa_last_print_date',
                        'coa_last_print_uid',
                    ])
        return super()._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
