# COA Sale Reservation Operation (`coa_sale_reservation`)

## 📌 الوصف العام (Overview)
Reservation checkbox on Sales Orders routed to a dedicated "Reservation" operation type (no routes needed)

### التفاصيل الوظيفية:

Sale Reservation Operation
==========================
Adds an "is Reservation" checkbox on the Sales Order. When checked, the
delivery generated on confirmation is created under a dedicated outgoing
operation type "حجز / Reservation" (own sequence RES/xxxxx, own card on
the Inventory Overview) instead of the standard Delivery type.

* No routes, no internal transfers — same flow as a normal delivery.
* The reservation picking type is created automatically per warehouse
  the first time it is needed.
* Stock is force-reserved on order confirmation, so reserved goods
  cannot be taken by other orders.
* Delivered quantities, invoicing and returns behave exactly like a
  standard delivery.
* Ready-made filters on Sales Orders and Transfers to isolate
  reservations.

Built for Odoo 18 (Community & Enterprise).
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `coa_sale_reservation`
- **التصنيف (Category):** `Inventory/Inventory`
- **الإصدار (Version):** `18.0.1.0.1`
- **الاعتماديات (Dependencies):** `sale_stock`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`
- **الملف:** `models\stock_rule.py`
  - **النماذج المعدلة (`_inherit`):** `stock.rule`, `stock.picking`
- **الملف:** `models\stock_warehouse.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking.type`, `stock.warehouse`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\sale_order_report.xml`, `views\report_saleorder_reservation.xml`, `views\sale_order_views.xml`, `views\stock_picking_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `COA Sale Reservation Operation` أو `coa_sale_reservation` والضغط على **تثبيت (Install)**.
