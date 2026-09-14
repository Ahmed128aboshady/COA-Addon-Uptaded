# Warehouse Location Restriction (`ts_location_restrictions`)

## 📌 الوصف العام (Overview)
Restrict warehouse/stock locations and operation types per user

### التفاصيل الوظيفية:

Warehouse Location Restriction
================================
Restrict inventory users' access to specific warehouses, transfer locations,
and operation types on an individual basis. Users can only access designated locations.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `ts_location_restrictions`
- **التصنيف (Category):** `Inventory/Warehouse`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`, `mail`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product_product.py`
  - **النماذج المعدلة (`_inherit`):** `product.product`, `product.template`
- **الملف:** `models\res_users.py`
  - **النماذج الجديدة (`_name`):** `stock.warehouse`, `stock.location`, `stock.picking.type`
  - **النماذج المعدلة (`_inherit`):** `res.users`
- **الملف:** `models\stock_location.py`
  - **النماذج المعدلة (`_inherit`):** `stock.location`
- **الملف:** `models\stock_move.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move`, `stock.move.line`
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`
- **الملف:** `models\stock_warehouse.py`
  - **النماذج المعدلة (`_inherit`):** `stock.warehouse`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\security.xml`, `views\res_users_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Warehouse Location Restriction` أو `ts_location_restrictions` والضغط على **تثبيت (Install)**.
