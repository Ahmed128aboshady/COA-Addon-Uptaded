# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_user_allowed_picking_type_ids(self):
        """Read allowed picking type IDs directly from DB to avoid circular access check."""
        self.env.cr.execute(
            "SELECT picking_type_id FROM res_users_stock_picking_type_rel WHERE user_id = %s",
            (self.env.uid,)
        )
        return [row[0] for row in self.env.cr.fetchall()]

    def _get_user_allowed_location_ids(self):
        """Read allowed location IDs directly from DB to avoid circular access check."""
        self.env.cr.execute(
            "SELECT location_id FROM res_users_stock_location_rel WHERE user_id = %s",
            (self.env.uid,)
        )
        return [row[0] for row in self.env.cr.fetchall()]

    def _is_location_restriction_enabled(self):
        """Safe check — returns False if column doesn't exist yet (during install)."""
        try:
            self.env.cr.execute(
                "SELECT location_restriction_enabled FROM res_users WHERE id = %s",
                (self.env.uid,)
            )
            row = self.env.cr.fetchone()
            return bool(row and row[0])
        except Exception:
            self.env.cr.rollback()
            return False

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, *, active_test=True, bypass_access=False):
        if not self.env.su and active_test and self._is_location_restriction_enabled():
            allowed_pt_ids = self._get_user_allowed_picking_type_ids()
            if allowed_pt_ids:
                domain = [('picking_type_id', 'in', allowed_pt_ids)] + list(domain or [])
            else:
                allowed_loc_ids = self._get_user_allowed_location_ids()
                if allowed_loc_ids:
                    all_allowed = self.env['stock.location'].sudo().search([
                        '|', ('usage', 'in', ['supplier', 'customer', 'inventory', 'production']),
                             ('id', 'child_of', allowed_loc_ids),
                    ])
                    loc_ids = all_allowed.ids
                    domain = ['|',
                        ('location_id', 'in', loc_ids),
                        ('location_dest_id', 'in', loc_ids),
                    ] + list(domain or [])
        return super()._search(domain, offset=offset, limit=limit, order=order, active_test=active_test, bypass_access=bypass_access)

    # ── Validate: block access to forbidden locations / operation types ──────
    def button_validate(self):
        user = self.env.user
        if self._is_location_restriction_enabled():
            for picking in self:
                if (
                    picking.picking_type_id
                    and user.allowed_picking_type_ids
                    and not user._is_picking_type_allowed(picking.picking_type_id)
                ):
                    raise UserError(_(
                        'You are not allowed to validate transfers of type "%s".\n'
                        'Please contact your administrator.',
                        picking.picking_type_id.name,
                    ))

                code = picking.picking_type_id.code if picking.picking_type_id else False

                if code == 'outgoing':
                    if (
                        picking.location_id
                        and user.allowed_location_ids
                        and not user._is_location_allowed(picking.location_id)
                    ):
                        raise UserError(_(
                            'You are not allowed to validate this transfer.\n'
                            'You do not have access to source location "%s".',
                            picking.location_id.complete_name,
                        ))
                elif code == 'incoming':
                    if (
                        picking.location_dest_id
                        and user.allowed_location_ids
                        and not user._is_location_allowed(picking.location_dest_id)
                    ):
                        raise UserError(_(
                            'You are not allowed to validate this transfer.\n'
                            'You do not have access to destination location "%s".',
                            picking.location_dest_id.complete_name,
                        ))
                else:
                    if (
                        picking.location_id
                        and user.allowed_location_ids
                        and not user._is_location_allowed(picking.location_id)
                    ):
                        raise UserError(_(
                            'You are not allowed to validate this transfer.\n'
                            'You do not have access to source location "%s".',
                            picking.location_id.complete_name,
                        ))
                    if (
                        picking.location_dest_id
                        and user.allowed_location_ids
                        and not user._is_location_allowed(picking.location_dest_id)
                    ):
                        raise UserError(_(
                            'You are not allowed to validate this transfer.\n'
                            'You do not have access to destination location "%s".',
                            picking.location_dest_id.complete_name,
                        ))

        return super().button_validate()
