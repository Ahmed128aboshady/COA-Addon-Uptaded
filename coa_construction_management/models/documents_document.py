# -*- coding: utf-8 -*-
from odoo import models, fields

class DocumentsDocument(models.Model):
    _name = 'documents.document'
    _description = 'Document'

    name = fields.Char(string='Name')
    folder_id = fields.Many2one('documents.document', string='Folder')
    user_permission = fields.Char(string='User Permission')
