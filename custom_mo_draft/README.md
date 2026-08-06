# MO Draft on Sale Confirm (`custom_mo_draft`)

## 📌 الوصف العام (Overview)
Keep Manufacturing Orders in Draft when created from Sale Orders

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `custom_mo_draft`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\stock_rule.py`
  - **النماذج المعدلة (`_inherit`):** `stock.rule`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `MO Draft on Sale Confirm` أو `custom_mo_draft` والضغط على **تثبيت (Install)**.
