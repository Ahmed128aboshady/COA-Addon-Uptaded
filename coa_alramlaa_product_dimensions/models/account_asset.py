from odoo import models, fields, api


class AccountAsset(models.Model):
    _inherit = "account.asset"

    category_id = fields.Many2one(
        "asset.category",
        string="Asset Category"
    )

    linked_asset_ids = fields.Many2many(
        "account.asset",
        "asset_link_rel",
        "asset_id",
        "linked_asset_id",
        string="Linked Assets"
    )

    purchase_date = fields.Date(string="Purchase Date")
    purchase_price = fields.Float(string="Purchase Price")
    asset_code = fields.Char(string="Asset Code")

    dimension_length = fields.Float(string="Length (mm)")
    dimension_width = fields.Float(string="Width (mm)")
    dimension_thickness = fields.Float(string="Thickness (mm)")

    square_meter = fields.Float(
        string="Square Meter",
        compute="_compute_asset_dimensions",
        store=True,
        digits=(16, 4),
    )

    cubic_meter = fields.Float(
        string="Cubic Meter",
        compute="_compute_asset_dimensions",
        store=True,
        digits=(16, 6),
    )

    @api.depends("dimension_length", "dimension_width", "dimension_thickness")
    def _compute_asset_dimensions(self):
        for rec in self:
            length = rec.dimension_length or 0.0
            width = rec.dimension_width or 0.0
            thickness = rec.dimension_thickness or 0.0

            rec.square_meter = (length * width) / 1000000.0 if length and width else 0.0
            rec.cubic_meter = (length * width * thickness) / 1000000000.0 if length and width and thickness else 0.0