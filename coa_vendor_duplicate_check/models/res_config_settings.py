# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    coa_vdc_mode = fields.Selection(
        selection=[("block", "Block save"), ("warn", "Warn only")],
        string="Duplicate Handling",
        default="block",
        config_parameter="coa_vendor_duplicate_check.mode",
    )
    coa_vdc_scope = fields.Selection(
        selection=[("vendor", "Vendors only"), ("all", "All contacts")],
        string="Apply To",
        default="vendor",
        config_parameter="coa_vendor_duplicate_check.scope",
    )
    coa_vdc_check_email = fields.Boolean(
        string="Detect duplicate Email",
        default=True,
        config_parameter="coa_vendor_duplicate_check.check_email",
    )
    coa_vdc_check_phone = fields.Boolean(
        string="Detect duplicate Phone",
        default=True,
        config_parameter="coa_vendor_duplicate_check.check_phone",
    )
