# COA Accounting Internal Transfer — دليل التركيب والاختبار (Odoo 19)

موديول مُعاد بناؤه بالكامل لاستعادة خاصية **Internal Transfer** الكلاسيكية على
شاشة Payments، اللي شالتها Odoo من الكور بداية من نسخة 18 (ومستمرة في 19).

---

## 1. خلفية مهمة قبل التركيب

في Odoo 19، الحقول القديمة `is_internal_transfer` و `destination_journal_id`
**متشالة بالكامل من core**. التحويل الداخلي الرسمي دلوقتي بيتم فقط عن طريق
bank reconciliation على statement lines، وده مختلف جوهريًا عن الـ workflow
القديم اللي كنت متعود عليه (وده نفس اللي بيقدمه أي إضافة بتقول "Compatible
with V19" زي اللي بعتها لي من الـ Apps Store — هي بتعيد بناء الحقول من الصفر،
مش بترجّعها من كود قديم).

الموديول ده بيعمل بالظبط كده: بيعيد بناء الحقول والمنطق من الصفر، فوق نظام
الـ Outstanding Accounts الحديث (`account.payment.method.line.payment_account_id`)
بدون أي افتراض إضافي.

---

## 2. التركيب

```bash
# 1. نسخ مجلد الموديول لمجلد addons بتاع السيرفر
cp -r coa_internal_transfer /path/to/your/odoo/addons/

# 2. تحديث قائمة الموديولات
#    Settings > Apps > Update Apps List (فعّل Developer Mode الأول)

# 3. البحث عن "COA Accounting Internal Transfer" وتثبيته
```

**الاعتمادية الوحيدة:** `account` (Invoicing/Accounting). مفيش أي اعتماديات
خارجية زي `mail` (الموديول الأصلي طلبها بس هي غير ضرورية لمنطقنا).

---

## 3. خطوات الاختبار اليدوي (Checklist)

### أ. التحضير
1. اعمل جورنالين بنكيين على الأقل: **Bank A** و **Bank B**
   (Accounting → Configuration → Journals → New)
2. على كل جورنال، روح لتبويب **Incoming Payments** و **Outgoing Payments**
   وشوف الـ Payment Method "Manual" — هنا هتحدد سلوك الـ Outstanding Account.

### ب. تجربة السيناريو الأول — Paid فورًا
1. على **Bank A**: في Outgoing Payments → Manual، حدد **Outstanding Payments
   Account** = نفس الحساب الرئيسي للجورنال (Bank Account نفسه).
2. على **Bank B**: في Incoming Payments → Manual، حدد **Outstanding Receipts
   Account** = نفس الحساب الرئيسي للجورنال (Bank Account نفسه).
3. روح Accounting → Customers/Vendors → Payments → New
4. فعّل checkbox **"Internal Transfer"**
5. هتلاحظ إن حقل **Partner** و **Partner Type** اختفوا، وظهر حقل
   **Destination Journal**
6. Journal = Bank A، Destination Journal = Bank B، Amount = أي رقم
7. اضغط **Confirm**
8. **المتوقع:**
   - الـ payment الأول (Bank A) حالته بقت **Paid** فورًا
   - اتعمل payment تاني تلقائيًا في **Bank B** بحالة **Paid** كذلك
   - زرار **"Paired Transfer"** ظهر في أعلى الفورم (smart button) وبيوديك
     للـ payment التاني

### ج. تجربة السيناريو الثاني — In Process لحد الـ Reconciliation
1. اعمل حسابين جديدين من نوع **Current Assets** (للـ Receipts) و
   **Current Liabilities** (للـ Payments)، فعّل عليهم **Allow Reconciliation**
2. حدد الحسابين دول كـ Outstanding Accounts على **Bank A** و **Bank B**
   (بدل ما تستخدم الحساب الرئيسي)
