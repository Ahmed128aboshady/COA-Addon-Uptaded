# Sale Operation Stages (`sale_operation_stages`)

## 📌 الوصف العام (Overview)
مراحل عمليات على المنتج قبل التسليم - مخزن عمليات - داشبورد تتبع

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_operation_stages`
- **التصنيف (Category):** `Sales/Inventory`
- **الإصدار (Version):** `18.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_stock`, `stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\operation_stage.py`
  - **النماذج الجديدة (`_name`):** `sale.operation.stage`
  - **الوصف:** مراحل العمليات
- **الملف:** `models\sale_operation.py`
  - **النماذج الجديدة (`_name`):** `sale.operation`, `sale.operation.stage.log`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** عملية على منتج
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`, `sale.order.line`, `stock.move`, `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\stage_data.xml`, `data\warehouse_data.xml`, `security\security.xml`, `views\dashboard_views.xml`, `views\operation_stage_views.xml`, `views\sale_operation_views.xml`, `views\sale_order_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Operation Stages` أو `sale_operation_stages` والضغط على **تثبيت (Install)**.
