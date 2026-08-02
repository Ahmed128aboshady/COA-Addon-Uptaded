# Journal Payment Commission (`account_journal_commission`)

## 📌 الوصف العام (Overview)
خصم عمولة تلقائي على الـ Journal - مبيعات ومشتريات منفصلين

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `account_journal_commission`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_journal.py`
  - **النماذج المعدلة (`_inherit`):** `account.journal`
- **الملف:** `models\account_payment.py`
  - **النماذج المعدلة (`_inherit`):** `account.payment`
- **الملف:** `models\account_payment_register.py`
  - **النماذج المعدلة (`_inherit`):** `account.payment.register`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\account_journal_views.xml`, `views\account_payment_register_views.xml`, `views\account_payment_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Journal Payment Commission` أو `account_journal_commission` والضغط على **تثبيت (Install)**.
