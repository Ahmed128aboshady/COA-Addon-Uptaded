# arabian_so_invoice_report (`arabian_so_invoice_report`)

## 📌 الوصف العام (Overview)
Short (1 phrase/line) summary of the module's purpose

### التفاصيل الوظيفية:

Long description of module's purpose
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arabian_so_invoice_report`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `0.1`
- **الاعتماديات (Dependencies):** `sale`, `account`, `l10n_gcc_invoice`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\models.py`
  - **النماذج الجديدة (`_name`):** `arabian_so_invoice_report.arabian_so_invoice_report`
  - **الوصف:** arabian_so_invoice_report.arabian_so_invoice_report
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `demo\demo.xml`, `report\invoice_template.xml`, `report\sale_order_template.xml`, `views\templates.xml`, `views\views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `arabian_so_invoice_report` أو `arabian_so_invoice_report` والضغط على **تثبيت (Install)**.
