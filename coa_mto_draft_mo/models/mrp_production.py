from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _run_manufacture(self, procurements):
        """
        Override _run_manufacture to keep MO in Draft state.
        Odoo by default calls production.action_confirm() after creating the MO.
        We skip that by wrapping the call with a context flag,
        then stripping the confirm call via MrpProduction override.
        """
        return super(StockRule, self.with_context(mto_keep_draft=True))._run_manufacture(procurements)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        """
        If MO was created automatically via MTO stock rule, skip confirmation.
        The MO stays in Draft until user manually clicks Confirm.
        """
        if self.env.context.get('mto_keep_draft'):
            # Do NOT confirm — return True to avoid errors in callers
            return True
        return super().action_confirm()
