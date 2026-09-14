# Petty Cash Management (`petty_cash`)

## 📌 الوصف العام (Overview)
Manage petty cash custodies and expenses with full accounting integration

### التفاصيل الوظيفية:

        Petty Cash Management System:
        - Each employee registers their own expenses
        - Accountants see all employee custodies and remaining balances
        - Each employee sees only their own expenses
        - Full accounting integration with automatic journal entries
        - Each category has a dedicated expense account
        - Custody account configured from Settings
        - Multi-level approval workflow
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `petty_cash`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `19.0.3.0.0`
- **الاعتماديات (Dependencies):** `base`, `mail`, `hr`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\petty_cash_approver.py`
  - **النماذج الجديدة (`_name`):** `petty.cash.approver`
  - **الوصف:** Petty Cash Approver
- **الملف:** `models\petty_cash_category.py`
  - **النماذج الجديدة (`_name`):** `petty.cash.category`
  - **الوصف:** Petty Cash Expense Category
- **الملف:** `models\petty_cash_config.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`
- **الملف:** `models\petty_cash_custody.py`
  - **النماذج الجديدة (`_name`):** `petty.cash.custody`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Petty Cash Custody
- **الملف:** `models\petty_cash_expense.py`
  - **النماذج الجديدة (`_name`):** `petty.cash.expense`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Petty Cash Expense

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\petty_cash_security.xml`, `views\petty_cash_approver_views.xml`, `views\petty_cash_category_views.xml`, `views\petty_cash_config_views.xml`, `views\petty_cash_custody_views.xml`, `views\petty_cash_expense_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Petty Cash Management` أو `petty_cash` والضغط على **تثبيت (Install)**.
