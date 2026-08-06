# Al-Ramlaa Custom HR Updates (`alramlaa_custom_hr_updates`)

## 📌 الوصف العام (Overview)
Customizations for HR Units, Departments, and Kafala Status

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_custom_hr_updates`
- **التصنيف (Category):** `Human Resources`
- **الإصدار (Version):** `1.0`
- **الاعتماديات (Dependencies):** `base`, `hr`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\hr_custom.py`
  - **النماذج الجديدة (`_name`):** `hr.unit`
  - **النماذج المعدلة (`_inherit`):** `hr.department`, `hr.job`, `hr.employee`
  - **الوصف:** HR Unit
- **الملف:** `models\hr_employee_custom.py`
  - **النماذج الجديدة (`_name`):** `hr.employee.family`
  - **النماذج المعدلة (`_inherit`):** `hr.employee`
  - **الوصف:** Employee Family Details

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\hr_custom_views.xml`, `views\hr_employee_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Al-Ramlaa Custom HR Updates` أو `alramlaa_custom_hr_updates` والضغط على **تثبيت (Install)**.
