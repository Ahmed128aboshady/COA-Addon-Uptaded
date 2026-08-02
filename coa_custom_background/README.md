# Custom Background (`custom_background`)

## 📌 الوصف العام (Overview)
Custom Background

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `custom_background`
- **التصنيف (Category):** `GenericModules`
- **الإصدار (Version):** `18.0.1.0.2`
- **الاعتماديات (Dependencies):** `base`, `web`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\report.py`
  - **النماذج الجديدة (`_name`):** `report.background.line`, `ir.actions.report`, `res.lang`
  - **النماذج المعدلة (`_inherit`):** `ir.actions.report`
  - **الوصف:** Report Background Line
- **الملف:** `models\report_background_lang.py`
  - **النماذج الجديدة (`_name`):** `report.background.lang`, `res.lang`, `ir.actions.report`
  - **الوصف:** Report Background Line Per Language
- **الملف:** `models\report_company_background_lang.py`
  - **النماذج الجديدة (`_name`):** `report.company.background.lang`
  - **الوصف:** Report Company Background Line Per Language
- **الملف:** `models\res_company.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\ir_actions.xml`, `views\res_company_view.xml`
- **ملفات التقارير (`Reports`):** `views\ir_actions.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Custom Background` أو `custom_background` والضغط على **تثبيت (Install)**.
