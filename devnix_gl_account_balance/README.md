# GL Balance in Accounting Dashboard (`devnix_gl_account_balance`)

## 📌 الوصف العام (Overview)
تطوير وتخصيص في بيئة أودو.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `devnix_gl_account_balance`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `1.0`
- **الاعتماديات (Dependencies):** `base`, `account_accountant`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\models.py`
  - **النماذج المعدلة (`_inherit`):** `account.journal`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\account_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `GL Balance in Accounting Dashboard` أو `devnix_gl_account_balance` والضغط على **تثبيت (Install)**.
