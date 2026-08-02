# Arfad HR Allowances (`arfad_hr_allowances`)

## 📌 الوصف العام (Overview)
Add 5 allowance fields to employee form

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arfad_hr_allowances`
- **التصنيف (Category):** `Human Resources`
- **الإصدار (Version):** `1.1`
- **الاعتماديات (Dependencies):** `hr`, `hr_payroll`, `l10n_sa_hr_payroll`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\hr_employee.py`
  - **النماذج المعدلة (`_inherit`):** `hr.employee`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\hr_employee_view.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Arfad HR Allowances` أو `arfad_hr_allowances` والضغط على **تثبيت (Install)**.
