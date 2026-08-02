# Sales Commission by Customer Tag (`commission_sales`)

## 📌 الوصف العام (Overview)
Calculate sales commissions based on customer tag and net sales

### التفاصيل الوظيفية:

        Sales Commission Module
        ========================
        - Calculates commission from net sales (Invoice Analysis)
        - Rate is determined based on the customer tag
        - Tags and rates can be added and modified from the Settings
        - Comprehensive report for each salesperson
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `commission_sales`
- **التصنيف (Category):** `Sales/Commission`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_management`, `account`, `crm`, `mail`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\commission_line.py`
  - **النماذج الجديدة (`_name`):** `commission.line`, `commission.line.detail`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** سطر العمولة
- **الملف:** `models\commission_payment.py`
  - **النماذج الجديدة (`_name`):** `commission.payment`
  - **الوصف:** دفعة عمولة
- **الملف:** `models\commission_rate.py`
  - **النماذج الجديدة (`_name`):** `commission.rate`
  - **الوصف:** نسبة العمولة حسب تاج العميل
- **الملف:** `models\res_company.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\commission_analysis_action.xml`, `report\commission_analysis_template.xml`, `report\commission_report_action.xml`, `report\commission_report_template.xml`, `security\record_rules.xml`, `views\commission_line_views.xml`, `views\commission_rate_views.xml`, `views\res_config_settings_views.xml`, `wizard\commission_analysis_wizard_views.xml`, `wizard\commission_payment_wizard_views.xml`
- **ملفات التقارير (`Reports`):** `report\commission_analysis_action.xml`, `report\commission_report_action.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sales Commission by Customer Tag` أو `commission_sales` والضغط على **تثبيت (Install)**.
