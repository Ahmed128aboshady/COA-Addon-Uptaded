# COA Production Variance Report (`coa_mfg_production_variance`)

## 📌 الوصف العام (Overview)
Planned vs Produced quantity variance report for Manufacturing Orders

### التفاصيل الوظيفية:

Production Quantity Variance Report
===================================
Compares the planned quantity (To Produce) against the actually produced
quantity for each Manufacturing Order, with variance in quantity and
percentage.

Features:
---------
* SQL view based report model (fast, no stored duplication)
* List, Pivot and Graph views
* Full grouping flexibility: Product, Product Category, Responsible,
  State, Finished Date (month), Company
* Ready-made filters: Done MOs, Over-produced, Under-produced
* Drill-down to the Manufacturing Order from the report line
* Export wizard: PDF (QWeb, A4 Landscape) and Excel (xlsxwriter,
  color-coded with totals and autofilter)

Compatible with Odoo 18 and Odoo 19 (Community & Enterprise).
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_mfg_production_variance`
- **التصنيف (Category):** `Manufacturing/Reporting`
- **الإصدار (Version):** `19.0.1.2.0`
- **الاعتماديات (Dependencies):** `mrp`, `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\production_variance.py`
  - **النماذج الجديدة (`_name`):** `coa.mfg.production.variance`, `production_id`
  - **الوصف:** Production Quantity Variance (Planned vs Produced)

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\production_variance_report.xml`, `views\production_variance_views.xml`, `wizard\production_variance_wizard_views.xml`
- **ملفات التقارير (`Reports`):** `report\production_variance_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Production Variance Report` أو `coa_mfg_production_variance` والضغط على **تثبيت (Install)**.
