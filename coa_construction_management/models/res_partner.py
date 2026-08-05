from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_reference = fields.Char(string="Partner Code", store=True)

    @api.model
    def create(self, vals):
        if not vals.get('partner_reference'):
            last_partner = self.env['res.partner'].search(
                [('partner_reference', '!=', False)],
                order='partner_reference desc',
                limit=1
            )
            next_number = int(
                last_partner.partner_reference) + 1 if last_partner and last_partner.partner_reference.isdigit() else 1
            vals['partner_reference'] = str(next_number).zfill(3)

        return super(ResPartner, self).create(vals)

    @api.model
    def _init_partner_references(self):
        partners = self.env['res.partner'].search([('partner_reference', '=', False)], order='id asc')

        last_partner = self.env['res.partner'].search(
            [('partner_reference', '!=', False)],
            order='partner_reference desc',
            limit=1
        )
        last_number = int(
            last_partner.partner_reference) if last_partner and last_partner.partner_reference.isdigit() else 0

        for partner in partners:
            last_number += 1
            partner.partner_reference = str(last_number).zfill(3)

    def init(self):
        self._init_partner_references()
