# Location & Warehouse Code (`location_warehouse_code`)

## 📌 الوصف العام (Overview)
Add code field to Location and Warehouse configuration

### التفاصيل الوظيفية:

        This module adds a 'Code' field after the 'Name' field in:
        - Stock Location configuration
        - Warehouse configuration
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `location_warehouse_code`
- **التصنيف (Category):** `Inventory/Configuration`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\stock_location.py`
  - **النماذج المعدلة (`_inherit`):** `stock.location`
- **الملف:** `models\stock_warehouse.py`
  - **النماذج المعدلة (`_inherit`):** `stock.warehouse`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\stock_location_views.xml`, `views\stock_warehouse_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Location & Warehouse Code` أو `location_warehouse_code` والضغط على **تثبيت (Install)**.
