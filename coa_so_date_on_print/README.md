# COA Sale Order Date on Print (`coa_so_date_on_print`)

## 📌 الوصف العام (Overview)
Set the Sale Order date to the print date on first print

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_so_date_on_print`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\ir_actions_report.py`
  - **النماذج المعدلة (`_inherit`):** `ir.actions.report`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Sale Order Date on Print` أو `coa_so_date_on_print` والضغط على **تثبيت (Install)**.
