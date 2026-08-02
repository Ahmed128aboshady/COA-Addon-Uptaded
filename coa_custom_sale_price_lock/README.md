# Custom Sale Price Lock (`custom_sale_price_lock`)

## 📌 الوصف العام (Overview)
Lock sale order line unit price and allow editing for specific users only.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `custom_sale_price_lock`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `1.0`
- **الاعتماديات (Dependencies):** `sale_management`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\security.xml`, `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Custom Sale Price Lock` أو `custom_sale_price_lock` والضغط على **تثبيت (Install)**.
