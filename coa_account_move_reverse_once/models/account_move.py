# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _check_reverse_once(self):
        """Raise if any move in self must not be reversed (again).

        Rules enforced:
          1. A journal entry that already has at least one active
             (non-cancelled) reversal cannot be reversed again.
          2. A move that is itself a reversal (reversed_entry_id set)
             cannot be reversed. To undo a wrong reversal, reset it to
             draft and cancel it instead of stacking reversals.

        Bypass for controlled server-side operations:
        context key ``skip_reverse_once_check=True``.
        """
        if self.env.context.get("skip_reverse_once_check"):
            return

        for move in self:
            # Rule 2: never reverse a reversal
            if move.reversed_entry_id:
                raise UserError(_(
                    "You cannot reverse the entry '%(move)s' because it is "
                    "itself a reversal of '%(origin)s'.\n\n"
                    "If this reversal is wrong, reset it to draft and cancel "
                    "it instead of reversing it again.",
                    move=move.display_name,
                    origin=move.reversed_entry_id.display_name,
                ))

            # Rule 1: only one active reversal per entry
            active_reversals = move.reversal_move_ids.filtered(
                lambda m: m.state != "cancel"
            )
            if active_reversals:
                raise UserError(_(
                    "The entry '%(move)s' has already been reversed by "
                    "'%(reversal)s'.\n\n"
                    "A journal entry can only be reversed once. If the "
                    "existing reversal is wrong, reset it to draft and "
                    "cancel it first.",
                    move=move.display_name,
                    reversal=", ".join(active_reversals.mapped("display_name")),
                ))

    def _reverse_moves(self, default_values_list=None, cancel=False):
        """Single choke point: every reversal path in Odoo goes through
        here — the Reverse Entry wizard, credit note creation from the
        wizard, and automatic reversals (e.g. accruals with auto-reverse
        dates)."""
        self._check_reverse_once()
        return super()._reverse_moves(
            default_values_list=default_values_list, cancel=cancel
        )
