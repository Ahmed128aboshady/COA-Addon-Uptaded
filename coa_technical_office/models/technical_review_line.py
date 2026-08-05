# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TechnicalReviewLine(models.Model):
    _name = 'technical.review.line'
    _description = 'Technical Review Line'
    _order = 'id asc'

    review_id = fields.Many2one(
        'technical.review',
        string='Review',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Sale Order Line',
        ondelete='set null',
        index=True,
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        related='sale_line_id.product_id',
        store=True,
        readonly=True,
        index=True,
    )
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        related='sale_line_id.product_id.product_tmpl_id',
        store=True,
        readonly=True,
    )
    product_qty = fields.Float(
        string='Quantity',
        related='sale_line_id.product_uom_qty',
        store=True,
        readonly=True,
    )
    product_uom = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        related='sale_line_id.product_uom_id',
        store=True,
        readonly=True,
    )

    # ── Dimension fields (from alramlaa_product_dimensions) ──────────────────
    dimension_length = fields.Float(
        string='Length (mm)',
        related='product_tmpl_id.dimension_length',
        store=False,
        readonly=True,
    )
    dimension_width = fields.Float(
        string='Width (mm)',
        related='product_tmpl_id.dimension_width',
        store=False,
        readonly=True,
    )
    dimension_thickness = fields.Float(
        string='Thickness (mm)',
        related='product_tmpl_id.dimension_thickness',
        store=False,
        readonly=True,
    )
    square_meter = fields.Float(
        string='Square Meter',
        related='product_tmpl_id.square_meter',
        store=False,
        readonly=True,
        digits=(16, 6),
    )
    cubic_meter = fields.Float(
        string='Cubic Meter',
        related='product_tmpl_id.cubic_meter',
        store=False,
        readonly=True,
        digits=(16, 9),
    )

    # ── BOM ──────────────────────────────────────────────────────────────────
    bom_id = fields.Many2one(
        'mrp.bom',
        string='Bill of Materials',
        domain="[('product_tmpl_id', '=', product_tmpl_id)]",
        copy=False,
    )

    # ── Status ───────────────────────────────────────────────────────────────
    line_state = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('reviewed', 'Reviewed'),
        ],
        string='Status',
        default='pending',
        required=True,
        index=True,
    )
    notes = fields.Text(string='Notes')

    # -------------------------------------------------------------------------
    # Actions — BOM management
    # -------------------------------------------------------------------------

    def action_create_bom(self):
        """Create an estimated mrp.bom for this product and open it."""
        self.ensure_one()
        if not self.product_tmpl_id:
            raise UserError(_('No product found on this line.'))
        if self.bom_id:
            raise UserError(
                _('A BOM is already linked to this line. Use "Open BOM" to edit it.')
            )
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_tmpl_id.id,
            'product_qty': 1.0,
            'is_estimated': True,
            'company_id': self.review_id.company_id.id,
        })
        self.bom_id = bom.id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bill of Materials — %s') % self.product_tmpl_id.name,
            'res_model': 'mrp.bom',
            'view_mode': 'form',
            'res_id': bom.id,
            'target': 'new',
        }

    def action_open_bom(self):
        """Open the linked BOM in a full form view."""
        self.ensure_one()
        if not self.bom_id:
            raise UserError(_('No BOM linked to this line. Use "Create BOM" first.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bill of Materials — %s') % self.product_tmpl_id.name,
            'res_model': 'mrp.bom',
            'view_mode': 'form',
            'res_id': self.bom_id.id,
            'target': 'new',
        }

    # -------------------------------------------------------------------------
    # Actions — Line status
    # -------------------------------------------------------------------------

    def action_mark_reviewed(self):
        """Mark this line as reviewed."""
        self.write({'line_state': 'reviewed'})

    def action_mark_pending(self):
        """Reset this line back to pending."""
        self.write({'line_state': 'pending'})
