# arabian_expense_payment (`arabian_expense_payment`)

## 📌 الوصف العام (Overview)

        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com

### التفاصيل الوظيفية:

        Long description of module's purpose
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arabian_expense_payment`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `0.1`
- **الاعتماديات (Dependencies):** `base`, `accountant`, `hr`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_journal.py`
  - **النماذج المعدلة (`_inherit`):** `account.journal`
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`, `account.move.line`
- **الملف:** `models\expense_payment.py`
  - **النماذج الجديدة (`_name`):** `expense.payment`, `expense.payment.line`
  - **النماذج المعدلة (`_inherit`):** `portal.mixin, mail.thread, mail.activity.mixin`
  - **الوصف:** Expense Payment
- **الملف:** `models\models.py`
  - **النماذج الجديدة (`_name`):** `arabian_expense_payment.arabian_expense_payment`
  - **الوصف:** arabian_expense_payment.arabian_expense_payment

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `demo\demo.xml`, `report\expense_payment_template.xml`, `views\account_journal.xml`, `views\account_move.xml`, `views\expense_payment.xml`, `views\templates.xml`, `views\views.xml`
- **ملفات التقارير (`Reports`):** `report\expense_payment.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `arabian_expense_payment` أو `arabian_expense_payment` والضغط على **تثبيت (Install)**.
