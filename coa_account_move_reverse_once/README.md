# Reverse Journal Entry Only Once (`account_move_reverse_once`)

## 📌 الوصف العام (Overview)
Block reversing a journal entry more than once and block reversing a reversal entry.

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `account_move_reverse_once`
- **التصنيف (Category):** `Accounting/Accounting`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\account_move_reversal.py`
  - **النماذج المعدلة (`_inherit`):** `account.move.reversal`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
لا توجد ملفات واجهات XML مستقلة.

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Reverse Journal Entry Only Once` أو `account_move_reverse_once` والضغط على **تثبيت (Install)**.
