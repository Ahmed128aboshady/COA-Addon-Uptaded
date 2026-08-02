# Sale: Stock Info in Product Search (`sale_product_stock_info`)

## 📌 الوصف العام (Overview)
يظهر الكمية المتاحة والـ On Hand في سيرش المنتجات داخل المبيعات

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_product_stock_info`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product_product.py`
  - **النماذج المعدلة (`_inherit`):** `product.product`, `product.template`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\product_search_more_views.xml`, `views\sale_order_line_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale: Stock Info in Product Search` أو `sale_product_stock_info` والضغط على **تثبيت (Install)**.
