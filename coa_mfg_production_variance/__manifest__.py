# -*- coding: utf-8 -*-
{
    'name': 'COA Production Variance Report',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Reporting',
    'summary': 'Planned vs Produced quantity variance report for Manufacturing Orders',
    'description': """
Production Quantity Variance Report
===================================
Compares the planned quantity (To Produce) against the actually produced
quantity for each Manufacturing Order, with variance in quantity and
percentage.

Features:
---------
* SQL view based report model (fast, no stored duplication)
* List, Pivot and Graph views
* Full grouping flexibility: Product, Product Category, Responsible,
  State, Finished Date (month), Company
* Ready-made filters: Done MOs, Over-produced, Under-produced
* Drill-down to the Manufacturing Order from the report line
* Export wizard: PDF (QWeb, A4 Landscape) and Excel (xlsxwriter,
  color-coded with totals and autofilter)

Compatible with Odoo 18 and Odoo 19 (Community & Enterprise).
    """,
    'author': 'COA (Community of Accountants)',
    'website': 'https://www.coa-egy.com',
    'license': 'LGPL-3',
    'depends': ['mrp', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/production_variance_views.xml',
        'wizard/production_variance_wizard_views.xml',
        'report/production_variance_report.xml',
    ],
    'installable': True,
    'application': False,
}
