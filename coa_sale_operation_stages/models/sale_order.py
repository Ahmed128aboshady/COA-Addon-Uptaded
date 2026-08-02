# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_operations = fields.Boolean(
        string='يوجد عمليات قبل التسليم',
        default=False,
        tracking=True,
    )
    operation_mode = fields.Selection([
        ('all',      'كل المنتجات'),
        ('specific', 'منتجات محددة'),
    ], string='نطاق العمليات', default='all',
       help='كل المنتجات: كل الأصناف القابلة للتخزين هتعدي بالعمليات\n'
            'منتجات محددة: بس الأصناف اللي علّمتها في الجدول')

    operation_ids = fields.One2many('sale.operation', 'sale_order_id', string='العمليات')
    operation_count = fields.Integer(compute='_compute_operation_count')
    operations_state = fields.Selection([
        ('none',        'لا يوجد'),
        ('pending',     'في الانتظار'),
        ('in_progress', 'جاري التنفيذ'),
        ('done',        'اكتملت'),
    ], compute='_compute_operations_state', store=True)

    @api.depends('operation_ids')
    def _compute_operation_count(self):
        for order in self:
            order.operation_count = len(order.operation_ids)

    @api.depends('operation_ids.state', 'has_operations')
    def _compute_operations_state(self):
        for order in self:
            if not order.has_operations:
                order.operations_state = 'none'
                continue
            ops = order.operation_ids
            if not ops:
                order.operations_state = 'pending'
            elif all(o.state == 'done' for o in ops):
                order.operations_state = 'done'
            elif any(o.state == 'in_progress' for o in ops):
                order.operations_state = 'in_progress'
            else:
                order.operations_state = 'pending'

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.has_operations:
                order._create_operations()
                order._lock_delivery()
        return res

    def _create_operations(self):
        """إنشاء العمليات — sudo لأنها تلقائية من تأكيد الأوردر"""
        self.ensure_one()
        if self.operation_mode == 'specific':
            lines = self.order_line.filtered(
                lambda l: l.has_operation and l.product_id.type in ('consu', 'product')
            )
        else:
            lines = self.order_line.filtered(
                lambda l: l.product_id.type in ('consu', 'product')
            )
        for line in lines:
            self.env['sale.operation'].sudo().create({
                'sale_order_id': self.id,
                'product_id':    line.product_id.id,
                'qty':           line.product_uom_qty,
                'sale_line_id':  line.id,
            })

    def _lock_delivery(self):
        """
        all:      قفل الـ picking كله
        specific: قفل الـ stock.move بتاعت الأصناف اللي عليها عمليات بس
        """
        self.ensure_one()
        pickings = self.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))

        if self.operation_mode == 'all':
            pickings.write({'operation_locked': True})
        else:
            # الأصناف اللي عليها عمليات بس
            op_products = self.order_line.filtered('has_operation').mapped('product_id')
            for picking in pickings:
                for move in picking.move_ids.filtered(lambda m: m.product_id in op_products):
                    move.operation_locked = True

    def _check_operations_complete(self):
        """لما تكتمل كل العمليات — افتح التسليم وأرسل إشعار"""
        self.ensure_one()
        all_done = all(op.state == 'done' for op in self.operation_ids)
        if not all_done:
            return

        pickings = self.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))

        if self.operation_mode == 'all':
            pickings.write({'operation_locked': False})
        else:
            # افتح الـ moves المقفولة بس
            for picking in pickings:
                picking.move_ids.filtered('operation_locked').write({'operation_locked': False})

        # احجز الكميات تاني عشان الـ backorder يتسلم بدون مشكلة
        # pickings.action_assign()

        # إشعار على الأوردر
        self.message_post(
            body=_('✅ اكتملت جميع العمليات على <b>%s</b> — تم فتح التسليم') % self.name
        )

        # إشعار + Activity على كل Picking
        for picking in pickings:
            picking.message_post(
                body=_(
                    '🟢 <b>العمليات اكتملت — يمكن التسليم الآن</b><br/>'
                    'الأوردر: <b>%s</b> — العميل: <b>%s</b>'
                ) % (self.name, self.partner_id.name),
                subtype_xmlid='mail.mt_note',
            )
            picking.activity_schedule(
                act_type_xmlid='mail.mail_activity_data_todo',
                summary=_('العمليات اكتملت — جاهز للتسليم'),
                note=_(
                    'الأوردر <b>%s</b> — العميل: <b>%s</b><br/>'
                    'جميع العمليات اكتملت. يرجى متابعة التسليم.'
                ) % (self.name, self.partner_id.name),
                user_id=picking.user_id.id or self.env.uid,
            )

    def action_view_operations(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'العمليات — %s' % self.name,
            'res_model': 'sale.operation',
            'view_mode': 'list,kanban,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id},
            'target': 'current',
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_operation = fields.Boolean(
        string='يحتاج عمليات',
        default=False,
        help='علّم هذا الصنف لو هيعدي بعمليات قبل التسليم',
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    operation_locked = fields.Boolean(
        string='مقفول - في انتظار العمليات',
        default=False,
    )


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    operation_locked = fields.Boolean(
        string='مقفول - في انتظار العمليات',
        default=False,
        tracking=True,
    )
    #
    # def button_validate(self):
    #     """منع التسليم لو في عمليات لسه مش خلصت"""
    #     for picking in self:
    #         # all mode: الـ picking كله محجوز — وقف كامل
    #         if picking.operation_locked:
    #             raise UserError(
    #                 '⚠️ مش ممكن تسلم!\n'
    #                 'كل المنتجات لسه في مرحلة العمليات.\n'
    #                 'لازم تكتمل جميع العمليات الأول.'
    #             )
    #
    #         locked_moves = picking.move_ids.filtered('operation_locked')
    #         if not locked_moves:
    #             continue
    #
    #         unlocked_moves = picking.move_ids - locked_moves
    #
    #         # لو كل الأصناف محجوزة بالعمليات (مفيش حاجة تتسلم دلوقتي)
    #         if not unlocked_moves:
    #             names = '\n'.join('• ' + n for n in locked_moves.mapped('product_id.name'))
    #             raise UserError(
    #                 '⚠️ مش ممكن تسلم — الأصناف دي لسه في مرحلة العمليات:\n\n'
    #                 '%s\n\n'
    #                 'لازم تكتمل العمليات الأول.' % names
    #             )
    #
    #         # تأكد إن الأصناف العادية عندها كمية تسليم
    #         for move in unlocked_moves:
    #             if not move.move_line_ids:
    #                 move.action_assign()
    #             for ml in move.move_line_ids:
    #                 if not ml.quantity:
    #                     ml.quantity = ml.quantity_product_uom
    #
    #         # صفّر الأصناف المحجوزة → Odoo يعمل backorder لها تلقائياً
    #         locked_moves.move_line_ids.write({'quantity': 0})
    #
    #     return super().button_validate()
