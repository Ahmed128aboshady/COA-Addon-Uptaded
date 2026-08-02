# Manufacturing Location Routes (مسارات المخزون بالكاتجوري) (`mfg_location_routes`)

## 📌 الوصف العام (Overview)
ربط لوكيشن السحب والتخزين بالكاتجوري تلقائياً في التصنيع والبيع والمرتجعات

### التفاصيل الوظيفية:

        المشاكل اللي بيحلها المديول ده:
        ====================================
        1. ربط source location بالكاتجوري لكل عملية (تصنيع / بيع / مرتجع)
        2. حل مشكلة "No rule has been found to replenish" للأصناف في sub-locations
        3. إنشاء Stock Rules تلقائياً لكل كاتجوري عند الحفظ
        4. دعم BUY + MTO مع لوكيشن مخصص
        5. حقل لوكيشن على component في BOM يورث من الكاتجوري
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `mfg_location_routes`
- **التصنيف (Category):** `Manufacturing`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`, `mrp`, `purchase`, `sale_stock`, `mrp_subcontracting`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\mrp_bom_line.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.bom.line`, `mrp.bom`, `mrp.production`
- **الملف:** `models\product_category_location.py`
  - **النماذج المعدلة (`_inherit`):** `product.category`
- **الملف:** `models\stock_rule_auto.py`
  - **النماذج المعدلة (`_inherit`):** `stock.rule`, `stock.route`, `stock.picking`, `stock.move`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\mrp_bom_views.xml`, `views\product_category_views.xml`, `views\stock_rule_views.xml`, `wizard\wizard_fix_routes_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Manufacturing Location Routes (مسارات المخزون بالكاتجوري)` أو `mfg_location_routes` والضغط على **تثبيت (Install)**.
