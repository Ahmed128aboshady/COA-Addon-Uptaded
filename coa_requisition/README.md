# arabian_requisition (`arabian_requisition`)

## 📌 الوصف العام (Overview)
Short (1 phrase/line) summary of the module's purpose

### التفاصيل الوظيفية:

Long description of module's purpose
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arabian_requisition`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `0.1`
- **الاعتماديات (Dependencies):** `base`, `hr`, `uom`, `stock`, `purchase`, `purchase_requisition`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\construction_requisition.py`
  - **النماذج الجديدة (`_name`):** `construction.requisition`, `construction.requisition.line`
  - **الوصف:** Construction Requisition
- **الملف:** `models\models.py`
  - **النماذج الجديدة (`_name`):** `arabian_requisition.arabian_requisition`
  - **الوصف:** arabian_requisition.arabian_requisition
- **الملف:** `models\purchase_agreements.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.requisition`
- **الملف:** `models\purchase_order.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order`
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`
- **الملف:** `models\stock_quant.py`
  - **النماذج المعدلة (`_inherit`):** `stock.quant`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `demo\demo.xml`, `security\construction_requisition_groups.xml`, `views\construction_requisition.xml`, `views\purchase_agreements.xml`, `views\purchase_order.xml`, `views\stock_picking.xml`, `views\templates.xml`, `views\views.xml`, `wizard\transfer_requisition_order.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `arabian_requisition` أو `arabian_requisition` والضغط على **تثبيت (Install)**.
