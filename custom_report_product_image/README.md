# Custom Reports — Product Image & Reference Code (`custom_report_product_image`)

## 📌 الوصف العام (Overview)
Adds product image to Delivery prints and splits product name / reference code into separate columns across all module reports

### التفاصيل الوظيفية:

        Customises printed reports for:
        - Inventory / Delivery Orders  : adds product image column + separate Reference column
        - Sales Orders / Quotations    : adds separate Reference column
        - Purchase Orders              : adds separate Reference column
        - Invoices & Bills             : adds separate Reference column

        The "Reference" column shows the product's Internal Reference (default_code).
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `custom_report_product_image`
- **التصنيف (Category):** `Technical`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`, `sale_management`, `purchase`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
لا توجد نماذج بايثون مخصصة أو معقدة.

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\report_delivery_custom.xml`, `report\report_invoice_custom.xml`, `report\report_purchase_custom.xml`, `report\report_sale_custom.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Custom Reports — Product Image & Reference Code` أو `custom_report_product_image` والضغط على **تثبيت (Install)**.
