# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalOrder(CustomerPortal):

    # ─── إضافة tile الـ "طلب أوردر" في My Account ───────────────────────────────

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        # دايماً نبعت 1 عشان الـ tile يظهر (مش بيعرض رقم للعميل)
        if 'order_request_count' in counters:
            values['order_request_count'] = 1
        return values

    # ─── صفحة النموذج ───────────────────────────────────────────────────────────

    @http.route('/my/order/request', type='http', auth='user', website=True)
    def portal_order_form(self, error=None, **kwargs):
        partner = request.env.user.partner_id
        # كل العناوين المرتبطة بالعميل (الشركة + الفروع)
        addresses = request.env['res.partner'].sudo().search([
            '|',
            ('id', '=', partner.id),
            ('parent_id', '=', partner.commercial_partner_id.id),
        ])
        if not addresses:
            addresses = partner

        values = {
            'partner': partner,
            'addresses': addresses,
            'error': error,
            'page_name': 'order_request',
        }
        return request.render('customer_portal_order.portal_order_form', values)

    # ─── استقبال النموذج وإنشاء الأوردر ─────────────────────────────────────────

    @http.route('/my/order/submit', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def portal_order_submit(self, **kwargs):
        partner = request.env.user.partner_id

        partner_shipping_id = int(kwargs.get('partner_shipping_id') or partner.id)
        partner_invoice_id  = int(kwargs.get('partner_invoice_id') or partner.id)
        note = kwargs.get('note', '').strip()

        form = request.httprequest.form
        product_ids = form.getlist('product_id[]')
        quantities  = form.getlist('qty[]')

        # بناء سطور الأوردر
        order_lines = []
        for pid, qty in zip(product_ids, quantities):
            try:
                pid = int(pid)
                qty = float(qty)
                if pid > 0 and qty > 0:
                    product = request.env['product.product'].sudo().browse(pid)
                    if product.exists() and product.sale_ok:
                        order_lines.append((0, 0, {
                            'product_id': pid,
                            'product_uom_qty': qty,
                            'price_unit': product.lst_price,
                        }))
            except (ValueError, TypeError):
                continue

        if not order_lines:
            return request.redirect('/my/order/request?error=1')

        # إنشاء السيلز أوردر
        order = request.env['sale.order'].sudo().create({
            'partner_id':          partner.id,
            'partner_shipping_id': partner_shipping_id,
            'partner_invoice_id':  partner_invoice_id,
            'note':                note,
            'order_line':          order_lines,
        })

        # تحويل لحالة "عرض سعر مرسل"
        order.sudo().action_quotation_sent()

        return request.redirect('/my/order/confirm/%d' % order.id)

    # ─── صفحة التأكيد ───────────────────────────────────────────────────────────

    @http.route('/my/order/confirm/<int:order_id>', type='http', auth='user', website=True)
    def portal_order_confirm(self, order_id, **kwargs):
        partner = request.env.user.partner_id
        order   = request.env['sale.order'].sudo().browse(order_id)

        if not order.exists() or order.partner_id.commercial_partner_id.id != partner.commercial_partner_id.id:
            return request.redirect('/my')

        return request.render('customer_portal_order.portal_order_confirm', {
            'order': order,
            'page_name': 'order_confirm',
        })

    # ─── بحث عن المنتجات (JSON) ──────────────────────────────────────────────────

    @http.route('/my/order/product/search', type='json', auth='user', website=True)
    def product_search(self, term='', **kwargs):
        if not term or len(term) < 2:
            return []

        domain = [
            ('sale_ok', '=', True),
            ('active', '=', True),
            '|',
            ('name', 'ilike', term),
            ('default_code', 'ilike', term),
        ]
        products = request.env['product.product'].sudo().search(domain, limit=12)

        return [{
            'id':        p.id,
            'name':      p.display_name,
            'code':      p.default_code or '',
            'price':     p.lst_price,
            'uom':       p.uom_id.name,
            'image_url': '/web/image/product.product/%d/image_128' % p.id,
        } for p in products]
