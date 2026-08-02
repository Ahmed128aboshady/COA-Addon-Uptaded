# BOM Formula Calculator (`mfg_bom_formula`)

## 📌 الوصف العام (Overview)
إضافة حاسبة معادلات ديناميكية على BOM

### التفاصيل الوظيفية:

        يضيف تاب "حاسبة التصنيع" على BOM يمكّنك من:
        - تعريف متغيرات (طول، عرض، سماكة، عدد، ثوابت)
        - كتابة معادلات Python يدوياً لكل component
        - حساب الكميات تلقائياً وتحديث BOM Lines
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `mfg_bom_formula`
- **التصنيف (Category):** `Manufacturing`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\bom_formula.py`
  - **النماذج الجديدة (`_name`):** `mrp.bom.formula.variable`, `mrp.bom.formula.line`
  - **النماذج المعدلة (`_inherit`):** `mrp.bom`
  - **الوصف:** BOM Formula Variable

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\bom_formula_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `BOM Formula Calculator` أو `mfg_bom_formula` والضغط على **تثبيت (Install)**.
