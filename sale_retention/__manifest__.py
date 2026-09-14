# -*- coding: utf-8 -*-
{
    "name": "Sales Retention Money",
    "summary": "Customer retention/holdback on sales: configurable percentage "
               "and holding period per order, automatic split of the "
               "receivable to a dedicated retention account with maturity "
               "based on the delivery date. Aging and partner ledger stay "
               "fully correct.",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "author": "COA (Community of Accountants)",
    "license": "LGPL-3",
    "depends": ["sale_stock", "account"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/retention_menu.xml",
        "report/retention_report.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": False,
}
