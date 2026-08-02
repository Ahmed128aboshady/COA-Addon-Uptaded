# Purchase Approval Workflow (`purchase_approval_workflow`)

## 📌 الوصف العام (Overview)
Configurable multi-level purchase order approval workflow

### التفاصيل الوظيفية:

Purchase Approval Workflow
==========================
Introduces a fully configurable, multi-level purchase order approval workflow
with 14 advanced features for enterprise-grade procurement governance.

Key Features:
1.  SLA & Escalation: per-level deadline, overdue badge, automatic escalation cron
2.  One-Click Email Approval: tokenized Approve/Reject buttons in notification emails
3.  Bulk Approval Dashboard: My/All Pending Approvals with inline actions and bulk server action
4.  Delegation / Out-of-Office: delegate approvals to another user with an optional end date
5.  Trusted Vendor Bypass: skip workflow for trusted vendors below a configurable amount limit
6.  Parallel Approval (AND logic): require all group members to approve before advancing
7.  HR Manager Auto-Routing: automatically route to the buyer's HR manager hierarchy
8.  Budget Check Integration: real-time remaining budget warning on PO approval screen
9.  Approval Analytics Dashboard: pivot + bar/trend graph views on approval history
10. Change Summary on Resubmission: automatic chatter diff of what changed since last submission
11. Approval Policy Templates: wizard to create pre-built matrix configurations in one click
12. Vendor-Specific Rules: restrict matrix rules to a specific vendor
13. Urgency Override: mark POs as Urgent or Critical to fast-track or escalate routing
14. Export Audit Trail: download the full audit trail as a formatted Excel file or branded PDF
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `purchase_approval_workflow`
- **التصنيف (Category):** `Purchase`
- **الإصدار (Version):** `19.0.4.0.0`
- **الاعتماديات (Dependencies):** `purchase`, `mail`, `hr`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\purchase_approval_history.py`
  - **النماذج الجديدة (`_name`):** `purchase.approval.history`
  - **الوصف:** Purchase Approval History
- **الملف:** `models\purchase_approval_matrix.py`
  - **النماذج الجديدة (`_name`):** `purchase.approval.matrix`, `%s (Level %d)`
  - **الوصف:** Purchase Approval Matrix
- **الملف:** `models\purchase_approval_matrix_diagram.py`
  - **النماذج الجديدة (`_name`):** `purchase.approval.matrix.diagram`
  - **الوصف:** Approval Workflow Diagram
- **الملف:** `models\purchase_approval_vote.py`
  - **النماذج الجديدة (`_name`):** `purchase.approval.vote`
  - **الوصف:** Purchase Approval Parallel Vote
- **الملف:** `models\purchase_order.py`
  - **النماذج المعدلة (`_inherit`):** `purchase.order`
- **الملف:** `models\res_config_settings.py`
  - **النماذج المعدلة (`_inherit`):** `res.config.settings`
- **الملف:** `models\res_partner_approval.py`
  - **النماذج المعدلة (`_inherit`):** `res.partner`
- **الملف:** `models\res_users_approval.py`
  - **النماذج المعدلة (`_inherit`):** `res.users`

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `data\cron_data.xml`, `data\mail_template_data.xml`, `security\record_rules.xml`, `security\security_groups.xml`, `views\purchase_approval_analytics_views.xml`, `views\purchase_approval_audit_export_wizard_views.xml`, `views\purchase_approval_audit_trail_report.xml`, `views\purchase_approval_dashboard_views.xml`, `views\purchase_approval_history_views.xml`, `views\purchase_approval_matrix_diagram_views.xml`, `views\purchase_approval_matrix_views.xml`, `views\purchase_approval_policy_wizard_views.xml`, `views\purchase_approval_reject_wizard_views.xml`, `views\purchase_order_views.xml`, `views\res_config_settings_views.xml`, `views\res_partner_views.xml`, `views\res_users_views.xml`
- **ملفات التقارير (`Reports`):** `views\purchase_approval_audit_trail_report.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Purchase Approval Workflow` أو `purchase_approval_workflow` والضغط على **تثبيت (Install)**.
