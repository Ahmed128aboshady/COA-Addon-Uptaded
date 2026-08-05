from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_assignment_allowance = fields.Monetary(string="Assignment Allowance")
    x_mobile_allowance = fields.Monetary(string="Mobile Allowance")
    x_project_allowance = fields.Monetary(string="Project Allowance")
    x_food_allowance = fields.Monetary(string="Food Allowance")
    x_risk_allowance = fields.Monetary(string="Risk Allowance")

    employee_contract = fields.Binary(string="عقد الموظف")
    employee_cv = fields.Binary(string="CV")
    national_address = fields.Binary(string="العنوان الوطني")
    education_certificate = fields.Binary(string="الشهادة الدراسية")

    iqama_date = fields.Date(string="تاريخ الإقامة")