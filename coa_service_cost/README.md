# COA Service Product Cost Flow (`coa_service_cost`)

## 📌 الوصف العام (Overview)
For service products: redirects purchase bills to an Intermediate Account (instead of expensing immediately), then on customer invoice automatically creates a COGS ← Intermediate cost journal entry.

### التفاصيل الوظيفية:

COA Service Product Cost Flow
==============================

Business problem:
-----------------
Standard Odoo expenses service-product costs immediately on purchase
(DR Expense / CR AP).  For project-based or resale services the cost
should only be recognised when the service is invoiced to the customer.

Solution:
---------
Configure two accounts on each service product (Accounting tab):

  • Intermediate Account  – cost-in-transit buffer
  • Cost of Sales Account – P&L account for the matched cost

Flow:
  1. Vendor bill posted  →  DR Intermediate / CR AP
  2. Customer invoice posted → automatic journal entry:
                                 DR Cost of Sales / CR Intermediate

Credit-note reversals are handled symmetrically.

Developed by Community of Accountants (COA)
WhatsApp: +20 101 390 7174
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_service_cost`
- **التصنيف (Category):** `Accounting`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `account`, `product`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\product_template.py`
  - **النماذج الجديدة (`_name`):** `account.account`, `account.account`
  - **النماذج المعدلة (`_inherit`):** `product.template`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\product_template_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Service Product Cost Flow` أو `coa_service_cost` والضغط على **تثبيت (Install)**.
