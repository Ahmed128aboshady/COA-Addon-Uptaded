from odoo import fields, models, tools


class PaymentMethodReport(models.Model):
    _name = 'payment.method.report'
    _description = 'Payment Method Report'
    _auto = False
    _rec_name = 'partner_id'
    _order = 'invoice_date desc'

    payment_method_id = fields.Many2one(
        'sale.payment.method',
        string='Payment Method',
        readonly=True,
    )
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    invoice_date = fields.Date(string='Invoice Date', readonly=True)
    move_type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
    ], string='Type', readonly=True)
    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
    ], string='Payment Status', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        currency_field='currency_id',
        readonly=True,
    )
    amount_tax = fields.Monetary(
        string='Taxes',
        currency_field='currency_id',
        readonly=True,
    )
    amount_total = fields.Monetary(
        string='Total',
        currency_field='currency_id',
        readonly=True,
    )
    amount_due = fields.Monetary(
        string='Amount Due',
        currency_field='currency_id',
        readonly=True,
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW payment_method_report AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY aml.id, spm.id)  AS id,
                    spm.id                                        AS payment_method_id,
                    am.partner_id                                 AS partner_id,
                    am.invoice_user_id                            AS user_id,
                    am.company_id                                 AS company_id,
                    am.currency_id                                AS currency_id,
                    am.invoice_date                               AS invoice_date,
                    am.move_type                                  AS move_type,
                    am.payment_state                              AS payment_state,
                    aml.product_id                                AS product_id,
                    pt.categ_id                                   AS categ_id,
                    aml.price_subtotal                            AS amount_untaxed,
                    aml.price_total - aml.price_subtotal          AS amount_tax,
                    aml.price_total                               AS amount_total,
                    CASE
                        WHEN am.amount_total != 0
                        THEN ROUND(
                            am.amount_residual * aml.price_total / am.amount_total,
                            2
                        )
                        ELSE 0
                    END                                           AS amount_due
                FROM account_move_line aml
                JOIN account_move am
                    ON am.id = aml.move_id
                JOIN account_move_payment_method_rel rel
                    ON rel.move_id = am.id
                JOIN sale_payment_method spm
                    ON spm.id = rel.payment_method_id
                JOIN product_product pp
                    ON pp.id = aml.product_id
                JOIN product_template pt
                    ON pt.id = pp.product_tmpl_id
                WHERE am.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')
                  AND am.state = 'posted'
                  AND aml.display_type = 'product'
                  AND aml.product_id IS NOT NULL
            )
        """)
