# Vendor Duplicate Check (Email / Phone) (`coa_vendor_duplicate_check`)

## 📌 الوصف العام (Overview)
Warn or block when a vendor's email or phone is already used by another contact.

### التفاصيل الوظيفية:

Vendor Duplicate Check
======================

Odoo natively alerts on duplicate Tax ID / Company Registry when a vendor is
created (including by duplicating an existing vendor), but it does NOT check for
a duplicate Email or Phone number.

This module adds that check on ``res.partner``:

* On save it can **block** the record (ValidationError) or only **warn**.
* A live **on-change warning** flags duplicates while typing / after duplicating.
* Configurable from *Settings > Duplicate Check*:
    - Handling mode: Block save / Warn only
    - Scope: Vendors only / All contacts
    - Which fields to check: Email, Phone

Note (Odoo 19): the separate ``mobile`` field was removed from contacts and
merged into ``phone``, so the mobile number is validated through ``phone``.


---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_vendor_duplicate_check`
- **التصنيف (Category):** `Contacts`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `base_setup`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`
- **الملف:** `models\res_partner.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\ir_config_parameter.xml`, `views\res_config_settings_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Vendor Duplicate Check (Email / Phone)` أو `coa_vendor_duplicate_check` والضغط على **تثبيت (Install)**.
