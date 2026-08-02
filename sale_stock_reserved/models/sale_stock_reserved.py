from odoo import api, fields, models, tools


class SaleStockReserved(models.Model):
    _name = 'sale.stock.reserved'
    _description = 'Sale Stock Reservation Report'
    _auto = False
    _rec_name = 'product_id'
    _order = 'partner_id, product_id'

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    sale_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    picking_id = fields.Many2one('stock.picking', string='Delivery Order', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_uom_qty = fields.Float(string='Ordered Qty', readonly=True, digits='Product Unit of Measure')
    reserved_qty = fields.Float(string='Reserved Qty', readonly=True, digits='Product Unit of Measure')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', readonly=True)
    state = fields.Selection([
        ('confirmed', 'Waiting'),
        ('waiting', 'Waiting Another Move'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Ready'),
    ], string='Availability', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW sale_stock_reserved AS (
                SELECT
                    sm.id                   AS id,
                    so.partner_id           AS partner_id,
                    sm.product_id           AS product_id,
                    sm.product_uom_qty      AS product_uom_qty,
                    sm.quantity             AS reserved_qty,
                    sp.sale_id              AS sale_id,
                    sp.id                   AS picking_id,
                    sm.state                AS state,
                    sm.product_uom          AS product_uom
                FROM stock_move sm
                JOIN stock_picking sp ON sp.id = sm.picking_id
                JOIN sale_order so     ON so.id = sp.sale_id
                WHERE sm.state IN ('confirmed', 'waiting', 'partially_available', 'assigned')
                  AND sp.state NOT IN ('done', 'cancel')
                  AND sm.quantity > 0
            )
        """)

    def action_unreserve(self):
        """Unreserve the selected stock moves and reload the view."""
        moves = self.env['stock.move'].browse(self.ids)
        moves._do_unreserve()
        # Reload the current view after unreserving
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
