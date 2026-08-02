# Duplicate Company Data PRO (`alramlaa_company_duplicator`)

## 📌 الوصف العام (Overview)
Seamlessly duplicate Chart of Accounts, Taxes, Journals, and Warehouses for Multi-Company Setup

### التفاصيل الوظيفية:

        This module allows you to safely duplicate essential accounting and inventory configurations 
        from one company to another in a multi-company environment.
        Fully compatible with Odoo 19 new shared accounts architecture.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_company_duplicator`
- **التصنيف (Category):** `Administration`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`, `account`, `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\company_wizard.py`
  - **النماذج الجديدة (`_name`):** `company.duplicator.wizard`
  - **الوصف:** Duplicate Company Data Wizard Pro

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\wizard_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Duplicate Company Data PRO` أو `alramlaa_company_duplicator` والضغط على **تثبيت (Install)**.
