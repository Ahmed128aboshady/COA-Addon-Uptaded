# Sale Payment Milestones (`sale_payment_milestone`)

## 📌 الوصف العام (Overview)
شروط سداد بالمراحل مع ربط مباشر بالمدفوعات المحاسبية

### التفاصيل الوظيفية:

        يتيح هذا الأدون للمبيعات تحديد جدول دفعات تفصيلي على أوردر البيع
        (مثل 10% تعاقد، 25% بداية تصنيع، ...) وربطها بالمدفوعات الفعلية
        المسجلة في المحاسبة دون الحاجة لإصدار فاتورة مسبقة.
    

---

## 🛠️ معلومات الموديول (Module Metadata)
- **الاسم الفني (Technical Name):** `sale_payment_milestone`
- **التصنيف (Category):** `Sales/Sales`
- **الإصدار (Version):** `19.0.1.0.0`
- **الاعتماديات (Dependencies):** `sale_management`, `account`

---

## 📦 النماذج البرمجية (Models & Backend)
- **الملف:** `models\account_payment.py`
  - **النماذج المعدلة (`_inherit`):** `account.payment`
- **الملف:** `models\sale_order.py`
  - **النماذج المعدلة (`_inherit`):** `sale.order`
- **الملف:** `models\sale_payment_milestone.py`
  - **النماذج الجديدة (`_name`):** `sale.payment.milestone`, `sale.milestone.payment.line`
  - **الوصف:** مرحلة سداد على أوردر البيع

---

## 🖥️ الواجهات والتقارير (Views & Reports)
- **ملفات الواجهات (`Views`):** `views\sale_order_views.xml`, `views\sale_payment_milestone_views.xml`, `wizard\milestone_reconcile_wizard_views.xml`

---

## 🚀 كيفية الاستخدام والتثبيت (Installation & Usage)
1. قُم بإضافة مجلد الموديول إلى مسار `addons_path` الخاص بالسيرفر.
2. قُم بتحديث قائمة الموديولات في أودو (Update Apps List).
3. البحث عن `Sale Payment Milestones` أو `sale_payment_milestone` والضغط على **تثبيت (Install)**.
