# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CommissionRate(models.Model):
    _name = 'commission.rate'
    _description = 'نسبة العمولة حسب تاج العميل'
    _order = 'sequence, id'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    customer_tag_id = fields.Many2one(
        'res.partner.category',
        string='Customer Tag',
        required=True,
        ondelete='restrict',
    )
    commission_rate = fields.Float(
        string='Commission Rate %',
        required=True,
        digits=(5, 4),
        help='Enter the rate as a percentage, e.g. 1.5 means 1.5%',
    )
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        (
            'unique_tag',
            'UNIQUE(customer_tag_id)',
            'This tag already exists! Each tag must have only one commission rate.',
        ),
        (
            'positive_rate',
            'CHECK(commission_rate >= 0)',
            'The commission rate must be zero or greater.',
        ),
    ]

    @api.depends('customer_tag_id', 'commission_rate')
    def _compute_name(self):
        for rec in self:
            if rec.customer_tag_id:
                rec.name = f"{rec.customer_tag_id.name} — {rec.commission_rate}%"
            else:
                rec.name = _('New')

    def compute_commission(self, net_sales):
        """Calculate commission based on net sales"""
        self.ensure_one()
        return net_sales * (self.commission_rate / 100.0)
