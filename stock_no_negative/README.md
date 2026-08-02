# Stock Disallow Negative (`stock_no_negative`)

## 📌 الوصف العام (Overview)
Disallow negative stock levels by default

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `stock_no_negative`
- **التصنيف (Category):** `Inventory, Logistic, Storage`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product.py`
  - **النماذج المعدلة (`_inherit`):** `product.category`, `product.template`
- **الملف:** `models\stock_location.py`
  - **النماذج المعدلة (`_inherit`):** `stock.location`
- **الملف:** `models\stock_quant.py`
  - **النماذج المعدلة (`_inherit`):** `stock.quant`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\product_product_views.xml`, `views\stock_location_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Stock Disallow Negative` أو `stock_no_negative` والضغط على **تثبيت (Install)**.
