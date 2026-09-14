# Sale Partner Balance (`sale_partner_balance`)

## 📌 الوصف العام (Overview)
Display partner previous and current balance on Sale Order and Invoice reports

### التفاصيل الوظيفية:

        This module adds a balance section to Sale Order and Invoice reports showing:
        - Previous Balance (الرصيد السابق)
        - Current Document Amount (الفاتورة الحالية)
        - Current Balance (الرصيد الحالي)
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_partner_balance`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `19.0.2.0.0`
- **الاعتماديات (Dependencies):** `sale`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\invoice_report_templates.xml`, `report\sale_report_templates.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Partner Balance` أو `sale_partner_balance` والضغط على **تثبيت (Install)**.
