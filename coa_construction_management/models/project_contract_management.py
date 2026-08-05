# -*- coding: utf-8 -*-
""" Project Contract Management """
from odoo import api, fields, models, _


class ProjectContractManagement(models.Model):
    """ Project Contract Management """
    _name = 'project contract management'
    _description = 'Project Contract Management'
    
    name = fields.Char()
