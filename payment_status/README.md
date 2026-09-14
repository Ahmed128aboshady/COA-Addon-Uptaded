# Payment Status on Delivery (`payment_status`)

## 📌 الوصف العام (Overview)
Shows invoice payment status automatically on delivery orders

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `payment_status`
- **التصنيف (Category):** `Inventory`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`, `purchase_stock`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\stock_picking_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Payment Status on Delivery` أو `payment_status` والضغط على **تثبيت (Install)**.
