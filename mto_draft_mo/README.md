# MTO Manufacturing Order - Keep Draft (`mto_draft_mo`)

## 📌 الوصف العام (Overview)
Keep MO in Draft state when created from Sales Order via MTO route

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `mto_draft_mo`
- **التصنيف (Category):** `Manufacturing`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `mrp`, `sale_mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\mrp_production.py`
  - **النماذج المعدلة (`_inherit`):** `stock.rule`, `mrp.production`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `MTO Manufacturing Order - Keep Draft` أو `mto_draft_mo` والضغط على **تثبيت (Install)**.
