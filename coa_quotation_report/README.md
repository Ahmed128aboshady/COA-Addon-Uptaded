# Al Ramlaa Quotation Report (`alramlaa_quotation_report`)

## 📌 الوصف العام (Overview)
Custom Quotation/Sales Order PDF Report - Al Ramlaa Wooden Products Style

### التفاصيل الوظيفية:

        Custom QWeb PDF report for Quotations and Sales Orders.
        Includes:
        - Company header with logo
        - Quotation summary page
        - Detailed item pages with images, descriptions, materials, dimensions, qty & prices
        - Joinery section
        - Furniture section
        - Payment terms & delivery terms
        - Arabic + English bilingual support
        - Footer with company info
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_quotation_report`
- **التصنيف (Category):** `Sales`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order_line.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order.line`, `sale.order`
- **الملف:** `models\summary_line.py`
  - **النماذج الجديدة (`_name`):** `alramlaa.summary.line`
  - **الوصف:** Al Ramlaa Quotation Summary Line

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\quotation_report.xml`, `report\quotation_report_template.xml`, `views\product_views.xml`, `views\sale_order_views.xml`
- **ملفات التقارير (`Reports`):** `report\quotation_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Al Ramlaa Quotation Report` أو `alramlaa_quotation_report` والضغط على **تثبيت (Install)**.
