# COA Quantity Available Warning (`coa_qty_available_warning`)

## 📌 الوصف العام (Overview)
Soft warning when the ordered quantity exceeds the free-to-use stock

### التفاصيل الوظيفية:

COA Quantity Available Warning
==============================
Shows a non-blocking warning when the requested quantity is greater than the
quantity available (Free To Use) across the whole company:

* Sale Order Line: an onchange warning appears while entering the quantity or
  the product, showing the available quantity. The user can still proceed.
* Delivery (stock.picking): on validation, a confirmation dialog lists the
  products short on stock. The user can press "Confirm Anyway" to continue.

Nothing is blocked - the warning is informative only.

Developed by Community of Accountants (COA) - Odoo Silver Partner
WhatsApp: +20 101 390 7174
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_qty_available_warning`
- **التصنيف (Category):** `Sales/Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`, `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`, `res.config.settings`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\res_config_settings_views.xml`, `views\sale_order_views.xml`, `wizard\qty_warning_wizard_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Quantity Available Warning` أو `coa_qty_available_warning` والضغط على **تثبيت (Install)**.
