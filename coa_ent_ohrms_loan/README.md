# Enterprise OpenHRMS Loan Management (`ent_ohrms_loan`)

## 📌 الوصف العام (Overview)
Manage Loan Requests

### التفاصيل الوظيفية:
Seamlessly manage and track loan requests from your 
    company's staff, ensuring a smooth and transparent approval process.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `ent_ohrms_loan`
- **التصنيف (Category):** `Generic Modules/Human Resources`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`, `hr_payroll`, `hr`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\hr_employee.py`
  - **النماذج المعدلة (`_inherit`):** `hr.employee`
- **الملف:** `models\hr_loan.py`
  - **النماذج الجديدة (`_name`):** `hr.loan`, `hr.employee`, `hr.department`, `hr.loan.line`, `loan_id`, `res.company`, `res.currency`, `hr.job`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Loan Request
- **الملف:** `models\hr_loan_line.py`
  - **النماذج الجديدة (`_name`):** `hr.loan.line`, `hr.employee`, `hr.loan`, `hr.payslip`
  - **الوصف:** Installment Line
- **الملف:** `models\hr_payroll_structure.py`
  - **النماذج الجديدة (`_name`):** `res.company`
  - **النماذج المعدلة (`_inherit`):** `hr.payroll.structure`
- **الملف:** `models\hr_payslip.py`
  - **النماذج المعدلة (`_inherit`):** `hr.payslip`
- **الملف:** `models\hr_payslip_input.py`
  - **النماذج الجديدة (`_name`):** `hr.loan.line`
  - **النماذج المعدلة (`_inherit`):** `hr.payslip.input`
- **الملف:** `models\hr_payslip_input_type.py`
  - **النماذج الجديدة (`_name`):** `hr.salary.rule`
  - **النماذج المعدلة (`_inherit`):** `hr.payslip.input.type`
- **الملف:** `models\hr_salary_rule.py`
  - **النماذج الجديدة (`_name`):** `res.company`
  - **النماذج المعدلة (`_inherit`):** `hr.salary.rule`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\hr_payroll_structure_data.xml`, `data\hr_payslip_input_type_data.xml`, `data\hr_salary_rule_data.xml`, `data\ir_sequence_data.xml`, `security\hr_loan_security.xml`, `views\hr_employee_views.xml`, `views\hr_loan_views.xml`, `views\hr_payroll_structure_views.xml`, `views\hr_payslip_views.xml`, `views\hr_salary_rule_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Enterprise OpenHRMS Loan Management` أو `ent_ohrms_loan` والضغط على **تثبيت (Install)**.
