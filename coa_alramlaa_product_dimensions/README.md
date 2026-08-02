# Alramlaa Product Dimensions (`alramlaa_product_dimensions`)

## 📌 الوصف العام (Overview)
Add Length, Width, Thickness, Square/Cubic Meter and Waste % to products

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_product_dimensions`
- **التصنيف (Category):** `Inventory/Products`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `product`, `purchase`, `stock`, `account_asset`, `mrp`, `base`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_asset.py`
  - **النماذج المعدلة (`_inherit`):** `account.asset`
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\account_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `account.move.line`
- **الملف:** `models\asset_category.py`
  - **النماذج الجديدة (`_name`):** `asset.category`, `parent_id`
  - **الوصف:** Asset Category
- **الملف:** `models\mrp_bom.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.bom.line`
- **الملف:** `models\product_product.py`
  - **النماذج المعدلة (`_inherit`):** `product.product`
- **الملف:** `models\product_template.py`
  - **النماذج المعدلة (`_inherit`):** `product.template`
- **الملف:** `models\purchase_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order.line`
- **الملف:** `models\stock_move.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move`
- **الملف:** `models\stock_quant.py`
  - **النماذج المعدلة (`_inherit`):** `stock.quant`, `stock.location`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\company_migration_action.xml`, `views\account_asset_views.xml`, `views\account_move_views.xml`, `views\asset_category_views.xml`, `views\mrp_views.xml`, `views\product_template_views.xml`, `views\purchase_order_views.xml`, `views\report_invoice_custom.xml`, `views\stock_report_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Alramlaa Product Dimensions` أو `alramlaa_product_dimensions` والضغط على **تثبيت (Install)**.
