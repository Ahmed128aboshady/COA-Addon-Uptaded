# -*- coding: utf-8 -*-
from odoo import api, models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    @api.model_create_multi
    def create(self, vals_list):
        """Fail fast: block already at wizard opening/creation so the user
        gets the error before filling in dates and reasons. The real
        enforcement remains in account.move._reverse_moves (which also
        covers automatic reversals that never open this wizard)."""
        wizards = super().create(vals_list)
        for wizard in wizards:
            wizard.move_ids._check_reverse_once()
        return wizards
