# COA Partial Quantity Relocate (`coa_partial_relocate`)

## 📌 الوصف العام (Overview)
Relocate a specific quantity (not the full quant) when using the Relocate action on stock locations / quants.

### التفاصيل الوظيفية:

COA Partial Quantity Relocate
=============================
The standard Odoo "Relocate" wizard (Inventory > Locations / Physical
Inventory) always moves the FULL on-hand quantity of each selected quant.

This module adds an editable line per selected quant inside the Relocate
wizard, so the user can specify exactly how much quantity to move to the
destination location. Lines left at 0 are skipped, lines at full quantity
follow the 100% native flow, and partial lines are moved using the same
native inventory-move mechanism (stock.move with is_inventory=True),
keeping lot / package / owner information intact.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_partial_relocate`
- **التصنيف (Category):** `Inventory/Inventory`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
لا توجد نماذج بايثون مخصصة أو معقدة.

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `wizard\stock_quant_relocate_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Partial Quantity Relocate` أو `coa_partial_relocate` والضغط على **تثبيت (Install)**.
