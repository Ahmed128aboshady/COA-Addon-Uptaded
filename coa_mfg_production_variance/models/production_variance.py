# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class MrpProductionVariance(models.Model):
    _name = 'coa.mfg.production.variance'
    _description = 'Production Quantity Variance (Planned vs Produced)'
    _auto = False
    _rec_name = 'production_id'
    _order = 'date_finished desc, id desc'

    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', string='UoM', readonly=True)
    user_id = fields.Many2one('res.users', string='Responsible', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
    ], string='State', readonly=True)
    date_start = fields.Datetime(string='Start Date', readonly=True)
    date_finished = fields.Datetime(string='End Date', readonly=True)

    sale_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    ordered_qty = fields.Float(string='Ordered Qty (SO)', readonly=True, aggregator='sum',
                               help='Quantity ordered by the customer on the Sale Order '
                                    'for this product.')
    delivered_qty = fields.Float(string='Delivered Qty', readonly=True, aggregator='sum',
                                 help='Quantity actually delivered to the customer '
                                      '(from the Sale Order lines).')

    planned_qty = fields.Float(string='Planned Qty', readonly=True, aggregator='sum')
    produced_qty = fields.Float(string='Produced Qty', readonly=True, aggregator='sum')
    variance_qty = fields.Float(string='Variance Qty', readonly=True, aggregator='sum',
                                help='Produced Qty - Planned Qty. Negative = under-production.')
    variance_percent = fields.Float(string='Variance %', readonly=True, aggregator='avg',
                                    help='(Produced - Planned) / Planned * 100')
    qty_on_hand = fields.Float(
        string='On Hand Qty',
        digits='Product Unit of Measure',
        readonly=True,
        aggregator='sum',
    )

    def _table_exists(self, table_name):
        self.env.cr.execute("""
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = current_schema() AND table_name = %s
        """, (table_name,))
        return bool(self.env.cr.fetchone())

    def _get_sale_link_sql(self):
        """Return (extra JOINs, sale_id expr) linking MO -> Sale Order.

        Odoo 19: procurement.group was removed; MTO traceability now goes
        through stock.reference (M2M rel tables to both mrp.production
        and sale.order).
        Odoo 18: classic mo.procurement_group_id -> procurement_group.sale_id.
        """
        if self._table_exists('stock_reference_production_rel') \
                and self._table_exists('stock_reference_sale_rel'):
            # Odoo 19+
            joins = """
                LEFT JOIN (
                    SELECT srp.production_id AS production_id,
                           MIN(srs.sale_id) AS sale_id
                    FROM stock_reference_production_rel srp
                    JOIN stock_reference_sale_rel srs
                        ON srs.reference_id = srp.reference_id
                    GROUP BY srp.production_id
                ) lnk ON lnk.production_id = mo.id
                LEFT JOIN sale_order so ON so.id = lnk.sale_id
            """
        elif self._table_exists('procurement_group') \
                and self._table_exists('sale_order'):
            # Odoo 18
            joins = """
                LEFT JOIN procurement_group pg ON pg.id = mo.procurement_group_id
                LEFT JOIN sale_order so ON so.id = pg.sale_id
            """
        else:
            # sale not installed: no link possible
            return """
                LEFT JOIN LATERAL (
                    SELECT NULL::integer AS id, NULL::integer AS partner_id
                ) so ON TRUE
            """, False
        return joins, True

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        sale_joins, has_sale = self._get_sale_link_sql()
        if has_sale:
            sol_join = """
                LEFT JOIN (
                    SELECT
                        l.order_id AS order_id,
                        l.product_id AS product_id,
                        SUM(l.product_uom_qty) AS ordered_qty,
                        SUM(l.qty_delivered) AS delivered_qty
                    FROM sale_order_line l
                    WHERE l.product_id IS NOT NULL
                    GROUP BY l.order_id, l.product_id
                ) sol ON sol.order_id = so.id AND sol.product_id = mo.product_id
            """
        else:
            sol_join = """
                LEFT JOIN LATERAL (
                    SELECT NULL::numeric AS ordered_qty,
                           NULL::numeric AS delivered_qty
                ) sol ON TRUE
            """
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    mo.id AS id,
                    mo.id AS production_id,
                    mo.product_id AS product_id,
                    pt.categ_id AS categ_id,
                    mo.product_uom_id AS product_uom_id,
                    mo.user_id AS user_id,
                    mo.company_id AS company_id,
                    mo.state AS state,
                    mo.date_start AS date_start,
                    mo.date_finished AS date_finished,
                    so.id AS sale_id,
                    so.partner_id AS partner_id,
                    COALESCE(sol.ordered_qty, 0.0) AS ordered_qty,
                    COALESCE(sol.delivered_qty, 0.0) AS delivered_qty,
                    mo.product_qty AS planned_qty,
                    COALESCE(fin.produced_qty, 0.0) AS produced_qty,
                    COALESCE(fin.produced_qty, 0.0) - mo.product_qty AS variance_qty,
                    CASE
                        WHEN mo.product_qty <> 0.0 THEN
                            (COALESCE(fin.produced_qty, 0.0) - mo.product_qty)
                            / mo.product_qty 
                        ELSE 0.0
                    END AS variance_percent,
                    COALESCE(onhand.qty_on_hand, 0.0) AS qty_on_hand
                FROM mrp_production mo
                JOIN product_product pp ON pp.id = mo.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                %s
                %s
                LEFT JOIN (
                    SELECT
                        sm.production_id AS production_id,
                        SUM(sm.quantity) AS produced_qty
                    FROM stock_move sm
                    JOIN mrp_production mo2 ON mo2.id = sm.production_id
                    WHERE sm.state = 'done'
                      AND sm.product_id = mo2.product_id
                    GROUP BY sm.production_id
                ) fin ON fin.production_id = mo.id
                LEFT JOIN (
                    SELECT
                        sq.product_id AS product_id,
                        sl.company_id AS company_id,
                        SUM(sq.quantity) AS qty_on_hand
                    FROM stock_quant sq
                    JOIN stock_location sl ON sl.id = sq.location_id
                    WHERE sl.usage = 'internal'
                      AND sl.active = TRUE
                    GROUP BY sq.product_id, sl.company_id
                ) onhand ON onhand.product_id = mo.product_id
                         AND onhand.company_id = mo.company_id
                WHERE mo.state != 'cancel'
            )
        """ % (self._table, sale_joins, sol_join))

    def action_open_sale_order(self):
        self.ensure_one()
        if not self.sale_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.sale_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_production(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'res_id': self.production_id.id,
            'view_mode': 'form',
            'target': 'current',
        }