# Custom Date Order (`custom_date_order`)

## 📌 الوصف العام (Overview)
تطوير وتخصيص في بيئة أودو.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `custom_date_order`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `18.0.1.0`
- **الاعتماديات (Dependencies):** `sale`, `purchase`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\purchase_order.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\purchase_order_view.xml`, `views\sale_order_view.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Custom Date Order` أو `custom_date_order` والضغط على **تثبيت (Install)**.
