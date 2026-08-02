# Inventory/Stock Aging Report (`sr_stock_aging_report`)

## 📌 الوصف العام (Overview)
Stock Aging Report By Warehouse and By Location

### التفاصيل الوظيفية:

        Stock Aging Report
        ==================
        The stock aging analysis report helps you analyze the age of your stock
        by organizing the value and quantity into configurable time periods.

        Features:
        - Stock Aging Report by Warehouse
        - Stock Aging Report by Location
        - Filter by Products or Product Categories
        - Configurable aging periods (e.g. 0-30, 31-60, 61-90, 91-120, 120+ days)
        - PDF Export
        - FIFO-based age calculation
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sr_stock_aging_report`
- **التصنيف (Category):** `Inventory/Inventory`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `stock`, `mail`

---

## 📦 النماذج البرمجية (Models & Backend)
لا توجد نماذج بايثون مخصصة أو معقدة.

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `report\stock_aging_report_action.xml`, `report\stock_aging_report_template.xml`, `wizard\stock_aging_wizard_view.xml`
- **ملفات التقارير (`Reports`):** `report\stock_aging_report_action.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Inventory/Stock Aging Report` أو `sr_stock_aging_report` والضغط على **تثبيت (Install)**.
