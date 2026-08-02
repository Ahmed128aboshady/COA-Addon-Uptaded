# Warehouse Restrictions (`warehouse_stock_restrictions`)

## 📌 الوصف العام (Overview)

         Warehouse and Stock Location Restriction on Users.

### التفاصيل الوظيفية:

        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `warehouse_stock_restrictions`
- **التصنيف (Category):** `Warehouse`
- **الإصدار (Version):** `1.0`
- **الاعتماديات (Dependencies):** `base`, `stock`, `sale`, `mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `stock.py`
  - **النماذج المعدلة (`_inherit`):** `res.users`, `stock.move`, `stock.return.picking`, `sale.order`, `mrp.production`, `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `users_view.xml`, `security\security.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Warehouse Restrictions` أو `warehouse_stock_restrictions` والضغط على **تثبيت (Install)**.
