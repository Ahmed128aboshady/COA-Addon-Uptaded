# arabian_construction_managment (`arabian_construction_management`)

## 📌 الوصف العام (Overview)
Short (1 phrase/line) summary of the module's purpose

### التفاصيل الوظيفية:

Long description of module's purpose
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `arabian_construction_management`
- **التصنيف (Category):** `Uncategorized`
- **الإصدار (Version):** `0.3`
- **الاعتماديات (Dependencies):** `base`, `hr`, `uom`, `account`, `purchase`, `utm`, `project`, `arabian_cheque_management`, `arabian_requisition`, `stock`, `arabian_letters_of_guarantee`, `documents`, `arabian_expense_payment`, `arabian_res_partner`, `hr_timesheet`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_move.py`
  - **النماذج المعدلة (`_inherit`):** `account.move`
- **الملف:** `models\account_payment.py`
  - **النماذج المعدلة (`_inherit`):** `account.payment`
- **الملف:** `models\advance_payment_guarantee.py`
  - **النماذج المعدلة (`_inherit`):** `lg.advance.payment.guarantee`
- **الملف:** `models\bid_bond.py`
  - **النماذج المعدلة (`_inherit`):** `lg.bid.bond`
- **الملف:** `models\boq_cost_estimation.py`
  - **النماذج الجديدة (`_name`):** `boq.cost.estimation`, `boq.cost.estimation.line`
  - **الوصف:** BOQ Cost Estimation
- **الملف:** `models\business_items_types.py`
  - **النماذج الجديدة (`_name`):** `business.items.types`
  - **الوصف:** Business Items Types
- **الملف:** `models\cheque_management.py`
  - **النماذج المعدلة (`_inherit`):** `incoming.cheque`, `outgoing.cheque`
- **الملف:** `models\construction_business_items.py`
  - **النماذج الجديدة (`_name`):** `construction.business.items`, `construction.business.items.line`
  - **النماذج المعدلة (`_inherit`):** `portal.mixin, mail.thread, mail.activity.mixin,
                utm.mixin`
  - **الوصف:** Construction Business Items
- **الملف:** `models\construction_pricing.py`
  - **النماذج الجديدة (`_name`):** `construction.pricing`, `construction.pricing.line`
  - **الوصف:** Construction Pricing
- **الملف:** `models\construction_project.py`
  - **النماذج الجديدة (`_name`):** `construction.project`
  - **الوصف:** Construction Project
- **الملف:** `models\construction_project_type.py`
  - **النماذج الجديدة (`_name`):** `construction.project.type`
  - **الوصف:** Construction Project Type
- **الملف:** `models\construction_requisition.py`
  - **النماذج المعدلة (`_inherit`):** `construction.requisition`
- **الملف:** `models\construction_subcontractor.py`
  - **النماذج الجديدة (`_name`):** `construction.subcontractor`, `construction.subcontractor.lines`
  - **الوصف:** Construction Subcontractor
- **الملف:** `models\contracting_project_classification.py`
  - **النماذج الجديدة (`_name`):** `contracting.project.classification`
  - **الوصف:** Contracting Project Classification
- **الملف:** `models\detailed_bill_of_quantities.py`
  - **النماذج الجديدة (`_name`):** `detailed.bill.of.quantities`, `bill.of.quantities.line`, `bill.quantities.labour.machines`, `bill.quantities.overhead`
  - **الوصف:** Detailed Bill Of Quantities
- **الملف:** `models\detailed_business_items.py`
  - **النماذج الجديدة (`_name`):** `detailed.business.items`
  - **النماذج المعدلة (`_inherit`):** `portal.mixin, mail.thread, mail.activity.mixin,
                utm.mixin`
  - **الوصف:** Detailed Business Items
- **الملف:** `models\expense_payment.py`
  - **النماذج المعدلة (`_inherit`):** `expense.payment`
- **الملف:** `models\interim_completion_certificate.py`
- **الملف:** `models\interim_invoice.py`
  - **النماذج الجديدة (`_name`):** `interim.invoice`, `interim.invoice.line`, `interim.invoice.deductions`
  - **الوصف:** Interim Invoice
- **الملف:** `models\maintenance_bond.py`
  - **النماذج المعدلة (`_inherit`):** `lg.maintenance.bond`
- **الملف:** `models\models.py`
  - **النماذج الجديدة (`_name`):** `arabian_construction_managment.arabian_construction_managment`
  - **الوصف:** arabian_construction_managment.arabian_construction_managment
- **الملف:** `models\performance_bond.py`
  - **النماذج المعدلة (`_inherit`):** `lg.performance.bond`
- **الملف:** `models\project_contract_management.py`
  - **النماذج الجديدة (`_name`):** `project contract management`
  - **الوصف:** Project Contract Management
- **الملف:** `models\project_project.py`
  - **النماذج المعدلة (`_inherit`):** `project.project`
- **الملف:** `models\project_task.py`
  - **النماذج المعدلة (`_inherit`):** `project.task`, `account.analytic.line`
- **الملف:** `models\purchase_order.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order`, `purchase.report`, `purchase.order.line`
- **الملف:** `models\purchase_report.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.report`
- **الملف:** `models\purchase_requisition.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.requisition`
- **الملف:** `models\res_partner.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`
- **الملف:** `models\stock_picking.py`
  - **النماذج المعدلة (`_inherit`):** `stock.picking`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\data_business_items_types.xml`, `data\data_construction_project_type.xml`, `data\data_contracting_project_classification.xml`, `data\data_detailed_business_items.xml`, `demo\demo.xml`, `security\construction_groups.xml`, `views\account_move.xml`, `views\account_payment.xml`, `views\advance_payment_guarantee.xml`, `views\bid_bond.xml`, `views\boq_cost_estimation.xml`, `views\business_items_types.xml`, `views\cheque_management.xml`, `views\construction_business_items.xml`, `views\construction_pricing.xml`, `views\construction_project.xml`, `views\construction_project_type.xml`, `views\construction_requisition.xml`, `views\construction_subcontractor.xml`, `views\contracting_project_classification.xml`, `views\detailed_bill_of_quantities.xml`, `views\detailed_business_items.xml`, `views\expense_payment.xml`, `views\interim_invoice.xml`, `views\maintenance_bond.xml`, `views\performance_bond.xml`, `views\project_project.xml`, `views\project_task.xml`, `views\purchase_order.xml`, `views\purchase_report.xml`, `views\purchase_requisition.xml`, `views\res_partner.xml`, `views\sale_order.xml`, `views\stock_picking.xml`, `views\templates.xml`, `views\time_sheet_report.xml`, `views\views.xml`, `wizard\construction_project_payment.xml`, `wizard\create_business_items.xml`, `wizard\select_detailed_boq_type.xml`, `wizard\subcontractor_attribution_boq.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `arabian_construction_managment` أو `arabian_construction_management` والضغط على **تثبيت (Install)**.
