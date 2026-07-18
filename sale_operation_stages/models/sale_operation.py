# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOperation(models.Model):
    _name = 'sale.operation'
    _description = 'عملية على منتج'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='رقم العملية',
        readonly=True,
        default='جديد',
        copy=False,
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='سيلز أوردر',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    partner_id = fields.Many2one(
        related='sale_order_id.partner_id',
        string='العميل',
        store=True,
    )
    product_id = fields.Many2one(
        'product.product',
        string='المنتج',
        required=True,
        tracking=True,
    )
    qty = fields.Float(
        string='الكمية',
        required=True,
        default=1.0,
    )
    uom_id = fields.Many2one(
        related='product_id.uom_id',
        string='الوحدة',
        store=True,
    )
    stage_id = fields.Many2one(
        'sale.operation.stage',
        string='المرحلة الحالية',
        tracking=True,
        group_expand='_read_group_stage_ids',
    )
    stage_history_ids = fields.One2many(
        'sale.operation.stage.log',
        'operation_id',
        string='سجل المراحل',
    )
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('in_progress', 'جاري التنفيذ'),
        ('done', 'اكتملت'),
        ('cancelled', 'ملغية'),
    ], string='الحالة', default='draft', tracking=True)

    picking_in_id = fields.Many2one(
        'stock.picking',
        string='حركة الاستلام',
        readonly=True,
        help='حركة نقل المنتج لمخزن العمليات'
    )
    picking_out_id = fields.Many2one(
        'stock.picking',
        string='حركة التسليم',
        readonly=True,
        help='حركة نقل المنتج للعميل بعد اكتمال العمليات'
    )

    sale_line_id = fields.Many2one(
        'sale.order.line',
        string='سطر الأوردر',
        readonly=True,
        ondelete='set null',
    )
    notes = fields.Text(string='ملاحظات')
    color = fields.Integer(related='stage_id.color', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'جديد') == 'جديد':
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.operation') or 'جديد'
        return super().create(vals_list)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['sale.operation.stage'].search([])

    def action_start(self):
        """ابدأ العمليات — انقل المنتج لمخزن العمليات"""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError('العملية شغالة بالفعل!')

        # أول مرحلة
        first_stage = self.env['sale.operation.stage'].search(
            [('is_first', '=', True)], limit=1
        )
        if not first_stage:
            first_stage = self.env['sale.operation.stage'].search([], order='sequence', limit=1)

        self.write({
            'state': 'in_progress',
            'stage_id': first_stage.id if first_stage else False,
        })

        # سجل المرحلة
        if first_stage:
            self._log_stage(first_stage)

        self.message_post(body=_('بدأت العمليات على المنتج %s') % self.product_id.name)

    def action_next_stage(self):
        """انتقل للمرحلة الجاية"""
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError('لازم تبدأ العملية الأول!')

        # تحقق من الصلاحية
        if self.stage_id.responsible_group_id:
            if not self.env.user.has_group(
                self.stage_id.responsible_group_id.get_external_id().get(
                    self.stage_id.responsible_group_id.id
                )
            ):
                raise UserError(
                    'مش عندك صلاحية تأكيد المرحلة دي!\nالمسؤول: %s'
                    % self.stage_id.responsible_group_id.name
                )

        # المرحلة الجاية
        next_stage = self.env['sale.operation.stage'].search([
            ('sequence', '>', self.stage_id.sequence),
        ], order='sequence', limit=1)

        if next_stage:
            self.stage_id = next_stage
            self._log_stage(next_stage)
            self.message_post(body=_('انتقل للمرحلة: %s') % next_stage.name)

            # لو مرحلة نهائية
            if next_stage.is_last:
                self.action_complete()
        else:
            self.action_complete()

    def action_complete(self):
        """اكتملت العمليات — فتح التسليم"""
        self.ensure_one()
        self.write({'state': 'done'})
        self.message_post(body=_('✅ اكتملت جميع العمليات — المنتج جاهز للتسليم'))

        # فتح التسليم على السيلز أوردر
        self.sale_order_id._check_operations_complete()

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'cancelled'})
        self.message_post(body=_('❌ تم إلغاء العملية'))

    def _log_stage(self, stage):
        self.env['sale.operation.stage.log'].create({
            'operation_id': self.id,
            'stage_id': stage.id,
            'user_id': self.env.uid,
            'date': fields.Datetime.now(),
        })


class SaleOperationStageLog(models.Model):
    _name = 'sale.operation.stage.log'
    _description = 'سجل مراحل العملية'
    _order = 'date desc'

    operation_id = fields.Many2one('sale.operation', required=True, ondelete='cascade')
    stage_id = fields.Many2one('sale.operation.stage', string='المرحلة', required=True)
    user_id = fields.Many2one('res.users', string='بواسطة')
    date = fields.Datetime(string='التاريخ', default=fields.Datetime.now)
    notes = fields.Char(string='ملاحظة')
