# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    retention_account_id = fields.Many2one(
        related="company_id.retention_account_id",
        readonly=False,
    )
    retention_default_percent = fields.Float(
        related="company_id.retention_default_percent",
        readonly=False,
    )
    retention_default_period_days = fields.Integer(
        related="company_id.retention_default_period_days",
        readonly=False,
    )
    retention_default_base = fields.Selection(
        related="company_id.retention_default_base",
        readonly=False,
    )
