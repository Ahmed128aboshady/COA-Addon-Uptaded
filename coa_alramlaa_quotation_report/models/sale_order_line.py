# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Section type for grouping (Furniture / Joinery)
    line_section_type = fields.Selection([
        ('furniture', 'Furniture / أثاث'),
        ('joinery', 'Joinery / نجارة'),
        ('other', 'Other / أخرى'),
    ], string='Section Type / نوع القسم', default='furniture')

    # Key materials / finish field
    key_materials = fields.Text(
        string='Key Materials & Finish / المواد والتشطيب',
        help='Describe the key materials, finish, and specifications'
    )

    # Dimensions field
    dimensions = fields.Char(
        string='Dimensions WxDxH / الأبعاد',
        help='e.g. 45 x 50 x 50 cm'
    )

    # Item number shown in report
    item_no = fields.Integer(
        string='Item No. / رقم البند',
        help='Sequential item number for the report'
    )

    # Product image (related from product)
    image = fields.Binary(
        string='Image / الصورة',
        related='product_id.image_128',
        readonly=True,
        store=False,
    )

    # Unit field override display (already exists, but add report label)
    report_unit = fields.Char(
        string='Unit (Report) / الوحدة',
        help='Unit label for the report e.g. PCS, SET, LS, M2, SM',
        default='PCS'
    )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Project Summary shown on quotation
    quotation_summary = fields.Text(
        string='Summary / الملخص',
        help='Short description or scope of work shown on the printed quotation',
    )

    # Follow-up person
    follow_up_person = fields.Char(
        string='Follow Up / المتابعة',
        help='Name of the follow-up contact person'
    )

    # Secondary contact number
    contact_number_2 = fields.Char(
        string='Contact Number 2 / رقم التواصل 2',
    )

    # Notes for report footer
    report_notes = fields.Text(
        string='Report Notes / ملاحظات التقرير',
        default='ALL DOORS WITHOUT HARDWARE / جميع الأبواب بدون أقفال',
    )

    # Payment terms text (free text override for report)
    payment_terms_detail = fields.Text(
        string='Payment Terms Detail / تفاصيل شروط الدفع',
        default=(
            "20% Down payment / دفعة مقدمة\n"
            "20% After shop drawing approval / بعد اعتماد المخططات التنفيذية\n"
            "30% Material insurance / تأمين مواد\n"
            "20% Installation / عند التركيب\n"
            "10% Retention / نسبة الضمان المحتجزة"
        ),
    )

    # Delivery terms
    delivery_terms = fields.Char(
        string='Delivery Terms / شروط التسليم',
        default='3 Months / 3 أشهر',
    )

    # Manual summary lines (independent from order_line)
    summary_line_ids = fields.One2many(
        'alramlaa.summary.line',
        'order_id',
        string='Summary Lines / أسطر الملخص',
    )

    # Terms and Conditions (free text for print)
    terms_conditions = fields.Text(
        string='Terms & Conditions / الشروط والأحكام',
        default=(
            "1. Prices are valid for 30 days from the date of this quotation.\n"
            "2. Delivery within agreed timeline after receipt of deposit.\n"
            "3. Any additional works not mentioned above will be quoted separately.\n"
            "4. All items are subject to final site measurements.\n"
            "5. Warranty: 1 year on workmanship."
        ),
    )

    def _get_furniture_lines(self):
        """Return lines classified as Furniture"""
        return self.order_line.filtered(
            lambda l: l.line_section_type == 'furniture' and not l.display_type
        )

    def _get_joinery_lines(self):
        """Return lines classified as Joinery"""
        return self.order_line.filtered(
            lambda l: l.line_section_type == 'joinery' and not l.display_type
        )