3. كرر خطوات إنشاء Internal Transfer زي فوق
4. **المتوقع:**
   - الـ payment الأول حالته **In Process** (مش Paid)
   - الـ payment التاني (المُتولّد تلقائيًا) حالته كذلك **In Process**
   - لازم تعمل Bank Reconciliation يدوي عشان تتحول لـ Paid

### د. تجربة الحالة المختلطة (Mixed) — الأهم بالنسبة لطلبك
1. سيب **Bank A** بإعداد "Outstanding = Main Account" (Paid فورًا)
2. خلّي **Bank B** بإعداد "Outstanding = حساب منفصل" (In Process)
3. اعمل تحويل من Bank A → Bank B
4. **المتوقع:** الـ payment الأول (Bank A) **Paid**، والتاني (Bank B)
   **In Process** — كل جورنال بإعداده المستقل تمامًا، وده تأكيد إن
   "Outstanding Accounts" بقى **Configurable بالكامل** زي ما طلبت.

### هـ. اختبارات الحدود (Edge Cases)
| الحالة | المتوقع |
|---|---|
| تفعيل Internal Transfer بدون تحديد Destination Journal | رسالة خطأ واضحة تمنع الحفظ |
| Destination Journal = نفس Journal المصدر | رسالة خطأ تمنع التحويل لنفس الجورنال |
| Destination Journal بدون أي Payment Method مُفعّل | رسالة خطأ واضحة بدل Traceback |
| الضغط على Confirm مرتين أو إعادة فتح الـ payment وحفظه | لا يتكرر إنشاء paired payment (idempotent) |
| استخدام فلتر "Internal Transfers" في قائمة الـ Payments | يعرض فقط التحويلات الداخلية |

---

## 4. ملاحظات تقنية للمطوّر (لو احتجت تعدّل لاحقًا)

- الحقول الجديدة: `is_internal_transfer` (Boolean) و
  `destination_journal_id` (Many2one → account.journal) على `account.payment`
- الـ pairing logic بالكامل في `_create_paired_internal_transfer_payment()`
  داخل `models/account_payment.py`
- بيستخدم `paired_internal_transfer_payment_id` — حقل **موجود أصلاً في core**
  بس مهجور وملوش أي قيمة بيتظبط بيها؛ الموديول ده بيستخدمه كما هو.
- الحماية من التكرار اللانهائي (infinite recursion): أي payment بيتعمل كـ
  "paired" بييجي معاه `paired_internal_transfer_payment_id` متظبط من
  لحظة الـ `create()`، فلما يتنفذ `action_post()` عليه، شرط الفلترة
  `not paired_internal_transfer_payment_id` بيكون `False` فمش بيحاول يعمل
  pairing تاني. تم اختباره بمحاكاة Python منفصلة (بدون سيرفر Odoo) وأكدت
  عدم وجود أي recursion أو تكرار.
- لو عايز تضيف حقل "Memo" تلقائي مختلف، عدّل `_get_aml_default_display_name_list()`

---

## 5. حدود الاختبار اللي تم

بسبب قيود بيئة العمل (لا يوجد اتصال إنترنت لتحميل وتشغيل سيرفر Odoo 19 فعلي
وقاعدة بيانات PostgreSQL)، تم التحقق من:
- ✅ سلامة Python syntax (`py_compile` + AST parsing) — صفر أخطاء
- ✅ سلامة XML (`lxml` well-formed parsing) — صفر أخطاء
- ✅ محاكاة منطقية كاملة لخوارزمية الـ pairing (idempotency, recursion,
  اتجاه التحويل، رفض self-transfer) — كل الاختبارات نجحت
- ✅ محاكاة سيناريوهات Outstanding Account (Paid / In Process / Mixed)
- ⚠️ **لم يتم** التشغيل الفعلي على سيرفر Odoo 19 حقيقي — هذا مطلوب منك
  كخطوة أخيرة قبل النشر على بيئة Production، باستخدام الـ Checklist في
  القسم 3 أعلاه.
