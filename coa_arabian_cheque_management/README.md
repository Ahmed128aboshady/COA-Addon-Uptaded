# arabian_cheque_management (`arabian_cheque_management`)

## 📌 الوصف العام (Overview)
Short (1 phrase/line) summary of the module's purpose

### التفاصيل الوظيفية:

Long description of module's purpose
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arabian_cheque_management`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `0.1`
- **الاعتماديات (Dependencies):** `base`, `accountant`, `account_accountant`, `utm`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`, `account.move.line`
- **الملف:** `models\incoming_cheque.py`
  - **النماذج الجديدة (`_name`):** `incoming.cheque`
  - **الوصف:** Incoming Cheque
- **الملف:** `models\models.py`
  - **النماذج الجديدة (`_name`):** `arabian_cheque_management.arabian_cheque_management`
  - **الوصف:** arabian_cheque_management.arabian_cheque_management
- **الملف:** `models\outgoing_cheque.py`
  - **النماذج الجديدة (`_name`):** `outgoing.cheque`
  - **الوصف:** Outgoing Cheque
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`, `res.company`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `demo\demo.xml`, `views\account_move.xml`, `views\incoming_cheque.xml`, `views\outgoing_cheque.xml`, `views\res_config_settings.xml`, `views\templates.xml`, `views\views.xml`, `wizard\check_accounts_cheque.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `arabian_cheque_management` أو `arabian_cheque_management` والضغط على **تثبيت (Install)**.
