# COA Accounting Internal Transfer (`coa_internal_transfer`)

## 📌 الوصف العام (Overview)
Restore the classic Internal Transfer feature on Payments (Odoo 19)

### التفاصيل الوظيفية:

COA Accounting Internal Transfer
=================================
Restores the classic "Internal Transfer" workflow that existed on
account.payment before it was removed from Odoo core (Odoo 18/19).

Features
--------
* Adds back "Internal Transfer" as a payment type, selectable from a new
  Payment Type radio (Send / Receive / Internal Transfer).
* Adds a "Destination Journal" field, shown only for internal transfers.
* On confirmation, automatically creates a paired payment in the
  destination journal and links both records.
* Fully configurable Outstanding Accounts behaviour:
    - If the source and destination journals use their own default
      account as both Outstanding Receipts/Payments account, the
      transfer is created directly reconciled (status = Paid).
    - If dedicated Outstanding Accounts are configured on the journals,
      the transfer is posted through those accounts and stays
      "In Process" until reconciled with the bank statement.
* A dedicated filter to list/find all internal transfers.

Developed by Community of Accountants (COA) - Odoo Silver Partner.


---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_internal_transfer`
- **التصنيف (Category):** `Accounting/Accounting`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_payment.py`
  - **النماذج الجديدة (`_name`):** `account.journal`
  - **النماذج المعدلة (`_inherit`):** `account.payment`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\account_payment_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Accounting Internal Transfer` أو `coa_internal_transfer` والضغط على **تثبيت (Install)**.
