# Sale Stock Reserved (`sale_stock_reserved`)

## 📌 الوصف العام (Overview)
Report of reserved stock by customer and product from sales orders, with unreserve button

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_stock_reserved`
- **التصنيف (Category):** `Inventory/Reporting`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product_product.py`
  - **النماذج المعدلة (`_inherit`):** `product.product`
- **الملف:** `models\res_partner.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`
- **الملف:** `models\sale_stock_reserved.py`
  - **النماذج الجديدة (`_name`):** `sale.stock.reserved`, `product_id`
  - **الوصف:** Sale Stock Reservation Report

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\sale_stock_reserved_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Stock Reserved` أو `sale_stock_reserved` والضغط على **تثبيت (Install)**.
