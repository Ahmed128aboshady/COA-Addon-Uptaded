# COA Partner Exact Reference Search (`coa_partner_ref_exact_search`)

## 📌 الوصف العام (Overview)
Exact-match search on partner Reference (ref) in search bar and dropdowns

### التفاصيل الوظيفية:

COA Partner Exact Reference Search
==================================
Searching a partner by Reference (e.g. 538) with the default behaviour
also matches partners whose reference merely contains the digits
(e.g. 1538). This module adds:

* A "Reference (Exact)" search option in the partner search view
  that matches the reference exactly.
* An override of partner name_search so that typing a pure number in
  any partner dropdown (Sales Orders, Invoices, Payments, ...) first
  tries an exact match on the Reference field, falling back to the
  standard behaviour when no exact match exists.


---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_partner_ref_exact_search`
- **التصنيف (Category):** `Contacts`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `base`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\res_partner.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\res_partner_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Partner Exact Reference Search` أو `coa_partner_ref_exact_search` والضغط على **تثبيت (Install)**.
