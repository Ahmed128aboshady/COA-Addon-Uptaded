# COA Invoice Report (`coa_invoice_report`)

## 📌 الوصف العام (Overview)
Custom Layout for Tax Invoice Report

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_invoice_report`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `19.0.1.0.9`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\report_invoice_template.xml`
- **ملفات التقارير (`Reports`):** `views\report_invoice_template.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Invoice Report` أو `coa_invoice_report` والضغط على **تثبيت (Install)**.
