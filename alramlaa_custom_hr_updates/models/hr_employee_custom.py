from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class HrEmployeeFamily(models.Model):
    _name = 'hr.employee.family'
    _description = 'Employee Family Details'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    relation = fields.Selection([
        ('wife', 'Wife'),
        ('son', 'Son'),
        ('daughter', 'Daughter')
    ], string='Relation', required=True)
    contact_no = fields.Char(string='Contact No')
    dob = fields.Date(string='DOB')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    identification_id = fields.Char(string='ID Number')
    
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    family_code = fields.Char(string='Code', compute='_compute_family_code', store=True)

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                rec.age = relativedelta(date.today(), rec.dob).years
            else:
                rec.age = 0

    @api.depends('relation', 'employee_id')
    def _compute_family_code(self):
        for rec in self:
            if rec.relation and rec.employee_id:
                prefix = ''
                if rec.relation == 'wife': prefix = 'W'
                elif rec.relation == 'son': prefix = 'S'
                elif rec.relation == 'daughter': prefix = 'D'
                
                emp_code = rec.employee_id.id 
                
                existing_records = self.search([('employee_id', '=', rec.employee_id.id)])
                if rec.id:
                    seq = list(existing_records.ids).index(rec.id) + 1
                else:
                    seq = len(existing_records) + 1
                
                rec.family_code = f"{prefix}{emp_code}{seq}"
            else:
                rec.family_code = False


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    family_line_ids = fields.One2many('hr.employee.family', 'employee_id', string='Family Dependence Details')

    is_insured = fields.Boolean(string='Insured')
    emp_doesnt_pay_insurance = fields.Boolean(string="Employee Doesn't Pay Insurance")
    company_rate = fields.Float(string='Company Rate')
    employee_rate = fields.Float(string='Employee Rate')