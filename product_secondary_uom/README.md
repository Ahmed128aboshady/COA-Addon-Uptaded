# Product Secondary Unit of Measure (`product_secondary_uom`)

## 📌 الوصف العام (Overview)
Independent secondary UoM tracked alongside the primary UoM on products

### التفاصيل الوظيفية:

        Adds an independent secondary unit of measure on products.
        The secondary UoM is completely independent - no mathematical conversion
        between primary and secondary. Example: a product tracked as "2 Tons AND 3 Reels".
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `product_secondary_uom`
- **التصنيف (Category):** `Inventory/Inventory`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `product`, `sale_stock`, `purchase_stock`, `stock`, `mrp`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `account.move.line`
- **الملف:** `models\mrp_bom_line.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.bom.line`
- **الملف:** `models\mrp_production.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.production`
- **الملف:** `models\product_product.py`
  - **النماذج المعدلة (`_inherit`):** `product.product`
- **الملف:** `models\product_template.py`
  - **النماذج المعدلة (`_inherit`):** `product.template`
- **الملف:** `models\purchase_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order.line`
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`
- **الملف:** `models\stock_move.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move`
- **الملف:** `models\stock_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move.line`
- **الملف:** `models\stock_quant.py`
  - **النماذج المعدلة (`_inherit`):** `stock.quant`
- **الملف:** `models\stock_rule.py`
  - **النماذج المعدلة (`_inherit`):** `stock.rule`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\account_move_views.xml`, `views\mrp_bom_views.xml`, `views\mrp_production_views.xml`, `views\product_template_views.xml`, `views\purchase_order_views.xml`, `views\sale_order_views.xml`, `views\stock_move_views.xml`, `views\stock_picking_views.xml`, `views\stock_product_views.xml`, `views\stock_quant_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Product Secondary Unit of Measure` أو `product_secondary_uom` والضغط على **تثبيت (Install)**.
