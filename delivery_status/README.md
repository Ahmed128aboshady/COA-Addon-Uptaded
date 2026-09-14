# Delivery Status in Sales Order (`delivery_status`)

## 📌 الوصف العام (Overview)
Show delivery status in sales order form

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `delivery_status`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `1.0`
- **الاعتماديات (Dependencies):** `sale`, `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order_delivery.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\sale_order_delivery_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Delivery Status in Sales Order` أو `delivery_status` والضغط على **تثبيت (Install)**.
