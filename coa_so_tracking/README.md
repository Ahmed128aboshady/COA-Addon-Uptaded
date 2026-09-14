# COA Sales Order Tracking Report (`coa_so_tracking`)

## 📌 الوصف العام (Overview)
متابعة أوامر البيع: كميات التصنيع والتسليم والفوترة لكل صنف

### التفاصيل الوظيفية:

COA Sales Order Tracking Report
===============================
لوحة تحكم تفاعلية لمتابعة أوامر البيع من البداية للنهاية:
- قائمة أوامر البيع قابلة للتوسيع (drop-list)
- لكل أمر بيع: تفاصيل كل صنف بالكمية (مطلوب / تم / متبقي)
- التصنيع: كمية تم تصنيعها + نسبة + المتبقي
- التسليم: كمية تم تسليمها + نسبة + المتبقي
- الفوترة: كمية تم فوترتها + نسبة + المتبقي
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_so_tracking`
- **التصنيف (Category):** `Sales/Sales`
- **الإصدار (Version):** `19.0.1.1.0`
- **الاعتماديات (Dependencies):** `sale`, `mrp`, `sale_mrp`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`, `mrp.production`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `static\src\xml\so_dashboard.xml`, `views\so_tracking_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Sales Order Tracking Report` أو `coa_so_tracking` والضغط على **تثبيت (Install)**.
