from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date


class HrEmployeeFamily(models.Model):
    _name = 'hr.employee.family'
    _description = 'Employee Family Details'

    name = fields.Char(string="Name", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", ondelete='cascade')
    relation = fields.Selection([
        ('W', 'Wife'),
        ('S', 'Son'),
        ('D', 'Daughter'),
        ('F', 'Father'),
        ('M', 'Mother')
    ], string="Relation", required=True)
    contact_no = fields.Char(string="Contact No")
    dob = fields.Date(string="DOB")
    id_number = fields.Char(string="ID No")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    code = fields.Char(string="Code", readonly=True, copy=False)

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                rec.age = relativedelta(date.today(), rec.dob).years
            else:
                rec.age = 0

    @api.model_create_multi
    def create(self, vals_list):
        records = super(HrEmployeeFamily, self).create(vals_list)
        for rec in records:
            if rec.relation and rec.employee_id:
                emp_code = rec.employee_id.emp_code or str(rec.employee_id.id)
                family_count = self.search_count([
                    ('employee_id', '=', rec.employee_id.id),
                    ('id', '<=', rec.id)
                ])
                rec.code = f"{rec.relation}{emp_code}-{family_count}"
        return records


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    family_ids = fields.One2many(
        'hr.employee.family', 'employee_id',
        string="Dependence Details"
    )

    is_insured = fields.Boolean(string="Insured")
    employee_doesnt_pay_insurance = fields.Boolean(
        string="Employee Doesn't Pay Insurance"
    )
    company_rate = fields.Float(string="Company Rate")
    employee_rate = fields.Float(string="Employee Rate")

    company_amount = fields.Float(
        string="Company Amount",
        compute="_compute_insurance_amounts",
        store=True,
    )
    employee_amount = fields.Float(
        string="Employee Amount",
        compute="_compute_insurance_amounts",
        store=True,
    )

    @api.depends('company_rate', 'employee_rate', 'wage')
    def _compute_insurance_amounts(self):
        for emp in self:
            version = self.env['hr.version'].search([
                ('employee_id', '=', emp.id)
            ], order='date_version desc', limit=1)
            housing = version.l10n_sa_housing_allowance if version else 0.0
            base = (emp.wage or 0.0) + housing
            emp.company_amount = round((emp.company_rate or 0.0) * base / 100, 2)
            emp.employee_amount = round((emp.employee_rate or 0.0) * base / 100, 2)