# Alramlaa Partner Name Translation (`alramlaa_partner_translate`)

## 📌 الوصف العام (Overview)
Make partner name translatable (Arabic/English)

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_partner_translate`
- **التصنيف (Category):** `Contacts`
- **الإصدار (Version):** `19.0.1.1.1`
- **الاعتماديات (Dependencies):** `contacts`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\res_company.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`
- **الملف:** `models\res_partner.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\res_partner_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Alramlaa Partner Name Translation` أو `alramlaa_partner_translate` والضغط على **تثبيت (Install)**.
