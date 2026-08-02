# HR Attendance Sheet And Policies (`rm_hr_attendance_sheet`)

## 📌 الوصف العام (Overview)
Managing  Attendance Sheets for Employees
        

### التفاصيل الوظيفية:

        Employees Attendance Sheet Management   
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `rm_hr_attendance_sheet`
- **التصنيف (Category):** `hr`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`, `hr`, `hr_payroll`, `hr_holidays`, `hr_payroll_holidays`, `hr_attendance`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\att_sheet_batch.py`
  - **النماذج الجديدة (`_name`):** `attendance.sheet.batch`, `attendance.sheet`, `batch_id`, `hr.payslip.run`
- **الملف:** `models\hr_attendance_policy.py`
  - **النماذج الجديدة (`_name`):** `hr.attendance.policy`, `hr.overtime.rule`, `hr.late.rule`, `hr.absence.rule`, `hr.diff.rule`, `hr.policy.overtime.line`, `hr.overtime.rule`, `hr.attendance.policy`, `hr.overtime.rule`, `hr.late.rule`, `hr.late.rule.line`, `late_id`, `hr.late.rule.line`, `hr.late.rule`, `hr.diff.rule`, `hr.diff.rule.line`, `diff_id`, `hr.diff.rule.line`, `hr.diff.rule`, `hr.absence.rule`, `hr.absence.rule.line`, `absence_id`, `hr.absence.rule.line`, `hr.absence.rule`
  - **الوصف:** Attendance Sheet Policies
- **الملف:** `models\hr_attendance_sheet.py`
  - **النماذج الجديدة (`_name`):** `attendance.sheet`, `hr.employee`, `attendance.sheet.batch`, `attendance.sheet.line`, `att_sheet_id`, `hr.attendance.policy`, `hr.payslip`, `attendance.sheet.line`, `attendance.sheet`
  - **النماذج المعدلة (`_inherit`):** `hr.attendance`, `hr.payslip`, `mail.thread.cc, mail.activity.mixin`
  - **الوصف:** Hr Attendance Sheet
- **الملف:** `models\hr_contract.py`
  - **النماذج المعدلة (`_inherit`):** `hr.contract`
  - **الوصف:** Employee Contract
- **الملف:** `models\hr_employee.py`
  - **النماذج المعدلة (`_inherit`):** `hr.employee`
- **الملف:** `models\hr_holidays.py`
  - **النماذج الجديدة (`_name`):** `hr.public.holiday`, `hr.employee`, `hr.department`, `hr.employee.category`
  - **النماذج المعدلة (`_inherit`):** `mail.thread`
  - **الوصف:** hr.public.holiday
- **الملف:** `models\hr_leave_type.py`
  - **النماذج المعدلة (`_inherit`):** `hr.leave.type`
- **الملف:** `models\hr_payroll.py`
  - **النماذج الجديدة (`_name`):** `attendance.sheet`, `payslip_id`
  - **النماذج المعدلة (`_inherit`):** `hr.payslip`
- **الملف:** `models\resource.py`
  - **النماذج المعدلة (`_inherit`):** `resource.calendar`
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`, `res.config.settings`
- **الملف:** `models\utils.py`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\data.xml`, `data\ir_cron.xml`, `data\ir_sequence.xml`, `demo\demo.xml`, `security\rule.xml`, `security\security.xml`, `views\attendance_sheet_batch_view.xml`, `views\hr_attendance_policy_view.xml`, `views\hr_attendance_sheet_view.xml`, `views\hr_contract_view.xml`, `views\hr_leave_type_view.xml`, `views\hr_payslip_view.xml`, `views\hr_public_holiday_view.xml`, `views\resource_view.xml`, `views\res_config_settings.xml`, `wizard\change_att_data_view.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `HR Attendance Sheet And Policies` أو `rm_hr_attendance_sheet` والضغط على **تثبيت (Install)**.
