# COA: Sales Order Quantity Adjust (Draft Pickings) (`coa_so_qty_adjust`)

## 📌 الوصف العام (Overview)
Decrease draft delivery quantities in place instead of creating a delivery + return when the SO quantity is reduced.

### التفاصيل الوظيفية:

COA - Sales Order Quantity Adjustment
=====================================

When a confirmed Sales Order line quantity is decreased, standard Odoo
creates a negative procurement which results in a return move, even if the
original delivery is still in **draft**.

This module intercepts that case: as long as the related delivery moves are
still not done (draft / confirmed / waiting / assigned), it reduces the
existing outgoing move quantity in place instead of generating a return.

Behaviour:

* Quantity decreased, picking still not delivered  -> existing move reduced.
* Quantity decreased below already-delivered qty    -> standard behaviour (return).
* Any part of the line already delivered (done)      -> standard behaviour (return).
* Quantity increased                                 -> standard behaviour (new procurement).


---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_so_qty_adjust`
- **التصنيف (Category):** `Sales/Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA: Sales Order Quantity Adjust (Draft Pickings)` أو `coa_so_qty_adjust` والضغط على **تثبيت (Install)**.
