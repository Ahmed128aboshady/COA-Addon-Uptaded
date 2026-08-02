# Account Restricted Access - COA (`account_restricted_access`)

## 📌 الوصف العام (Overview)
تقييد رؤية المحاسب على حسابات معينة في الجينرال ليدجر وحركة الحسابات

### التفاصيل الوظيفية:

Account Restricted Access
==========================
يسمح هذا الموديول بتحديد قائمة حسابات (Many2many) لكل مستخدم من خلال بطاقة
المستخدم (Users). المستخدم المنتمي لمجموعة "محاسب مقيّد الصلاحية" لن يرى
ولن يستطيع الوصول إلا إلى:

- حركة القيود (Journal Items / account.move.line) الخاصة بالحسابات المسموح بها فقط
- دفتر الأستاذ العام (General Ledger) محدود بهذه الحسابات
- شجرة الحسابات (Chart of Accounts) محدودة بهذه الحسابات فقط

تم تطويره بواسطة Community of Accountants - COA
Odoo Silver Partner
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `account_restricted_access`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_account.py`
  - **النماذج المعدلة (`_inherit`):** `account.account`
- **الملف:** `models\account_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `account.move.line`
- **الملف:** `models\res_users.py`
  - **النماذج الجديدة (`_name`):** `account.account`
  - **النماذج المعدلة (`_inherit`):** `res.users`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `security\account_restricted_security.xml`, `views\res_users_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Account Restricted Access - COA` أو `account_restricted_access` والضغط على **تثبيت (Install)**.
