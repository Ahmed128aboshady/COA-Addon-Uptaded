# MFG Component Correction (`mfg_component_correction`)

## 📌 الوصف العام (Overview)
تصحيح كميات المكونات بعد إتمام أوامر التصنيع

### التفاصيل الوظيفية:

        يتيح هذا الموديول إمكانية تصحيح كميات المكونات المستهلكة
        بعد إغلاق أمر التصنيع، مع إرجاع الفارق للمخزن وتصحيح التكلفة تلقائياً.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `mfg_component_correction`
- **التصنيف (Category):** `Manufacturing`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `mrp`, `stock`, `stock_account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\mrp_production.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.production`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\mrp_production_view.xml`, `wizard\mrp_component_correction_wizard_view.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `MFG Component Correction` أو `mfg_component_correction` والضغط على **تثبيت (Install)**.
