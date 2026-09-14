# Sales Retention Money (`sale_retention`)

## 📌 الوصف العام (Overview)
Customer retention/holdback on sales: configurable percentage and holding period per order, automatic split of the receivable to a dedicated retention account with maturity based on the delivery date. Aging and partner ledger stay fully correct.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_retention`
- **التصنيف (Category):** `Accounting/Accounting`
- **الإصدار (Version):** `19.0.2.0.1`
- **الاعتماديات (Dependencies):** `sale_stock`, `account`

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
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\retention_report.xml`, `views\account_move_views.xml`, `views\res_config_settings_views.xml`, `views\retention_menu.xml`, `views\sale_order_views.xml`
- **ملفات التقارير (`Reports`):** `report\retention_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sales Retention Money` أو `sale_retention` والضغط على **تثبيت (Install)**.
