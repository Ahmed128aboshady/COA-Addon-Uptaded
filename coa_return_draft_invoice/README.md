# COA Adjust Draft Invoice on Stock Return (`coa_return_draft_invoice`)

## 📌 الوصف العام (Overview)
When a warehouse return of a Sale Order is validated, the linked DRAFT customer invoice is automatically reduced by the returned quantities. Audit-trail safe (never touches posted entries).

### التفاصيل الوظيفية:

COA Adjust Draft Invoice on Stock Return
========================================
Business case:
--------------
A customer invoice is created in DRAFT (before posting). Later, some goods
are returned from the warehouse against the same Sale Order. Standard Odoo
does NOT sync the already-created draft invoice with the return, so the
draft still shows the old (higher) quantities.

What this module does:
----------------------
On validation of a return picking:
  1. Detects the return moves (moves with origin_returned_move_id).
  2. Finds the related Sale Order through the original delivery move.
  3. Finds that order's DRAFT customer invoice(s).
  4. Reduces the matching invoice line quantity by the returned quantity
     (UoM-aware). Lines that reach zero are removed.
  5. Logs a note in the invoice chatter for traceability.

Why draft only (audit trail safe):
-----------------------------------
The module never modifies a POSTED invoice, so it fully respects the
Accounting Audit Trail. For posted invoices the correct accounting action
is a Credit Note (reversal) - available as an optional extension.

Notes:
------
* The adjustment runs inside a guarded block: if anything fails, the
  warehouse operation is NOT blocked (error is logged instead).
* Trigger is narrow: only return moves linked to a Sale Order that has a
  draft customer invoice.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_return_draft_invoice`
- **التصنيف (Category):** `Inventory/Sales`
- **الإصدار (Version):** `18.0.1.3.0`
- **الاعتماديات (Dependencies):** `sale_stock`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Adjust Draft Invoice on Stock Return` أو `coa_return_draft_invoice` والضغط على **تثبيت (Install)**.
