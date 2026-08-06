import ast
import math
import logging
import re
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


# ===================================================================
# دوال Excel — تشتغل بالاسم الكبير أو الصغير زي الإكسيل بالظبط
# ===================================================================

def _excel_if(condition, value_if_true, value_if_false=0):
    """Excel: IF(condition, value_if_true, value_if_false)
    مثال: IF(L > 2, L * W * 2, L * W)
    """
    return value_if_true if condition else value_if_false


def _excel_ifs(*args):
    """Excel: IFS(cond1, val1, cond2, val2, ...) — أول شرط يتحقق يرجع قيمته
    مثال: IFS(L < 1, 0, L < 2, L * W, L >= 2, L * W * 1.1)
    """
    if len(args) % 2 != 0:
        raise ValueError('IFS يحتاج عدد زوجي من المعاملات: IFS(شرط1, قيمة1, شرط2, قيمة2, ...)')
    for i in range(0, len(args), 2):
        if args[i]:
            return args[i + 1]
    return 0


def _excel_and(*args):
    """Excel: AND(a, b, ...) — True لو كل الشروط محققة
    مثال: AND(L > 0, W > 0, N > 0)
    """
    return all(bool(a) for a in args)


def _excel_or(*args):
    """Excel: OR(a, b, ...) — True لو شرط واحد على الأقل محقق
    مثال: OR(L > 5, W > 5)
    """
    return any(bool(a) for a in args)


def _excel_not(value):
    """Excel: NOT(value) — عكس الشرط
    مثال: NOT(L > 5)
    """
    return not bool(value)


def _excel_sum(*args):
    """Excel: SUM(a, b, c, ...) — مجموع قيم
    مثال: SUM(L, W, T)
    """
    return sum(float(a) for a in args)


def _excel_average(*args):
    """Excel: AVERAGE(a, b, ...) — متوسط
    مثال: AVERAGE(L, W)
    """
    if not args:
        return 0.0
    return sum(float(a) for a in args) / len(args)


def _excel_mod(number, divisor):
    """Excel: MOD(number, divisor) — باقي القسمة
    مثال: MOD(L, 3) — كام قطعة بتفضل
    """
    return number % divisor


def _excel_power(number, pwr):
    """Excel: POWER(number, power) — رفع لقوة
    مثال: POWER(L, 2) = L^2
    """
    return number ** pwr


def _excel_log(number, base=10):
    """Excel: LOG(number, [base]) — لوغاريتم (أساسه 10 افتراضياً)
    مثال: LOG(L, 10)
    """
    return math.log(number, base)


def _excel_ln(number):
    """Excel: LN(number) — لوغاريتم طبيعي
    مثال: LN(L)
    """
    return math.log(number)


def _excel_exp(number):
    """Excel: EXP(number) — e مرفوعة للقوة number
    مثال: EXP(L)
    """
    return math.exp(number)


def _excel_roundup(number, num_digits=0):
    """Excel: ROUNDUP(number, num_digits) — تقريب لأعلى
    مثال: ROUNDUP(L * W, 2) — تقريب لأعلى لـ خانتين عشريتين
    """
    factor = 10 ** int(num_digits)
    return math.ceil(number * factor) / factor


def _excel_rounddown(number, num_digits=0):
    """Excel: ROUNDDOWN(number, num_digits) — تقريب لأسفل
    مثال: ROUNDDOWN(L * W, 2)
    """
    factor = 10 ** int(num_digits)
    return math.floor(number * factor) / factor


def _excel_ceiling(number, significance=1):
    """Excel: CEILING(number, significance) — تقريب لأعلى لأقرب مضاعف
    مثال: CEILING(L, 0.5) — أقرب نص متر للأعلى
    """
    if significance == 0:
        return 0.0
    return math.ceil(number / significance) * significance


def _excel_floor_fn(number, significance=1):
    """Excel: FLOOR(number, significance) — تقريب لأسفل لأقرب مضاعف
    مثال: FLOOR(L, 0.5) — أقرب نص متر للأسفل
    """
    if significance == 0:
        return 0.0
    return math.floor(number / significance) * significance


def _excel_pi():
    """Excel: PI() — قيمة π = 3.14159..."""
    return math.pi


