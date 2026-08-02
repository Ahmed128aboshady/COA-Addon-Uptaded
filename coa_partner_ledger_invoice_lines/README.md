# Partner Ledger Invoice Lines (`partner_ledger_invoice_lines`)

## 📌 الوصف العام (Overview)
Display invoice lines details in Partner Ledger Report

### التفاصيل الوظيفية:

Partner Ledger Invoice Lines
=============================

This module extends the Partner Ledger Report to display invoice line items
(products) under each invoice entry in an expandable/collapsible format.

Features:
---------
* Expandable invoice lines under each invoice/bill entry
* Display product name, quantity, unit price
* Show amounts in Debit/Credit/Balance columns
* Support for all invoice types (invoices, bills, refunds)
* Clean and professional formatting
* Maintains report performance with on-demand loading

Usage:
------
1. Go to Accounting > Reporting > Partner Ledger
2. Expand any partner line to see their invoices
3. Click the expand icon on any invoice to see its line items
4. Each line shows: Product | Qty × Price with amounts

Technical:
----------
* Inherits: account.partner.ledger.report.handler
* Adds unfoldable functionality to move lines
* Custom expand function for invoice lines
* Filters only product lines (excludes sections/notes)



---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `partner_ledger_invoice_lines`
- **التصنيف (Category):** `Accounting/Reporting`
- **الإصدار (Version):** `1.4`
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
3. البحث عن `Partner Ledger Invoice Lines` أو `partner_ledger_invoice_lines` والضغط على **تثبيت (Install)**.
