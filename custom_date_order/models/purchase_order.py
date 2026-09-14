from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    confirmation_date = fields.Date(
        string='Confirmation Date',
        compute='_compute_confirmation_date',
        store=True
    )
    expected_arrival = fields.Date(
        string='Expected Arrival',
        compute='_compute_expected_arrival',
        store=True
    )
    order_deadline = fields.Date(
        string='Order Deadline',
        compute='_compute_order_deadline',
        store=True
    )

    @api.depends('date_approve','confirmation_date')
    def _compute_confirmation_date(self):
        for rec in self:
            rec.confirmation_date = rec.date_approve.date() if rec.date_approve else False

    @api.depends('date_planned','expected_arrival')
    def _compute_expected_arrival(self):
        for rec in self:
            rec.expected_arrival = rec.date_planned.date() if rec.date_planned else False

    @api.depends('date_order','order_deadline')
    def _compute_order_deadline(self):
        for rec in self:
            rec.order_deadline = rec.date_order.date() if rec.date_order else False