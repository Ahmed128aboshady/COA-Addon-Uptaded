# Sale Order Return (`sale_order_return`)

## 📌 الوصف العام (Overview)
Create return transfers directly from sales orders

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_order_return`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\sale_order_views.xml`, `wizard\sale_return_wizard_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Order Return` أو `sale_order_return` والضغط على **تثبيت (Install)**.
