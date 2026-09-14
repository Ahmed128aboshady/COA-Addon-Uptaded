# COA Sale Order - Direct Invoice Print (`coa_so_print_invoice`)

## 📌 الوصف العام (Overview)
Print the Sale Order invoice(s) directly from the SO with one click. Opens the browser print dialog immediately (no download). Works for Sales users without Accounting access.

### التفاصيل الوظيفية:

COA Sale Order - Direct Invoice Print
=====================================
- Adds a "Print Invoice" button on the Sale Order header.
- One click opens the invoice PDF and fires the browser print dialog
  automatically (inline preview, NOT a download).
- Salespeople can print the invoice even without Accounting access:
  access is validated on the Sale Order itself, then the invoice
  report is rendered server-side with elevated rights (safe scope:
  only invoices linked to that Sale Order).
- If the SO has multiple posted invoices, they are merged in one PDF.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_so_print_invoice`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Sale Order - Direct Invoice Print` أو `coa_so_print_invoice` والضغط على **تثبيت (Install)**.
