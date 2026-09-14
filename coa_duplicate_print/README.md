# COA Duplicate Print Watermark (`coa_duplicate_print`)

## 📌 الوصف العام (Overview)
Show a DUPLICATE watermark when a document is re-printed

### التفاصيل الوظيفية:

COA Duplicate Print Watermark
=============================
Counts how many times a document has been printed to PDF and shows a big
rotated "DUPLICATE - مكرر - Copy #N" watermark from the 2nd print onwards.

* Supported documents: Sale Order / Quotation, Delivery Slip (stock.picking).
* Configurable in General Settings: Disabled / Inventory only / Sales only /
  Inventory and Sales.
* The counter only increases on a real PDF print, not when opening the form.
* Print info (count, date, user) is visible on the document form.
* A "Reset Print Count" server action is available to treat the next print as
  the original again.

Developed by Community of Accountants (COA) - Odoo Silver Partner
WhatsApp: +20 101 390 7174
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_duplicate_print`
- **التصنيف (Category):** `Technical`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `base_setup`, `sale`, `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\coa_duplicate_print_mixin.py`
  - **النماذج الجديدة (`_name`):** `coa.duplicate.print.mixin`
  - **الوصف:** Duplicate Print Mixin
- **الملف:** `models\ir_actions_report.py`
  - **النماذج المعدلة (`_inherit`):** `ir.actions.report`
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`, `res.config.settings`
- **الملف:** `models\sale_order.py`
  - **النماذج الجديدة (`_name`):** `sale.order`
  - **النماذج المعدلة (`_inherit`):** `sale.order, coa.duplicate.print.mixin`
- **الملف:** `models\stock_picking.py`
  - **النماذج الجديدة (`_name`):** `stock.picking`
  - **النماذج المعدلة (`_inherit`):** `stock.picking, coa.duplicate.print.mixin`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\server_actions.xml`, `report\coa_duplicate_print_templates.xml`, `views\res_config_settings_views.xml`, `views\sale_order_views.xml`, `views\stock_picking_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Duplicate Print Watermark` أو `coa_duplicate_print` والضغط على **تثبيت (Install)**.
