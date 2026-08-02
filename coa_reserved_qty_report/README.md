# Reserved Qty Report (`reserved_qty_report`)

## 📌 الوصف العام (Overview)
Report showing reserved products in sales orders

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `reserved_qty_report`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `1.0`
- **الاعتماديات (Dependencies):** `sale`, `stock`, `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`
- **الملف:** `models\stock_move.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\reserved_report_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Reserved Qty Report` أو `reserved_qty_report` والضغط على **تثبيت (Install)**.