def _excel_iferror(value, value_if_error):
    """Excel: IFERROR(value, value_if_error) — لو القيمة خطأ يرجع البديل
    ملاحظة: كلا الجانبين يُحسبان أولاً (سلوك Python)
    مثال: IFERROR(L / W, 0)
    """
    if value is None:
        return value_if_error
    try:
        if isinstance(value, float) and math.isnan(value):
            return value_if_error
    except Exception:
        pass
    return value


def _excel_max(*args):
    """Excel: MAX(a, b, ...) — أكبر قيمة"""
    return max(float(a) for a in args)


def _excel_min(*args):
    """Excel: MIN(a, b, ...) — أصغر قيمة"""
    return min(float(a) for a in args)


# ===================================================================
# جدول الدوال والثوابت الآمنة المسموح بها في المعادلات
# ===================================================================
SAFE_BUILTINS = {
    # ── Python أساسي ──────────────────────────────────────────────
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'int': int,
    'float': float,
    'bool': bool,
    'sum': sum,

    # ── رياضيات Python ────────────────────────────────────────────
    'sqrt': math.sqrt,
    'ceil': math.ceil,
    'floor': math.floor,
    'pow': pow,
    'log': math.log,
    'log10': math.log10,
    'log2': math.log2,
    'exp': math.exp,
    'pi': math.pi,
    'e': math.e,

    # ── Excel — أسماء صغيرة (تكتب في الكود زي Python) ────────────
    'if_': _excel_if,
    'ifs': _excel_ifs,
    'and_': _excel_and,
    'or_': _excel_or,
    'not_': _excel_not,
    'mod': _excel_mod,
    'power': _excel_power,
    'ln': _excel_ln,
    'average': _excel_average,
    'avg': _excel_average,
    'roundup': _excel_roundup,
    'rounddown': _excel_rounddown,
    'ceiling': _excel_ceiling,
    'iferror': _excel_iferror,

    # ── Excel — أسماء كبيرة (نفس الإكسيل بالظبط) ─────────────────
    'IF': _excel_if,
    'IFS': _excel_ifs,
    'AND': _excel_and,
    'OR': _excel_or,
    'NOT': _excel_not,
    'SUM': _excel_sum,
    'AVERAGE': _excel_average,
    'AVG': _excel_average,
    'MOD': _excel_mod,
    'POWER': _excel_power,
    'LOG': _excel_log,
    'LN': _excel_ln,
    'EXP': _excel_exp,
    'ABS': abs,
    'ROUND': round,
    'MIN': _excel_min,
    'MAX': _excel_max,
    'INT': int,
    'SQRT': math.sqrt,
    'CEIL': math.ceil,
    'FLOOR': _excel_floor_fn,
    'CEILING': _excel_ceiling,
    'ROUNDUP': _excel_roundup,
    'ROUNDDOWN': _excel_rounddown,
    'IFERROR': _excel_iferror,
    'PI': _excel_pi,           # PI() بصيغة Excel

    # ── ثوابت Boolean بصيغة Excel ─────────────────────────────────
    'TRUE': True,
    'FALSE': False,
}

# أسماء الدوال القابلة للاستدعاء (للـ security check)
SAFE_CALLABLE_NAMES = frozenset(
    name for name, val in SAFE_BUILTINS.items() if callable(val)
)


def _preprocess_formula(formula):
    """
    يحوّل صياغة Excel إلى Python قبل الحساب:
      = في البداية  → يُشال  (المعادلات في Excel بتبدأ بـ =)
      ^             → **     (عامل القوة في Excel)
      <>            → !=     (غير مساوٍ في Excel)
    """
    result = formula.strip()
    # شيل علامة = من الأول لو المعادلة بتبدأ بيها (زي Excel)
    if result.startswith('='):
        result = result[1:].strip()
    # استبدل ^ بـ ** لعامل القوة
    result = re.sub(r'\^', '**', result)
    # استبدل <> بـ != (غير مساوٍ بصيغة Excel)
    result = re.sub(r'<>', '!=', result)
    return result


