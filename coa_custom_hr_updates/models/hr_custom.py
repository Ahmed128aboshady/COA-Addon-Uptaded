from odoo import models, fields

# 1. موديل الوحدات الجديد
class HrUnit(models.Model):
    _name = 'hr.unit'
    _description = 'HR Unit'

    name = fields.Char(string='Unit Name', required=True)

# 2. تعديل شاشة الأقسام
class HrDepartment(models.Model):
    _inherit = 'hr.department'

    unit_id = fields.Many2one('hr.unit', string='Unit / الوحدة')

# 3. تعديل شاشة المسميات الوظيفية
class HrJob(models.Model):
    _inherit = 'hr.job'

    # حقول للقراءة فقط بناءً على القسم اللي هيتم اختياره
    parent_department_id = fields.Many2one(
        'hr.department', 
        related='department_id.parent_id', 
        string='Parent Department / الإدارة الأم',
        store=True,
        readonly=False
    )
    unit_id = fields.Many2one(
        'hr.unit', 
        related='department_id.unit_id', 
        string='Unit / الوحدة',
        store=True,
        readonly=False
    )

# 4. تعديل شاشة الموظفين
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # حقول مربوطة بالقسم
    parent_department_id = fields.Many2one(
        'hr.department', 
        related='department_id.parent_id', 
        string='Parent Department / الإدارة الأم',
        store=True,
        readonly=False
    )
    unit_id = fields.Many2one(
        'hr.unit', 
        related='department_id.unit_id', 
        string='Unit / الوحدة',
        store=True,
        readonly=False
    )
    
    # الحقول الجديدة المطلوبة في تبويب Work
    emp_code = fields.Char(string='Employee Code / كود الموظف')
    kafala_status = fields.Selection([
        ('inside', 'داخل الكفالة'),
        ('outside', 'خارج الكفالة')
    ], string='Kafala Status / حالة الكفالة')
    sponsor_name = fields.Char(string='Sponsor Name / الكفيل')