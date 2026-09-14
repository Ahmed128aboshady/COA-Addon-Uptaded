# Multi Approval (`multi_approval`)

## 📌 الوصف العام (Overview)
Multi-stage approval workflow for Sales, Purchase, Inventory and Accounting

### التفاصيل الوظيفية:

        Configure multi-stage approval workflows for:
        - Sale Orders (Quotations)
        - Purchase Orders
        - Vendor Bills / Customer Invoices (Accounting)
        - Inventory Transfers (Stock Pickings)

        Features:
        - Unlimited configurable approval stages
        - Per-stage approvers with flexible requirements (any/all/minimum)
        - Automatic stage advancement
        - Email & activity notifications
        - Refuse with reason
        - Auto-confirm option after full approval
        - Full audit trail via chatter
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `multi_approval`
- **التصنيف (Category):** `Approvals`
- **الإصدار (Version):** `19.0.1.2.0`
- **الاعتماديات (Dependencies):** `sale_management`, `purchase`, `account`, `stock`, `mail`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج الجديدة (`_name`):** `account.move`
  - **النماذج المعدلة (`_inherit`):** `account.move, multi.approval.mixin`
- **الملف:** `models\account_payment.py`
  - **النماذج الجديدة (`_name`):** `account.payment`
  - **النماذج المعدلة (`_inherit`):** `account.payment, multi.approval.mixin`
- **الملف:** `models\multi_approval_mixin.py`
  - **النماذج الجديدة (`_name`):** `multi.approval.mixin`
  - **الوصف:** Multi Approval Mixin
- **الملف:** `models\multi_approval_request.py`
  - **النماذج الجديدة (`_name`):** `multi.approval.request`, `name`, `multi.approval.line`
  - **النماذج المعدلة (`_inherit`):** `mail.thread, mail.activity.mixin`
  - **الوصف:** Multi Approval Request
- **الملف:** `models\multi_approval_type.py`
  - **النماذج الجديدة (`_name`):** `multi.approval.type`, `multi.approval.stage`
  - **الوصف:** Multi Approval Type
- **الملف:** `models\purchase_order.py`
  - **النماذج الجديدة (`_name`):** `purchase.order`
  - **النماذج المعدلة (`_inherit`):** `purchase.order, multi.approval.mixin`
- **الملف:** `models\sale_order.py`
  - **النماذج الجديدة (`_name`):** `sale.order`
  - **النماذج المعدلة (`_inherit`):** `sale.order, multi.approval.mixin`
- **الملف:** `models\stock_picking.py`
  - **النماذج الجديدة (`_name`):** `stock.picking`
  - **النماذج المعدلة (`_inherit`):** `stock.picking, multi.approval.mixin`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\multi_approval_data.xml`, `security\multi_approval_security.xml`, `views\account_move_views.xml`, `views\account_payment_views.xml`, `views\multi_approval_dashboard_views.xml`, `views\multi_approval_request_views.xml`, `views\multi_approval_type_views.xml`, `views\purchase_order_views.xml`, `views\sale_order_views.xml`, `views\stock_picking_views.xml`, `wizard\approval_refuse_wizard_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Multi Approval` أو `multi_approval` والضغط على **تثبيت (Install)**.