class MrpBomFormulaVariable(models.Model):
    """متغيرات المدخلات والثوابت — بتظهر كحقول في التاب"""
    _name = 'mrp.bom.formula.variable'
    _description = 'BOM Formula Variable'
    _order = 'sequence, id'

    bom_id = fields.Many2one('mrp.bom', string='BOM', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(
        string='اسم المتغير',
        required=True,
        help='الاسم اللي هتستخدمه في المعادلة — حروف وأرقام إنجليزي بس.\n'
             'أمثلة: L, W, T, N, q1, wall_k, door_h'
    )
    label = fields.Char(
        string='الوصف',
        help='وصف بالعربي — مثال: الطول (م)، ثابت عرض الحائط'
    )
    value = fields.Float(string='القيمة', digits=(16, 6))
    var_type = fields.Selection([
        ('input', 'مدخل (بيتغير لكل باب)'),
        ('constant', 'ثابت'),
    ], string='النوع', default='input', required=True)


class MrpBomFormulaLine(models.Model):
    """سطر المعادلة — صنف + معادلة = كمية محسوبة"""
    _name = 'mrp.bom.formula.line'
    _description = 'BOM Formula Line'
    _order = 'sequence, id'

    bom_id = fields.Many2one('mrp.bom', string='BOM', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    product_id = fields.Many2one(
        'product.product', string='الصنف', required=True,
        domain=[('type', 'in', ['consu', 'product'])]
    )
    product_uom_id = fields.Many2one(
        'uom.uom', string='الوحدة',
        related='product_id.uom_id', readonly=True
    )
    description = fields.Char(
        string='الوصف',
        help='مثال: الحلق، البرواز، الشاسيه'
    )
    formula = fields.Text(
        string='المعادلة',
        required=True,
        help="""اكتب المعادلة بصيغة Excel أو Python.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
عوامل Excel المدعومة:
  ^   للقوة: L^2 = L**2
  <>  لغير مساوٍ: L <> 0  =  L != 0

دوال Excel المدعومة (كبيرة وصغيرة):
  IF(cond, true, false)       مثال: IF(T > 0.1, L*W*2, 0)
  IFS(c1,v1, c2,v2, ...)      شروط متعددة
  AND(a, b) / OR(a, b)        شروط منطقية
  SUM(a, b, c)                مجموع
  AVERAGE(a, b)               متوسط
  ROUND(n, 2) / ROUNDUP / ROUNDDOWN
  CEILING(L, 0.5)             أقرب مضاعف للأعلى
  MOD(L, 3)                   باقي القسمة
  POWER(L, 2)                 قوة = L^2
  SQRT(L)                     جذر تربيعي
  ABS(x) / MIN / MAX
  LOG(n) / LN(n) / EXP(n)
  PI()                        = 3.14159...
  TRUE / FALSE                قيم منطقية

أمثلة:
  ((L * 2) + W) * q1 * N * 1.1
  IF(T < 0.1, 0, L * W * 2 * N)
  CEILING(L * q1 * N, 0.5)
  ROUND(L * W * 2 * N, 4)
  L^2 * pi * 0.001""",
    )
    computed_qty = fields.Float(
        string='الكمية المحسوبة', digits=(16, 6),
        readonly=True, store=True
    )
    formula_error = fields.Char(string='خطأ في المعادلة', readonly=True)

    sync_to_bom = fields.Boolean(
        string='تحديث BOM تلقائي؟',
        default=True,
        help='لو مفعّل، الكمية المحسوبة بتتنقل تلقائياً لـ BOM Lines'
    )
    bom_line_id = fields.Many2one(
        'mrp.bom.line', string='BOM Line المرتبطة', readonly=True
    )

    def _get_formula_context(self):
        """يبني context المتغيرات اللي المعادلة بتشتغل فيها"""
        self.ensure_one()
        ctx = dict(SAFE_BUILTINS)
        for var in self.bom_id.formula_variable_ids:
            if var.name:
                ctx[var.name] = var.value
        return ctx

    def action_compute(self):
        """يحسب الكمية من المعادلة بصيغة Excel أو Python"""
        for rec in self:
            if not rec.formula:
                rec.computed_qty = 0.0
                rec.formula_error = False
                continue

            raw_formula = rec.formula.strip()
            # ─── تحويل صياغة Excel إلى Python ───
            formula_py = _preprocess_formula(raw_formula)

            ctx = rec._get_formula_context()
            try:
                # تحليل المعادلة للتأكد من أنها expression آمنة
                tree = ast.parse(formula_py, mode='eval')

                # فحص أمان الـ AST
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        raise UserError('الـ import غير مسموح في المعادلات.')
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            raise UserError(
                                f'استدعاء الدوال بالشكل "object.method()" غير مسموح.'
                            )
                        if isinstance(node.func, ast.Name):
                            fname = node.func.id
                            if fname not in SAFE_CALLABLE_NAMES:
                                raise UserError(
                                    f'الدالة "{fname}" غير مسموح بها.\n'
                                    f'الدوال المتاحة: IF, AND, OR, NOT, SUM, AVERAGE, '
                                    f'ROUND, ROUNDUP, ROUNDDOWN, CEILING, FLOOR, MOD, '
                                    f'POWER, SQRT, ABS, MIN, MAX, LOG, LN, EXP, PI, INT, IFERROR'
                                )

                result = eval(compile(tree, '<formula>', 'eval'), {'__builtins__': {}}, ctx)
                rec.computed_qty = float(result)
                rec.formula_error = False

            except UserError as e:
                rec.computed_qty = 0.0
                rec.formula_error = str(e.args[0]) if e.args else str(e)
            except ZeroDivisionError:
                rec.computed_qty = 0.0
                rec.formula_error = 'قسمة على صفر — تحقق من قيم المتغيرات'
            except NameError as e:
                rec.computed_qty = 0.0
                var_name = str(e).split("'")[1] if "'" in str(e) else str(e)
                rec.formula_error = (
                    f'متغير غير معرّف: "{var_name}" — '
                    f'تأكد من تعريفه في جدول المتغيرات فوق'
                )
            except SyntaxError as e:
                rec.computed_qty = 0.0
                rec.formula_error = f'خطأ في كتابة المعادلة: {e.msg}'
            except TypeError as e:
                rec.computed_qty = 0.0
                rec.formula_error = f'خطأ في نوع البيانات: {e}'
            except ValueError as e:
                rec.computed_qty = 0.0
                rec.formula_error = f'قيمة خاطئة: {e}'
            except Exception as e:
                rec.computed_qty = 0.0
                rec.formula_error = f'خطأ: {e}'
                _logger.warning('BOM Formula error in line %s: %s', rec.id, e)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    formula_variable_ids = fields.One2many(
        'mrp.bom.formula.variable', 'bom_id',
        string='المتغيرات والثوابت'
    )
    formula_line_ids = fields.One2many(
        'mrp.bom.formula.line', 'bom_id',
        string='معادلات المكونات'
    )
    formula_note = fields.Text(
        string='ملاحظات',
        help='أي ملاحظات على المعادلات أو افتراضات الحساب'
    )

    def action_compute_all_formulas(self):
        """يحسب كل المعادلات ويحدّث BOM Lines"""
        for bom in self:
            bom.formula_line_ids.action_compute()
            bom._sync_formula_lines_to_bom()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'تم الحساب',
                'message': 'تم حساب جميع المعادلات وتحديث BOM Lines بنجاح ✓',
                'type': 'success',
                'sticky': False,
            }
        }

    def _sync_formula_lines_to_bom(self):
        """ينقل الكميات المحسوبة لـ BOM Lines"""
        self.ensure_one()
        BomLine = self.env['mrp.bom.line']
        for fline in self.formula_line_ids.filtered(
            lambda l: l.sync_to_bom and not l.formula_error
        ):
            if fline.bom_line_id:
                # تحديث السطر الموجود
                fline.bom_line_id.product_qty = fline.computed_qty
            else:
                # ابحث عن سطر موجود بنفس الصنف
                existing = BomLine.search([
                    ('bom_id', '=', self.id),
                    ('product_id', '=', fline.product_id.id),
                ], limit=1)
                if existing:
                    existing.product_qty = fline.computed_qty
                    fline.bom_line_id = existing
                else:
                    # أنشئ سطر جديد
                    new_line = BomLine.create({
                        'bom_id': self.id,
                        'product_id': fline.product_id.id,
                        'product_qty': fline.computed_qty,
                    })
                    fline.bom_line_id = new_line

    def action_reset_formula_values(self):
        """إعادة تصفير قيم المدخلات"""
        self.ensure_one()
        self.formula_variable_ids.filtered(
            lambda v: v.var_type == 'input'
        ).write({'value': 0.0})
        return True
