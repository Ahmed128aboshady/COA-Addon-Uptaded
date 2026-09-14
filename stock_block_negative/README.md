# Block Negative Stock (`stock_block_negative`)

## 📌 الوصف العام (Overview)
Prevent stock levels from going negative anywhere in the system (manufacturing, deliveries, internal transfers, POS, adjustments via moves).

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `stock_block_negative`
- **التصنيف (Category):** `Inventory/Inventory`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product_category.py`
  - **النماذج المعدلة (`_inherit`):** `product.category`
- **الملف:** `models\product_product.py`
  - **النماذج المعدلة (`_inherit`):** `product.template`
- **الملف:** `models\stock_location.py`
  - **النماذج المعدلة (`_inherit`):** `stock.location`
- **الملف:** `models\stock_quant.py`
  - **النماذج المعدلة (`_inherit`):** `stock.quant`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\stock_block_negative_security.xml`, `views\product_views.xml`, `views\stock_location_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Block Negative Stock` أو `stock_block_negative` والضغط على **تثبيت (Install)**.
