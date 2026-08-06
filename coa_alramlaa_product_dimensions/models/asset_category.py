from odoo import models, fields


class AssetCategory(models.Model):
    _name = "asset.category"
    _description = "Asset Category"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(required=True)
    parent_id = fields.Many2one(
        "asset.category",
        string="Parent Category"
    )
    child_ids = fields.One2many(
        "asset.category",
        "parent_id",
        string="Child Categories"
    )
    parent_path = fields.Char(index=True)