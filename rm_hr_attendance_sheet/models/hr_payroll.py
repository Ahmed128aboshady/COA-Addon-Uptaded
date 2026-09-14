# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#    Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    attendance_sheet_ids = fields.One2many(comodel_name='attendance.sheet', inverse_name='payslip_id',
                                           string='Attendance Sheets', ondelete='cascade')

    # الحقول الغير متسجلة (store=False)
    overtime_no = fields.Integer(string="Overtime No", compute='_compute_att_sheet_data_non_stored')
    overtime_hours = fields.Float(string="Overtime Hours", compute='_compute_att_sheet_data_non_stored')
    late_no = fields.Integer(string="Late No", compute='_compute_att_sheet_data_non_stored')
    late_hours = fields.Float(string="Late Hours", compute='_compute_att_sheet_data_non_stored')
    absent_no = fields.Integer(string="Absent No", compute='_compute_att_sheet_data_non_stored')
    absent_hours = fields.Float(string="Absent Hours", compute='_compute_att_sheet_data_non_stored')
    diff_no = fields.Integer(string="Diff No", compute='_compute_att_sheet_data_non_stored')
    diff_hours = fields.Float(string="Diff Hours", compute='_compute_att_sheet_data_non_stored')
    worked_days = fields.Integer(string="Work Days No", compute='_compute_att_sheet_data_non_stored')
    worked_hours = fields.Float(string="Work Days Hours", compute='_compute_att_sheet_data_non_stored')
    no_unpaid_leave = fields.Float(compute="_compute_att_sheet_data_non_stored",
                                   string="No Unpaid Leave Times")
    tot_unpaid_leave = fields.Float(compute="_compute_att_sheet_data_non_stored",
                                    string="Total Unpaid Leave")

    # الحقول المتسجلة (store=True)
    unattended_days = fields.Integer(string="Number of Unttended Days",
                                     readonly=True, store=True)
    attendance_count = fields.Integer(string="Number of Attended Days",
                                      readonly=True, store=True)
    no_diff_days = fields.Integer(string="No of Diff Days",  readonly=True,
                                  store=True)

    @api.depends('attendance_sheet_ids')
    def _compute_att_sheet_data_non_stored(self):
        for slip in self:
            overtime_no = overtime_hours = late_no = late_hours = absent_no = absent_hours = diff_no = diff_hours = worked_days = worked_hours = 0
            no_unpaid_leave = 0
            tot_unpaid_leave = 0
            for sheet in slip.attendance_sheet_ids:
                overtime_no += sheet.no_overtime
                overtime_hours += sheet.tot_overtime
                late_no += sheet.no_late
                late_hours += sheet.tot_late
                absent_no += sheet.no_absence
                absent_hours += sheet.tot_absence
                diff_no += sheet.no_difftime
                diff_hours += sheet.tot_difftime
                worked_hours += sheet.tot_worked_hour
                no_unpaid_leave += sheet.unpaid_leave
                tot_unpaid_leave += sheet.total_unpaid_leave

            slip.overtime_no = overtime_no
            slip.overtime_hours = overtime_hours
            slip.late_no = late_no
            slip.late_hours = late_hours
            slip.absent_no = absent_no
            slip.absent_hours = absent_hours
            slip.diff_no = diff_no
            slip.diff_hours = diff_hours
            slip.worked_days = worked_days
            slip.worked_hours = worked_hours
            slip.no_unpaid_leave = no_unpaid_leave
            slip.tot_unpaid_leave = tot_unpaid_leave

    @api.depends('attendance_sheet_ids', 'attendance_sheet_ids.unattended_days', 'attendance_sheet_ids.attendance_count', 'attendance_sheet_ids.no_diff_days')
    def _compute_att_sheet_data_stored(self):
        for slip in self:
            attendance_count = unattendance_count = no_diff_days = 0
            for sheet in slip.attendance_sheet_ids:
                unattendance_count += sheet.unattended_days
                attendance_count += sheet.attendance_count
                no_diff_days += sheet.no_diff_days

            slip.unattended_days = unattendance_count
            slip.attendance_count = attendance_count
            slip.no_diff_days = no_diff_days

    def set_payslip_attendance_sheet(self):
        self.ensure_one()
        sheet_ids = self.env['attendance.sheet'].search(
            [('employee_id', '=', self.employee_id.id), ('date_from', '>=', self.date_from),
             ('date_to', '<=', self.date_to), ('state', '=', 'done')])
        if sheet_ids:
            self.write({'attendance_sheet_ids': [(6, 0, sheet_ids.ids)]})

    def _get_new_worked_days_lines(self):
        res = super(HrPayslip, self)._get_new_worked_days_lines()

        # # بنعمل فحص آمن لتجنب AttributeError
        # contract = getattr(self, 'contract_id', False)
        #
        # # لو ملقاش العقد في الـ payslip مباشرة، بيحاول يجيبه من الموظف
        # if not contract and getattr(self, 'employee_id', False):
        #     contract = self.employee_id.contract_id
        #
        if self.employee_id:
            self.set_payslip_attendance_sheet()

        return res

    def compute_sheet(self):
        for slip in self:
            if slip.employee_id:
                slip.set_payslip_attendance_sheet()
                # if not slip.attendance_sheet_ids:
                #     raise UserError(_('No Approved Attendance Sheet Found For Employee : %s') % (slip.employee_id.name))
        return super(HrPayslip, self).compute_sheet()