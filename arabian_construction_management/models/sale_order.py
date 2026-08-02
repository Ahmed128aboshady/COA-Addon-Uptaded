from odoo import api, fields, models, _
from datetime import datetime

class SaleOrder(models.Model):
    """ inherit sale Order """

    _inherit = 'sale.order'

    construction_ids = fields.One2many('construction.project', 'sale_id', string="Construction Projects")

    construction_id = fields.Many2one('construction.project', string="Construction Project")

    construction_count = fields.Integer(string="Construction Count", compute="_compute_construction_count")
    project_name = fields.Char(string="Project Name")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if isinstance(vals, dict) and vals.get('name', _("New")) in [_("New"), "جديد"]:
                partner_id = vals.get('partner_id')
                vals['name'] = self._get_custom_sequence(partner_id)

        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)

        if 'partner_id' in vals:
            for order in self:
                partner_id = order.partner_id.id
                year_code = f"Q{str(fields.Date.today().year)[-2:]}"

                existing_customers = self.search([('name', 'like', f"{year_code}-%")])
                unique_partner_ids = list(set(existing_customers.mapped('partner_id.id')))

                if partner_id in unique_partner_ids:
                    customer_number = str(unique_partner_ids.index(partner_id) + 1).zfill(3)
                else:
                    customer_number = str(len(unique_partner_ids) + 1).zfill(3)

                last_order = self.search(
                    [('partner_id', '=', partner_id), ('name', 'like', f"{year_code}-{customer_number}/%")],
                    order="id desc",
                    limit=1
                )

                if last_order and '/' in last_order.name:
                    last_seq_number = int(last_order.name.split('/')[-1])
                    new_seq_number = str(last_seq_number + 1).zfill(2)
                else:
                    new_seq_number = "01"

                order.write({'name': f"{year_code}-{customer_number}/{new_seq_number}"})

        return res

    def _get_custom_sequence(self, partner_id):
        if not partner_id:
            return "Q25-000/00"

        last_order = self.env['sale.order'].search([
            ('partner_id', '=', partner_id)
        ], order='id desc', limit=1)

        if last_order and last_order.name:
            try:
                last_seq_number = int(last_order.name.split("/")[-1])
                order_number = str(last_seq_number + 1).zfill(2)
            except ValueError:
                order_number = "01"
        else:
            order_number = "01"

        existing_orders = self.env['sale.order'].search([], order='id asc')

        partner_index_map = {}
        customer_counter = 1

        for order in existing_orders:
            p_id = order.partner_id.id
            if p_id not in partner_index_map:
                partner_index_map[p_id] = str(customer_counter).zfill(3)
                customer_counter += 1

        customer_number = partner_index_map.get(partner_id, str(customer_counter).zfill(3))
        partner = self.env['res.partner'].browse(partner_id)
        customer_code = partner.partner_reference if partner.partner_reference else 'None'


        year_code = f"Q{str(fields.Date.today().year)[-2:]}"
        return f"{year_code}-{customer_code}/{order_number}"

    def action_create_con_project(self):
        for order in self:
            year_code = f"C{str(datetime.today().year)[-2:]}"

            # existing_projects = self.env['construction.project'].search([
            #     ('sale_id', '=', order.id)
            # ])
            # project_number = str(len(existing_projects) + 1).zfill(3)
            partner = order.partner_id
            customer_code = partner.partner_reference if partner.partner_reference else 'None'
            sequence_name = f"{year_code}-{customer_code}"
            project_vals = {
                'name': sequence_name,
                'project_name': order.project_name,
                'partner_id': order.partner_id.id,
                'sale_id': order.id,
                'sale': True,
            }
            self.env['construction.project'].create(project_vals)

        return True

    @api.depends('construction_ids')
    def _compute_construction_count(self):
        for order in self:
            order.construction_count = self.env['construction.project'].search_count([('sale_id', '=', order.id)])

    def action_view_construction_projects(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "construction.project",
            "domain": [('sale_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Construction Projects"),
            "view_mode": 'list,form',
        }




