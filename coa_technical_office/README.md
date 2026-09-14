# Alramlaa Technical Office (`alramlaa_technical_office`)

## 📌 الوصف العام (Overview)
Technical Office review workflow between Sale Orders and Manufacturing

### التفاصيل الوظيفية:

        Adds a Technical Office approval layer between Sale Orders and Manufacturing.

        Features
        --------
        * "Request Technical Review" button on Sale Order
        * One technical.review record per SO with per-product review lines
        * BOM auto-detection per product; create estimated BOM if none exists
        * Approve / Reject workflow with mandatory rejection reason
        * Blocks SO confirmation until the review is approved
        * Integrates with alramlaa_product_dimensions (dimension fields on products & BOM)
        * Full mail.thread + mail.activity.mixin on the review record
        * Sequence-generated reference (TR/YYYY/MM/0001)
        * Security groups: Technical Office User / Manager
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `alramlaa_technical_office`
- **التصنيف (Category):** `Manufacturing`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_management`, `mrp`, `mail`, `alramlaa_product_dimensions`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\mrp_bom.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.bom`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`
- **الملف:** `models\technical_review.py`
  - **النماذج الجديدة (`_name`):** `technical.review`, `name`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Technical Review
- **الملف:** `models\technical_review_line.py`
  - **النماذج الجديدة (`_name`):** `technical.review.line`
  - **الوصف:** Technical Review Line

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\ir_sequence.xml`, `security\security.xml`, `views\sale_order_views.xml`, `views\technical_review_views.xml`, `wizard\reject_wizard_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Alramlaa Technical Office` أو `alramlaa_technical_office` والضغط على **تثبيت (Install)**.
