# Al-Ramlaa HR Customization (`alramlaa_hr_custom`)

## 📌 الوصف العام (Overview)
Custom HR fields for Al-Ramlaa Project (Family & Insurance)

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_hr_custom`
- **التصنيف (Category):** `Human Resources`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`, `hr`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\employee.py`
  - **النماذج الجديدة (`_name`):** `hr.employee.family`
  - **النماذج المعدلة (`_inherit`):** `hr.employee`
  - **الوصف:** Employee Family Details

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\employee_view.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Al-Ramlaa HR Customization` أو `alramlaa_hr_custom` والضغط على **تثبيت (Install)**.
