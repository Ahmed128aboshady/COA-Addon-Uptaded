# Sale Line Reserved Location Detail (`sale_stock_location_detail`)

## 📌 الوصف العام (Overview)
Show reserved sub-locations per SO line (from stock.move.line) in SO, invoice & print

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_stock_location_detail`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `account.move.line`, `sale.order`
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`, `sale.order`, `stock.picking`
- **الملف:** `models\stock_move.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`, `stock.move`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\sale_order_report.xml`, `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Line Reserved Location Detail` أو `sale_stock_location_detail` والضغط على **تثبيت (Install)**.
