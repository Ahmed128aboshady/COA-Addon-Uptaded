# -*- coding: utf-8 -*-
{
    'name': 'COA Mfg Bom Consumption Report',
    'summary': 'Compare planned BOM quantities with actual stock consumption per MO',
    'description': 'COA Mfg Bom Consumption Report developed by COA Egypt (https://www.coa-egy.com). Flagship enterprise solution for Odoo 17.0.19.0.1.0.1.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.0.1',
    'license': 'OPL-1',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp', 'stock'],
    'data': ['security/ir.model.access.csv', 'wizard/bom_consumption_wizard_view.xml', 'report/bom_consumption_report_template.xml', 'report/bom_consumption_report_action.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
