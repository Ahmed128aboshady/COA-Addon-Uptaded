# HR Loan Accounting (`hr_loan_accounting`)

## 📌 الوصف العام (Overview)
Accounting integration for HR Loans

### التفاصيل الوظيفية:
Adds journal entry creation on loan approval, smart button for journal entries, and installment delay wizard.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `hr_loan_accounting`
- **التصنيف (Category):** `Human Resources`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `ent_ohrms_loan`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\hr_loan.py`
  - **النماذج المعدلة (`_inherit`):** `hr.loan`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\delay_installments_views.xml`, `views\hr_loan_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `HR Loan Accounting` أو `hr_loan_accounting` والضغط على **تثبيت (Install)**.
