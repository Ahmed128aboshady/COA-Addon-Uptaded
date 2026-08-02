# Edit Sale Order Date (`edit_order_date`)

## 📌 الوصف العام (Overview)
Change the order date for particular user group

### التفاصيل الوظيفية:
We can change the order date of the confirmed sale order.The access for the editing the order date can berestricted to particular user group. The user who have no access to edit the field got a user error while trying tochange the field

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `edit_order_date`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_management`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\edit_order_date_groups.xml`, `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Edit Sale Order Date` أو `edit_order_date` والضغط على **تثبيت (Install)**.
