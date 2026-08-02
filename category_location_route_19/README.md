# Category Location Route (`category_location_route_19`)

## 📌 الوصف العام (Overview)
Auto-create routes from product category location settings

### التفاصيل الوظيفية:

        Add sales and manufacturing source locations to product categories.
        The addon automatically creates/updates routes and procurement rules
        so each product is pulled from its category's designated location.
        Returns go back to the same source location automatically.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `category_location_route_19`
- **التصنيف (Category):** `Inventory`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`, `sale_stock`, `mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product_category.py`
  - **النماذج المعدلة (`_inherit`):** `product.category`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\product_category_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Category Location Route` أو `category_location_route_19` والضغط على **تثبيت (Install)**.
