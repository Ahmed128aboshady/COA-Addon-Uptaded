from odoo import fields, models, api, _
from odoo.http import request

class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _load_menus_blacklist(self):
        """Override to add access-management hidden menus to the blacklist (Odoo 19)."""
        blacklist = super()._load_menus_blacklist()
        try:
            cids_cookie = request.httprequest.cookies.get('cids')
            cids = int(cids_cookie.split('-')[0]) if cids_cookie else self.env.company.id
            hidden_menu_ids = self.env.user.access_management_ids.filtered(
                lambda line: line.is_apply_on_without_company or int(cids) in line.company_ids.ids
            ).mapped('hide_menu_ids.menu_id')
            return list(blacklist) + list(hidden_menu_ids)
        except Exception:
            pass
        return list(blacklist)

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        ids = super(ir_ui_menu, self).search(args, offset=0, limit=None, order=order)
        all_menu = ids.ids
        try:
            cids_cookie = request.httprequest.cookies.get('cids')
            cids = cids_cookie.split('-')[0] if cids_cookie else self.env.company.id
            for menu_id in self.env.user.access_management_ids.filtered(
                lambda line: line.is_apply_on_without_company or int(cids) in line.company_ids.ids
            ).mapped('hide_menu_ids.menu_id'):
                if menu_id in all_menu:
                    all_menu.remove(menu_id)
        except Exception:
            pass
        return self.browse(all_menu)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ir_ui_menu, self).create(vals_list)
        menu_item_obj = self.env['menu.item'].sudo()
        for record in res:
            menu_item_obj.create({'name': record.display_name, 'menu_id': record.id})
        return res

    def unlink(self):
        menu_item_obj = self.env['menu.item'].sudo()
        for record in self:
            menu_item_obj.search([('menu_id', '=', record.id)]).unlink()
        return super(ir_ui_menu, self).unlink()
