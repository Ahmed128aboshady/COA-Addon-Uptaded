# Manufacturing Machines & Maintenance (`manufacturing_machines`)

## 📌 الوصف العام (Overview)
إدارة الآلات والصيانة وتتبع التكاليف في التصنيع

### التفاصيل الوظيفية:

        نظام متكامل لإدارة:
        - الآلات ومراكز الإنتاج
        - الصيانة الوقائية والتصحيحية
        - تتبع تكاليف العمال والمواد
        - التكاليف الإضافية (Overhead)
        - الربط بالحسابات تلقائياً
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `manufacturing_machines`
- **التصنيف (Category):** `Manufacturing`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`, `mail`, `account`, `stock`, `mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\cost_line.py`
- **الملف:** `models\machine.py`
  - **النماذج الجديدة (`_name`):** `mfg.machine`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Machine
- **الملف:** `models\maintenance.py`
  - **النماذج الجديدة (`_name`):** `mfg.maintenance`, `mfg.maintenance.part`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Maintenance Record
- **الملف:** `models\manufacturing_machine.py`
  - **النماذج الجديدة (`_name`):** `manufacturing.machine`, `mrp.production.machine.line`, `mrp.production.labor.line`, `mrp.production.overhead.line`
  - **الوصف:** Manufacturing Machine
- **الملف:** `models\mrp_production.py`
  - **النماذج الجديدة (`_name`):** `mfg.mrp.labor.line`, `mfg.mrp.overhead.line`, `mfg.production.machine.line`
  - **النماذج المعدلة (`_inherit`):** `mrp.production`
  - **الوصف:** Labor Line in MRP Production
- **الملف:** `models\production_order.py`
  - **النماذج الجديدة (`_name`):** `mfg.production.order`, `mfg.labor.line`, `mfg.overhead.line`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Production Order
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\sequence.xml`, `report\production_cost_report.xml`, `security\security.xml`, `views\cost_views.xml`, `views\machine_views.xml`, `views\maintenance_views.xml`, `views\manufacturing_machine_views.xml`, `views\mrp_production_views.xml`, `views\production_order_views.xml`
- **ملفات التقارير (`Reports`):** `report\production_cost_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Manufacturing Machines & Maintenance` أو `manufacturing_machines` والضغط على **تثبيت (Install)**.
