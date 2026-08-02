# Post Dated Cheque Management - Community Edition (`sh_pdc`)

## 📌 الوصف العام (Overview)
Post Dated Cheque Management, Manage Post Dated Cheque App, View Vendor Invoice PDC , List Of Customer PDC Payment, Track Client PDC Process, Register Vendor Post Dated Cheque Module, Print VendorPDC Report, Print Client PDC Report Odoo.

### التفاصيل الوظيفية:
In Invoice/Bill, a post-dated cheque is a cheque written by the customer/vendor (payer) for a date in the future. Whether a post-dated cheque may be cashed or deposited before the date written on it depends on the country. Currently, odoo does not provide any kind of feature to manage post-dated cheque. That why we make this module, it will help to manage a post-dated cheque with an accounting journal entries. This module provides a feature to Register PDC Cheque in an account. This module allows to manage postdated cheque for the customer as well vendors, you can easily track/move to a different state of cheque like new, registered, return, deposit, bounce, done. We have taken care of all states with accounting journal entries, You can easily list filter cheque with different states. We have also made simple pdf reports. Post Dated Cheque Management Odoo
 Manage Vendor Post Dated Cheque Module, Manage Client Post Dated Cheque View Client PDC In Invoice, Get Vendor PDC In Bill, See List Of PDC Bill Of Vendor, Track PDC Process Of Customer, Register Post Dated Cheque, Print Vendor PDC Report Odoo.
 Manage Post Dated Cheque App, View Vendor Invoice PDC , List Of Customer PDC Payment, Track Client PDC Process, Register Vendor Post Dated Cheque Module, Print VendorPDC Report, Print Client PDC Report Odoo.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sh_pdc`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `19.0.8.0.2`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\account_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `account.move.line`
- **الملف:** `models\res_company.py`
  - **النماذج المعدلة (`_inherit`):** `res.company`
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\account_data.xml`, `data\ir_cron_cust.xml`, `data\ir_cron_ven.xml`, `data\ir_sequence.xml`, `data\mail_templates.xml`, `report\pdc_wizard_template.xml`, `security\pdc_security.xml`, `views\account_move_views.xml`, `views\res_config_settings_views.xml`, `wizard\pdc_multi_action_views.xml`, `wizard\pdc_payment_wizard_views.xml`
- **ملفات التقارير (`Reports`):** `report\pdc_wizard_template.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Post Dated Cheque Management - Community Edition` أو `sh_pdc` والضغط على **تثبيت (Install)**.
