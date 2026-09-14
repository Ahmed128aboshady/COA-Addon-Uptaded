# -*- coding: utf-8 -*-
""" Cheque Management """
from odoo import api, fields, models, _

class IncomingCheque(models.Model):
    """ inherit Incoming Cheque """
    _inherit = 'incoming.cheque'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)

    @api.onchange('construction_project_id')
    def _onchange_construction_project_id(self):
        """ construction_project_id """
        self.project_name=self.construction_project_id.project_name
        self.project_number=self.construction_project_id.project_number

class OutgoingCheque(models.Model):
    """ inherit Outgoing Cheque """
    _inherit = 'outgoing.cheque'

    construction_project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)

    @api.onchange('construction_project_id')
    def _onchange_construction_project_id(self):
        """ construction_project_id """
        self.project_name=self.construction_project_id.project_name
        self.project_number=self.construction_project_id.project_number