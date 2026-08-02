# Sale Payment Method (`sale_payment_method`)

## 📌 الوصف العام (Overview)
Add payment method tags on sales orders and invoices with reporting

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_payment_method`
- **التصنيف (Category):** `Accounting/Reporting`
- **الإصدار (Version):** `18.0.2.0.0`
- **الاعتماديات (Dependencies):** `sale`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج الجديدة (`_name`):** `sale.payment.method`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\payment_method_report.py`
  - **النماذج الجديدة (`_name`):** `payment.method.report`, `partner_id`
  - **الوصف:** Payment Method Report
- **الملف:** `models\payment_method_tag.py`
  - **النماذج الجديدة (`_name`):** `sale.payment.method`
  - **الوصف:** Payment Method
- **الملف:** `models\res_partner.py`
  - **النماذج الجديدة (`_name`):** `sale.payment.method`
  - **النماذج المعدلة (`_inherit`):** `res.partner`
- **الملف:** `models\sale_order.py`
  - **النماذج الجديدة (`_name`):** `sale.payment.method`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\payment_method_data.xml`, `views\account_move_views.xml`, `views\report_views.xml`, `views\res_partner_views.xml`, `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Payment Method` أو `sale_payment_method` والضغط على **تثبيت (Install)**.
