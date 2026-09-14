# COA Journal Dashboard – GL Balance (`coa_journal_gl_balance`)

## 📌 الوصف العام (Overview)
Show the General Ledger balance on the bank/cash journal dashboard instead of the statement-based balance. For foreign-currency journals, shows both the foreign-currency amount and the company-currency equivalent on two lines.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_journal_gl_balance`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `19.0.2.0.0`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_journal.py`
  - **النماذج المعدلة (`_inherit`):** `account.journal`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Journal Dashboard – GL Balance` أو `coa_journal_gl_balance` والضغط على **تثبيت (Install)**.
