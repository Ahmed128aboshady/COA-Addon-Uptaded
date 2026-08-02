# Sale Price Edit Permission (`sale_price_security`)

## 📌 الوصف العام (Overview)
Add a checkbox permission to control who can edit sale order prices

### التفاصيل الوظيفية:

Adds a new group "Can Edit Sale Prices" that appears as a checkbox
in the user access rights page under the Sales section.

When a user does NOT have this permission, the Unit Price field
in sale order lines becomes read-only for them.

By default the group is granted to:
- Administrators
- Sales / Administrator (Sales Manager)
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_price_security`
- **التصنيف (Category):** `Sales/Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_management`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\groups.xml`, `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Price Edit Permission` أو `sale_price_security` والضغط على **تثبيت (Install)**.
