from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    secondary_uom_id = fields.Many2one(
        related='product_tmpl_id.secondary_uom_id', store=True)
    has_secondary_uom = fields.Boolean(
        related='product_tmpl_id.has_secondary_uom', store=True)

    secondary_qty_available = fields.Float(
        'Secondary On Hand', compute='_compute_secondary_quantities',
        digits='Product Unit', compute_sudo=False)
    secondary_virtual_available = fields.Float(
        'Secondary Forecasted', compute='_compute_secondary_quantities',
        digits='Product Unit', compute_sudo=False)
    secondary_incoming_qty = fields.Float(
        'Secondary Incoming', compute='_compute_secondary_quantities',
        digits='Product Unit', compute_sudo=False)
    secondary_outgoing_qty = fields.Float(
        'Secondary Outgoing', compute='_compute_secondary_quantities',
        digits='Product Unit', compute_sudo=False)

    @api.depends('stock_quant_ids.secondary_quantity', 'stock_move_ids.state',
                 'stock_move_ids.secondary_product_uom_qty',
                 'stock_move_ids.secondary_quantity')
    @api.depends_context('location', 'warehouse_id', 'allowed_company_ids')
    def _compute_secondary_quantities(self):
        for product in self:
            if not product.has_secondary_uom:
                product.secondary_qty_available = 0.0
                product.secondary_virtual_available = 0.0
                product.secondary_incoming_qty = 0.0
                product.secondary_outgoing_qty = 0.0
                continue

            # On hand from quants
            domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product._get_domain_locations()
            quants = self.env['stock.quant'].sudo().search([
                ('product_id', '=', product.id),
            ] + domain_quant_loc)
            product.secondary_qty_available = sum(quants.mapped('secondary_quantity'))

            # Incoming: confirmed/assigned/waiting moves going into these locations
            incoming_moves = self.env['stock.move'].sudo().search([
                ('product_id', '=', product.id),
                ('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available')),
            ] + domain_move_in_loc)
            product.secondary_incoming_qty = sum(incoming_moves.mapped('secondary_product_uom_qty'))

            # Outgoing: confirmed/assigned/waiting moves going out of these locations
            outgoing_moves = self.env['stock.move'].sudo().search([
                ('product_id', '=', product.id),
                ('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available')),
            ] + domain_move_out_loc)
            product.secondary_outgoing_qty = sum(outgoing_moves.mapped('secondary_product_uom_qty'))

            product.secondary_virtual_available = (
                product.secondary_qty_available
                + product.secondary_incoming_qty
                - product.secondary_outgoing_qty
            )
