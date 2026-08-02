# -*- coding: utf-8 -*-
{
    'name': 'COA Production Variance Report',
    'summary': 'Planned vs Produced quantity variance report for Manufacturing Orders',
    'description': '\nProduction Quantity Variance Report\n===================================\nCompares the planned quantity (To Produce) against the actually produced\nquantity for each Manufacturing Order, with variance in quantity and\npercentage.\n\nFeatures:\n---------\n* SQL view based report model (fast, no stored duplication)\n* List, Pivot and Graph views\n* Full grouping flexibility: Product, Product Category, Responsible,\n  State, Finished Date (month), Company\n* Ready-made filters: Done MOs, Over-produced, Under-produced\n* Drill-down to the Manufacturing Order from the report line\n* Export wizard: PDF (QWeb, A4 Landscape) and Excel (xlsxwriter,\n  color-coded with totals and autofilter)\n\nCompatible with Odoo 18 and Odoo 19 (Community & Enterprise).\n    ',
    'author': 'COA / Ahmed Aboshady',
    'website': 'https://github.com/Ahmed128aboshady/-COA-Addons',
    'category': 'Manufacturing',
    'version': '17.0.19.0.1.2.0',
    'license': 'LGPL-3',
    'price': 45.0,
    'currency': 'EUR',
    'depends': ['mrp', 'sale_stock'],
    'data': ['security/ir.model.access.csv', 'views/production_variance_views.xml', 'wizard/production_variance_wizard_views.xml', 'report/production_variance_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
