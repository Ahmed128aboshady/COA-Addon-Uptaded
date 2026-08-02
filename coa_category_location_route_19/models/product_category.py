from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    # ── Sales ────────────────────────────────────────────────────────
    sales_location_id = fields.Many2one(
        'stock.location',
        string='Sales Source Location',
        domain=[('usage', '=', 'internal')],
        help='Products pulled from this location on Sales Orders. '
             'Returns go back here automatically.',
    )
    sales_route_id = fields.Many2one(
        'stock.route', string='Sales Route (auto)',
        readonly=True, copy=False,
    )

    # ── Manufacturing – 3 steps ──────────────────────────────────────
    # Step1 (Pull) : Source Location      →  Pre-Production
    # Step2 (Push) : Pre-Production      →  Production
    # Step3 (Push) : Production           →  Finished Goods Store

    mfg_location_id = fields.Many2one(
        'stock.location',
        string='Components Source Location',
        domain=[('usage', '=', 'internal')],
        help='Step1 – Components are picked from here to Pre-Production.',
    )
    mfg_pre_production_id = fields.Many2one(
        'stock.location',
        string='Pre-Production Location',
        domain=[('usage', '=', 'internal')],
        help='Step2 – Components are pushed from here to Production.',
    )
    mfg_store_location_id = fields.Many2one(
        'stock.location',
        string='Finished Goods Store Location',
        domain=[('usage', '=', 'internal')],
        help='Step3 – Finished products are pushed here after manufacturing.',
    )
    mfg_route_id = fields.Many2one(
        'stock.route', string='Manufacturing Route (auto)',
        readonly=True, copy=False,
    )

    # ─────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────────────────

    def _get_warehouse(self):
        return self.env['stock.warehouse'].search([], limit=1)

    def _get_or_create_route(self, route, name, warehouse):
        """Return existing route or create a fresh one; wipe old rules."""
        if not route:
            route = self.env['stock.route'].create({
                'name': name,
                'product_categ_selectable': True,
                'supplied_wh_id': warehouse.id if warehouse else False,
            })
        else:
            route.name = name
        # Wipe all existing rules so we rebuild clean
        self.env['stock.rule'].search([('route_id', '=', route.id)]).unlink()
        return route

    def _picking_type(self, warehouse, code):
        return self.env['stock.picking.type'].search([
            ('warehouse_id', '=', warehouse.id),
            ('code', '=', code),
        ], limit=1)

    def _internal_type(self, warehouse):
        return self._picking_type(warehouse, 'internal')

    # ─────────────────────────────────────────────────────────────────────
    # Sales route
    # ─────────────────────────────────────────────────────────────────────

    def _sync_sales_route(self):
        if not self.sales_location_id:
            if self.sales_route_id:
                self.route_ids = [(3, self.sales_route_id.id)]
                self.sales_route_id.unlink()
                self.sales_route_id = False
            return

        warehouse = self._get_warehouse()
        if not warehouse:
            return

        out_type = self._picking_type(warehouse, 'outgoing')
        if not out_type:
            _logger.warning('No outgoing picking type for warehouse %s', warehouse.name)
            return

        customer_loc = (
            out_type.default_location_dest_id
            or self.env.ref('stock.stock_location_customers', raise_if_not_found=False)
        )

        name = _('Sales: %s → Customer') % self.sales_location_id.complete_name
        route = self._get_or_create_route(self.sales_route_id, name, warehouse)

        # Rule 1: Pull from Sales Location → Customer (Outgoing)
        self.env['stock.rule'].create({
            'name': name,
            'route_id': route.id,
            'action': 'pull',
            'picking_type_id': out_type.id,
            'location_src_id': self.sales_location_id.id,
            'location_dest_id': customer_loc.id,
            'procure_method': 'make_to_stock',
            'warehouse_id': warehouse.id,
            'sequence': 10,
        })

        # Rule 2: Pull from Customer → Sales Location (Return)
        return_type = self.env['stock.picking.type'].search([
            ('warehouse_id', '=', warehouse.id),
            ('code', '=', 'incoming'),
        ], limit=1)        
        if return_type:
            # Set the return picking type to deliver to Sales Location by default
            return_type.default_location_dest_id = self.sales_location_id.id
            self.env['stock.rule'].create({
                'name': _('Return: Customer → %s') % self.sales_location_id.complete_name,
                'route_id': route.id,
                'action': 'pull',
                'picking_type_id': return_type.id,
                'location_src_id': customer_loc.id,
                'location_dest_id': self.sales_location_id.id,
                'procure_method': 'make_to_stock',
                'warehouse_id': warehouse.id,
                'sequence': 20,
            })

        self.sales_route_id = route
        if route not in self.route_ids:
            self.route_ids = [(4, route.id)]

    # ─────────────────────────────────────────────────────────────────────
    # Manufacturing route (3 steps: Pick → Pre-Production → Production → Store)
    # ─────────────────────────────────────────────────────────────────────

    def _sync_mfg_route(self):
        # Need at least one location to proceed
        if not self.mfg_location_id and not self.mfg_pre_production_id and not self.mfg_store_location_id:
            if self.mfg_route_id:
                self.route_ids = [(3, self.mfg_route_id.id)]
                self.mfg_route_id.unlink()
                self.mfg_route_id = False
            return

        warehouse = self._get_warehouse()
        if not warehouse:
            return

        # ── Picking types ────────────────────────────────────────────
        pick_type = (
            self._picking_type(warehouse, 'mrp_operation')
            or self._internal_type(warehouse)
        )
        store_type = self._internal_type(warehouse)

        # ── Locations ────────────────────────────────────────────────
        production_loc = (
            self.env.ref('mrp.location_production', raise_if_not_found=False)
            or (pick_type.default_location_dest_id if pick_type else None)
        )

        # Build route name
        src = self.mfg_location_id.complete_name if self.mfg_location_id else '?'
        pre = self.mfg_pre_production_id.complete_name if self.mfg_pre_production_id else '?'
        dst = self.mfg_store_location_id.complete_name if self.mfg_store_location_id else '?'
        name = _('Mfg 3-step: %s → %s → Production → %s') % (src, pre, dst)

        route = self._get_or_create_route(self.mfg_route_id, name, warehouse)

        # ── Rule 1 – PULL: Source Location → Pre-Production (Step1) ────
        if self.mfg_location_id and self.mfg_pre_production_id and pick_type:
            self.env['stock.rule'].create({
                'name': _('Pick: %s → %s') % (self.mfg_location_id.complete_name, self.mfg_pre_production_id.complete_name),
                'route_id': route.id,
                'action': 'pull',
                'picking_type_id': pick_type.id,
                'location_src_id': self.mfg_location_id.id,
                'location_dest_id': self.mfg_pre_production_id.id,
                'procure_method': 'make_to_order',
                'warehouse_id': warehouse.id,
                'sequence': 10,
            })

        # ── Rule 2 – PUSH: Pre-Production → Production (Step2) ───────
        if self.mfg_pre_production_id and production_loc and store_type:
            self.env['stock.rule'].create({
                'name': _('Push: %s → Production') % self.mfg_pre_production_id.complete_name,
                'route_id': route.id,
                'action': 'push',
                'picking_type_id': store_type.id,
                'location_src_id': self.mfg_pre_production_id.id,
                'location_dest_id': production_loc.id,
                'auto': 'manual',
                'warehouse_id': warehouse.id,
                'sequence': 20,
            })

        # ── Rule 3 – PUSH: Production → Finished Goods Store (Step3) ─
        if self.mfg_store_location_id and production_loc and store_type:
            self.env['stock.rule'].create({
                'name': _('Store FG: Production → %s') % self.mfg_store_location_id.complete_name,
                'route_id': route.id,
                'action': 'push',
                'picking_type_id': store_type.id,
                'location_src_id': production_loc.id,
                'location_dest_id': self.mfg_store_location_id.id,
                'auto': 'manual',
                'warehouse_id': warehouse.id,
                'sequence': 30,
            })

        self.mfg_route_id = route
        if route not in self.route_ids:
            self.route_ids = [(4, route.id)]

    # ─────────────────────────────────────────────────────────────────────
    # ORM overrides
    # ─────────────────────────────────────────────────────────────────────

    def write(self, vals):
        res = super().write(vals)
        sales_changed = 'sales_location_id' in vals
        mfg_changed = any(f in vals for f in (
            'mfg_location_id', 'mfg_pre_production_id', 'mfg_store_location_id',
        ))
        for rec in self:
            if sales_changed:
                rec._sync_sales_route()
            if mfg_changed:
                rec._sync_mfg_route()
        return res

    def unlink(self):
        for rec in self:
            if rec.sales_route_id:
                rec.sales_route_id.unlink()
            if rec.mfg_route_id:
                rec.mfg_route_id.unlink()
        return super().unlink()
