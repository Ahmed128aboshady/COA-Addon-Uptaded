# Auto Sequence Generator (`auto_sequence_generator`)

## 📌 الوصف العام (Overview)
Auto-generate unique codes for products, customers, and vendors on record creation

### التفاصيل الوظيفية:

Auto Sequence Generator
========================
Automatically assigns unique reference codes when clicking the New button for:
- Products  → Internal Reference (PROD-0000001, PROD-0000002, ...)
- Customers → Customer Code    (CUST-0000001, CUST-0000002, ...)
- Vendors   → Vendor Code      (VEND-0000001, VEND-0000002, ...)

The generated code is displayed immediately and is read-only to prevent manual edits.
Sequences are fully configurable via Settings > Technical > Sequences.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `auto_sequence_generator`
- **التصنيف (Category):** `Technical`
- **الإصدار (Version):** `19.0.1.2.2`
- **الاعتماديات (Dependencies):** `product`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\product_template.py`
  - **النماذج المعدلة (`_inherit`):** `product.template`, `product.product`
- **الملف:** `models\res_partner.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\sequence_data.xml`, `views\product_template_views.xml`, `views\res_partner_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Auto Sequence Generator` أو `auto_sequence_generator` والضغط على **تثبيت (Install)**.
