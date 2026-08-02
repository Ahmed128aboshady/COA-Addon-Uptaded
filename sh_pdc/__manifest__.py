# -*- coding: utf-8 -*-
{
    'name': 'Post Dated Cheque Management - Community Edition',
    'summary': 'Post Dated Cheque Management, Manage Post Dated Cheque App, View Vendor Invoice PDC , List Of Customer PDC Payment, T...',
    'description': 'In Invoice/Bill, a post-dated cheque is a cheque written by the customer/vendor (payer) for a date in the future. Whether a post-dated cheque may be cashed or deposited before the date written on it depends on the country. Currently, odoo does not provide any kind of feature to manage post-dated cheque. That why we make this module, it will help to manage a post-dated cheque with an accounting journal entries. This module provides a feature to Register PDC Cheque in an account. This module allows to manage postdated cheque for the customer as well vendors, you can easily track/move to a different state of cheque like new, registered, return, deposit, bounce, done. We have taken care of all states with accounting journal entries, You can easily list filter cheque with different states. We have also made simple pdf reports. Post Dated Cheque Management Odoo\n Manage Vendor Post Dated Cheque Module, Manage Client Post Dated Cheque View Client PDC In Invoice, Get Vendor PDC In Bill, See List Of PDC Bill Of Vendor, Track PDC Process Of Customer, Register Post Dated Cheque, Print Vendor PDC Report Odoo.\n Manage Post Dated Cheque App, View Vendor Invoice PDC , List Of Customer PDC Payment, Track Client PDC Process, Register Vendor Post Dated Cheque Module, Print VendorPDC Report, Print Client PDC Report Odoo.',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Accounting',
    'version': '17.0.19.0.8.0.2',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'EUR',
    'depends': ['account'],
    'data': ['data/account_data.xml', 'data/ir_cron_cust.xml', 'data/mail_templates.xml', 'security/ir.model.access.csv', 'security/pdc_security.xml', 'wizard/pdc_payment_wizard_views.xml', 'wizard/pdc_multi_action_views.xml', 'views/account_move_views.xml', 'views/res_config_settings_views.xml', 'report/pdc_wizard_template.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
