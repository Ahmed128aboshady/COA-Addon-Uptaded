# -*- coding: utf-8 -*-
from odoo import api, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.constrains('check_account_audit_trail')
    def _check_audit_trail_records(self):
        # Override to allow disabling audit trail even when journal entries exist
        pass
