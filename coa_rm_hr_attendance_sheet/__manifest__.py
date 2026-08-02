# -*- coding: utf-8 -*-
{
    'name': 'COA Rm Hr Attendance Sheet',
    'summary': 'Managing  Attendance Sheets for Employees',
    'description': 'COA Rm Hr Attendance Sheet developed by COA Egypt (https://www.coa-egy.com). Fully integrated for Odoo 17.0.19.0.1.0.0.',
    'author': 'COA (Chart of Accounts)',
    'website': 'https://www.coa-egy.com',
    'category': 'Human Resources',
    'version': '17.0.19.0.1.0.0',
    'license': 'OPL-1',
    'price': 39.0,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'hr_payroll', 'hr_holidays', 'hr_payroll_holidays', 'hr_attendance'],
    'data': ['data/ir_sequence.xml', 'data/data.xml', 'data/ir_cron.xml', 'security/security.xml', 'security/ir.model.access.csv', 'security/rule.xml', 'wizard/change_att_data_view.xml', 'views/hr_attendance_sheet_view.xml', 'views/hr_attendance_policy_view.xml', 'views/hr_public_holiday_view.xml', 'views/attendance_sheet_batch_view.xml', 'views/hr_payslip_view.xml', 'views/hr_leave_type_view.xml', 'views/hr_contract_view.xml', 'views/res_config_settings.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
