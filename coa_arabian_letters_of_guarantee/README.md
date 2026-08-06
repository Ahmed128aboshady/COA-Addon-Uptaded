# arabian_letters_of_guarantee (`arabian_letters_of_guarantee`)

## 📌 الوصف العام (Overview)
Short (1 phrase/line) summary of the module's purpose

### التفاصيل الوظيفية:

Long description of module's purpose
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arabian_letters_of_guarantee`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `0.1`
- **الاعتماديات (Dependencies):** `base`, `account`, `account_asset`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`, `account.move.line`
- **الملف:** `models\advance_payment_guarantee.py`
  - **النماذج الجديدة (`_name`):** `lg.advance.payment.guarantee`
  - **الوصف:** Lg Advance Payment Guarantee
- **الملف:** `models\bid_bond.py`
  - **النماذج الجديدة (`_name`):** `lg.bid.bond`
  - **الوصف:** Lg Bid Bond
- **الملف:** `models\maintenance_bond.py`
  - **النماذج الجديدة (`_name`):** `lg.maintenance.bond`
  - **الوصف:** Lg Maintenance Bond
- **الملف:** `models\models.py`
  - **النماذج الجديدة (`_name`):** `arabian_letters_of_guarantee.arabian_letters_of_guarantee`
  - **الوصف:** arabian_letters_of_guarantee.arabian_letters_of_guarantee
- **الملف:** `models\performance_bond.py`
  - **النماذج الجديدة (`_name`):** `lg.performance.bond`
  - **الوصف:** Lg Performance Bond
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`, `res.company`, `account.asset`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `demo\demo.xml`, `views\account_move.xml`, `views\advance_payment_guarantee.xml`, `views\bid_bond.xml`, `views\maintenance_bond.xml`, `views\performance_bond.xml`, `views\res_config_settings.xml`, `views\templates.xml`, `views\views.xml`, `wizard\check_lg_accounts.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `arabian_letters_of_guarantee` أو `arabian_letters_of_guarantee` والضغط على **تثبيت (Install)**.
