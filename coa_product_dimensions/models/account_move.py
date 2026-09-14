from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_project_number = fields.Char(string='Project NO / رقم المشروع')
    custom_project_name = fields.Char(string='Project Name / اسم المشروع')
    custom_site_code = fields.Char(string='SITE CODE / رمز المستودع')