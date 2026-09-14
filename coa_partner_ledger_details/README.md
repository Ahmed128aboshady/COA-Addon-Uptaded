# COA Partner Ledger - Invoice Details Drill-down (`coa_partner_ledger_details`)

## 📌 الوصف العام (Overview)
Adds an expandable arrow next to each invoice in the Partner Ledger. Unfolding shows the invoice product lines with quantity and total.

### التفاصيل الوظيفية:

COA Partner Ledger - Invoice Details Drill-down
===============================================
Extends the Enterprise Partner Ledger report (account_reports) so that every
invoice / journal-item line becomes unfoldable. When you click its arrow, the
report expands into the invoice's PRODUCT LINES, showing:

    Product name  -  Quantity (UoM)   |   Line Total

How it works (framework-safe):
------------------------------
* Inherits the report custom handler
  'account.partner.ledger.report.handler'.
* After the standard partner expansion runs, each move line that belongs to
  an invoice is tagged unfoldable with a custom expand function.
* Child (product) lines are built with the OFFICIAL
  account.report._get_generic_line_id() helper - no hand-crafted line IDs,
  so _parse_line_id never breaks.
* No change to the account.report data record and no new columns: the line
  total is rendered in the existing Balance column, and the quantity is shown
  in the line label (the Partner Ledger has fixed Debit/Credit/Balance
  columns).

Requires: Odoo Enterprise (account_reports).

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_partner_ledger_details`
- **التصنيف (Category):** `Accounting/Accounting`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `account_reports`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_partner_ledger.py`
  - **النماذج المعدلة (`_inherit`):** `account.partner.ledger.report.handler`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Partner Ledger - Invoice Details Drill-down` أو `coa_partner_ledger_details` والضغط على **تثبيت (Install)**.
