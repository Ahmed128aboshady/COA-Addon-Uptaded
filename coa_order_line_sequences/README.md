# Order Line Sequences/Line Numbers (`order_line_sequences`)

## 📌 الوصف العام (Overview)
Sequence numbers in order lines of sales,purchase and delivery.

### التفاصيل الوظيفية:
This module will help you to add sequence for order lines
    in sales, purchase and delivery. It will also add line numbers in report lines.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `order_line_sequences`
- **التصنيف (Category):** `Extra Tools`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`, `sale_management`, `purchase`, `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\purchase_order.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order.line`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`
- **الملف:** `models\stock.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move`, `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\purchase_order_templates.xml`, `views\purchase_order_views.xml`, `views\sale_order_templates.xml`, `views\sale_order_views.xml`, `views\stock_picking_templates.xml`, `views\stock_picking_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Order Line Sequences/Line Numbers` أو `order_line_sequences` والضغط على **تثبيت (Install)**.
