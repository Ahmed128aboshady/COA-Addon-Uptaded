# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    retention_percent = fields.Float(
        string="Retention (%)",
        default=lambda self: self.env.company.retention_default_percent,
        tracking=True,
        help="Percentage of the invoice held as retention. "
             "Set 0 to disable retention for this order.",
    )
    retention_period_days = fields.Integer(
        string="Retention Period (Days)",
        default=lambda self: self.env.company.retention_default_period_days,
        tracking=True,
        help="Days after delivery until the retained amount becomes due.",
    )
    retention_base = fields.Selection(
        [
            ("total", "Total (VAT Included)"),
            ("untaxed", "Untaxed Amount (Before VAT)"),
        ],
        string="Retention Base",
        default=lambda self: self.env.company.retention_default_base,
        required=True,
        tracking=True,
        help="Amount the retention percentage is applied to for this "
             "order/contract.",
    )
    retention_amount = fields.Monetary(
        string="Retention Amount",
        compute="_compute_retention_amount",
        help="Indicative retention on the current order "
             "(final amount is computed per invoice).",
    )

    @api.depends("amount_total", "amount_untaxed",
                 "retention_percent", "retention_base")
    def _compute_retention_amount(self):
        for order in self:
            base = (
                order.amount_untaxed
                if order.retention_base == "untaxed"
                else order.amount_total
            )
            order.retention_amount = order.currency_id.round(
                base * order.retention_percent / 100.0
            )

    @api.constrains("retention_percent")
    def _check_retention_percent(self):
        for order in self:
            if order.retention_percent < 0 or order.retention_percent > 100:
                raise ValidationError(
                    self.env._("Retention percentage must be between 0 and 100.")
                )

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals["retention_percent"] = self.retention_percent
        vals["retention_period_days"] = self.retention_period_days
        vals["retention_base"] = self.retention_base
        return vals
