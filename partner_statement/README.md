# Partner Statement Report (`partner_statement`)

## 📌 الوصف العام (Overview)
Partner Account Statement Report with Opening Balance

### التفاصيل الوظيفية:

        Generates a partner account statement report showing:
        - Opening balance before the selected period
        - All debit/credit transactions within the period
        - Running balance per line
        - Totals at the bottom
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `partner_statement`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
لا توجد نماذج بايثون مخصصة أو معقدة.

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\partner_statement_report.xml`, `report\partner_statement_template.xml`, `wizard\partner_statement_wizard_views.xml`
- **ملفات التقارير (`Reports`):** `report\partner_statement_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Partner Statement Report` أو `partner_statement` والضغط على **تثبيت (Install)**.
