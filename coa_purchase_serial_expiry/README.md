# Purchase & Manufacturing Serial + Lot Expiry (FIFO) (`purchase_serial_expiry`)

## 📌 الوصف العام (Overview)
Auto serial on PO/MO, expiry entry on receipts, FIFO auto-lot on delivery & MO

### التفاصيل الوظيفية:

    Features
    ========
    1. Checkbox on product: "Requires Expiry Date on Purchase"
       - Blocks receipt validation if expiry date is missing
       - Auto-enables Lot tracking + FIFO removal strategy

    2. Expiry Date entry on Receipt (Detailed Operations):
       - Storekeeper fills Lot # + Expiry Date per line
       - Multiple lines = multiple lots with different expiry dates
       - Lots created automatically in stock on validation

    3. FIFO auto-assignment on delivery (Sales) and Manufacturing:
       - Detailed Operations auto-sorted: earliest expiry lot first
       - MO raw material lines auto-filled with FIFO lots on produce

    4. Auto serial number on Purchase Orders and Manufacturing Orders

    5. Daily cron: email + chatter + activity 30 days before lot expiry

    6. Lot Expiry Report (List / Graph / Pivot / PDF)
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `purchase_serial_expiry`
- **التصنيف (Category):** `Inventory/Purchase`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `purchase`, `mrp`, `stock`, `sale_stock`, `mail`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\expiry_report.py`
- **الملف:** `models\mrp_production.py`
  - **النماذج المعدلة (`_inherit`):** `mrp.production`
- **الملف:** `models\product_template.py`
  - **النماذج المعدلة (`_inherit`):** `product.template`, `product.product`
- **الملف:** `models\purchase_order.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order`
- **الملف:** `models\purchase_order_line_lot.py`
  - **النماذج الجديدة (`_name`):** `purchase.order.line.lot`
  - **الوصف:** Purchase Order Line – Lot & Expiry (legacy link)
- **الملف:** `models\stock_lot.py`
  - **النماذج المعدلة (`_inherit`):** `stock.lot`
- **الملف:** `models\stock_move_line.py`
  - **النماذج المعدلة (`_inherit`):** `stock.move.line`
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`
- **الملف:** `models\stock_quant.py`
  - **النماذج المعدلة (`_inherit`):** `stock.quant`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\ir_cron_data.xml`, `data\ir_sequence_data.xml`, `data\mail_template_data.xml`, `report\expiry_report_action.xml`, `report\expiry_report_template.xml`, `views\expiry_report_views.xml`, `views\mrp_production_views.xml`, `views\product_template_views.xml`, `views\purchase_order_views.xml`, `views\stock_lot_views.xml`, `views\stock_picking_views.xml`, `views\stock_quant_views.xml`
- **ملفات التقارير (`Reports`):** `report\expiry_report_action.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Purchase & Manufacturing Serial + Lot Expiry (FIFO)` أو `purchase_serial_expiry` والضغط على **تثبيت (Install)**.
