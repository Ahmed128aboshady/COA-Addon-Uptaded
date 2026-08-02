# -*- coding: utf-8 -*-
""" Detailed Bill Of Quantities """
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DetailedBillOfQuantities(models.Model):
    """ Detailed Bill Of Quantities """
    _name = 'detailed.bill.of.quantities'
    _description = 'Detailed Bill Of Quantities'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('send_to_assay', 'Send to Assay')
    ], string='Status', default='draft')
    name = fields.Char(default='New')
    construction_business_items_id = fields.Many2one(
        'construction.business.items')
    business_items_line_ids = fields.Many2many(
        'construction.business.items.line',
        'business_items_line_detailed_boq_rel',
    )
    project_id = fields.Many2one('construction.project')
    project_name = fields.Char(translate=True)
    project_number = fields.Char(translate=True)
    project_description = fields.Html(translate=True)
    project_type_id = fields.Many2one('construction.project.type')
    partner_id = fields.Many2one('res.partner', string="Customer")
    project_location = fields.Char(translate=True)
    date = fields.Date(default=fields.Date.today())
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    description = fields.Text(translate=True)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    quantity = fields.Float(default=1)
    bill_of_quantities_line_ids = fields.One2many('bill.of.quantities.line',
                                                  'detailed_bill_of_quantities_id')
    bill_quantities_labour_machines_ids = fields.One2many(
        'bill.quantities.labour.machines', 'detailed_bill_of_quantities_id')
    bill_quantities_overhead_ids = fields.One2many('bill.quantities.overhead',
                                                   'detailed_bill_of_quantities_id')

    total_material_cost = fields.Monetary(currency_field='currency_id',
                                          string="Total",
                                          compute='_compute_total_material_cost',
                                          store=True)
    total_labour_cost = fields.Monetary(currency_field='currency_id',
                                        string="Total",
                                        compute='_compute_total_labour_cost',
                                        store=True)
    total_overhead_cost = fields.Monetary(currency_field='currency_id',
                                          string="Total",
                                          compute='_compute_total_overhead_cost',
                                          store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    material_note = fields.Html()
    labour_note = fields.Html()
    overhead_note = fields.Html()

    margin = fields.Float(string="Margin%", digits=(16, 0))
    margin_amount = fields.Float(compute='_compute_margin_amount', store=True,
                                 digits=(16, 0))
    labour_margin_amount = fields.Float(compute='_compute_margin_amount',
                                        store=True, digits=(16, 0))
    overhead_margin_amount = fields.Float(string="OverHead Margin Amount",
                                          compute='_compute_margin_amount',
                                          store=True, digits=(16, 0))
    vat = fields.Float(string="Vat%", digits=(16, 0))
    material_vat_amount = fields.Float(compute='_compute_vat_amount',
                                       store=True, digits=(16, 0))
    labour_vat_amount = fields.Float(compute='_compute_vat_amount', store=True,
                                     digits=(16, 0))
    # overhead_vat_amount = fields.Float(string="OverHead Vat Amount",compute='_compute_vat_amount', store=True)
    brokerage_margin = fields.Float(string="Brokerage Margin%", digits=(16, 0))
    brokerage_margin_amount = fields.Float(
        compute='_compute_brokerage_margin_amount', store=True, digits=(16, 0))
    labour_brokerage_margin_amount = fields.Float(
        compute='_compute_brokerage_margin_amount',
        store=True, digits=(16, 0))
    overhead_brokerage_margin_amount = fields.Float(
        string="OverHead Brokerage Margin Amount",
        compute='_compute_brokerage_margin_amount',
        store=True, digits=(16, 0))

    additional_expenses = fields.Float(string="Additional Expenses%",
                                       digits=(16, 0))
    total_margin = fields.Float(digits=(16, 0))
    total_vat = fields.Float(digits=(16, 0))
    total_additional_expenses = fields.Float(digits=(16, 0))

    total_labour_margin = fields.Float(digits=(16, 0))
    total_labour_vat = fields.Float(digits=(16, 0))
    total_labour_additional_expenses = fields.Float(digits=(16, 0))

    item_total_cost = fields.Monetary(currency_field='currency_id',
                                      compute='_compute_item_total_cost',
                                      store=True, digits=(16, 0))
    item_total_margin = fields.Monetary(string="Total Margin ",
                                        currency_field='currency_id',
                                        compute='_compute_item_total_cost',
                                        store=True, digits=(16, 0))
    item_total_brokerage_margin = fields.Monetary(
        string="Total Brokerage Margin ", currency_field='currency_id',
        compute='_compute_item_total_cost',
        store=True, digits=(16, 0))
    item_total_vat = fields.Monetary(string="Total Vat ",
                                     currency_field='currency_id',
                                     compute='_compute_item_total_cost',
                                     store=True, digits=(16, 0))
    item_total_vat_margin = fields.Monetary(
        string="Total After Vat & Margin & Brokerage Margin",
        currency_field='currency_id',
        compute='_compute_item_total_cost',
        store=True, digits=(16, 0))
    boq_cost_estimation_id = fields.Many2one('boq.cost.estimation')
    item_code = fields.Char()
    material_total_margin_vat = fields.Float(
        string="Total after Vat & Margin & Brokerage Margin",
        compute='_compute_total_margin_vat', store=True, digits=(16, 0))
    labour_total_margin_vat = fields.Float(
        string="Total after Vat & Margin & Brokerage Margin",
        compute='_compute_total_margin_vat', store=True, digits=(16, 0))
    overhead_total_margin_vat = fields.Float(
        string="Total after Margin & Brokerage Margin",
        compute='_compute_total_margin_vat', store=True, digits=(16, 0))
    purchase_order_ids = fields.One2many(
        'purchase.order',
        'detailed_boq_id',
        string="Purchase Orders"
    )

    purchase_order_count = fields.Integer(
        string="Purchase Orders",
        compute="_compute_purchase_order_count"
    )
    journal_entry_id = fields.Many2one('account.move', string="Journal Entry")
    move_ids = fields.Many2many(
        'account.move'
    )
    move_count = fields.Integer(
        compute='_compute_move_count', store=True
    )
    not_journal_created = fields.Boolean(
        compute='_compute_not_journal_created', store=True
    )
    credit_account_id = fields.Many2one(
        'account.account'
    )
    not_create_purchase = fields.Boolean(
        compute='_compute_not_create_purchase', store=True
    )

    @api.depends('bill_of_quantities_line_ids.create_purchase')
    def _compute_not_create_purchase(self):
        """ Compute not_create_purchase value """
        for rec in self:
            rec.not_create_purchase = any(
                not n.create_purchase for n in
                rec.bill_of_quantities_line_ids)

    @api.depends('move_ids')
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.move_ids.ids)

    @api.depends('bill_quantities_overhead_ids.journal_created',
                 'bill_quantities_labour_machines_ids.journal_created')
    def _compute_not_journal_created(self):
        """ Compute not_journal_created value """
        for rec in self:
            rec.not_journal_created = any(
                not n.journal_created for n in
                rec.bill_quantities_overhead_ids) or any(
                not n.journal_created for n in
                rec.bill_quantities_labour_machines_ids)

    detailed_boq_type = fields.Selection(
        [('single_order', 'Single Order'), ('multi_orders', 'Multi Orders')],
        string="Detailed BOQ Type", default='single_order')

    def action_view_journal_entry(self):
        """ :return Account Move action """
        self.ensure_one()
        recs = self.mapped('move_ids')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'name': _('Journal Entry'),
            'view_mode': 'list,form',
            'context': {'form_view_initial_mode': 'edit', },
            'domain': [('id', 'in', recs.ids)],
            'views': [(False, 'list'), (False, 'form')],
        }

    def action_create_journal_entry(self):
        self.ensure_one()

        journal = self.env['account.journal'].search([('code', '=', 'MISC')],
                                                     limit=1)
        if not journal:
            raise UserError(
                _("Please create a journal with code 'MISC' (Miscellaneous Operations)."))

        bill_quantities_overhead_ids = self.bill_quantities_overhead_ids.filtered(
            lambda r: not r.journal_created)
        if bill_quantities_overhead_ids:
            self.create_bill_quantities_overhead_move(
                bill_quantities_overhead_ids, journal)
        bill_quantities_labour_machines_ids = self.bill_quantities_labour_machines_ids.filtered(
            lambda r: not r.journal_created)
        if bill_quantities_labour_machines_ids:
            self.create_bill_quantities_labour_machines_move(
                bill_quantities_labour_machines_ids, journal)

    def create_bill_quantities_overhead_move(self, bill_quantities_overhead_ids,
                                             journal):
        lines = []
        for line in bill_quantities_overhead_ids:
            amount = line.subtotal
            if not amount:
                continue

            lines.append((0, 0, {
                'name': line.product_id.name or line.name or 'Overhead Cost',
                'account_id': line.account_id.id,
                'partner_id': line.partner_id.id,
                'debit': amount,
                'credit': 0.0,
            }))

            lines.append((0, 0, {
                'name': 'Credit Entry',
                'account_id': line.account_id.id,
                'debit': 0.0,
                'credit': amount,
            }))
        move = self.env['account.move'].create({
            'journal_id': journal.id,
            'date': fields.Date.today(),
            'ref': self.name or 'Overhead Journal Entry',
            'line_ids': lines,
        })
        self.bill_quantities_overhead_ids.filtered(
            lambda r: not r.journal_created).write({'journal_created': True})
        self.write({'move_ids': [(4, move.id)]})

    def create_bill_quantities_labour_machines_move(self,
                                                    bill_quantities_labour_machines_ids,
                                                    journal):
        if self.credit_account_id:
            lines = []
            for line in bill_quantities_labour_machines_ids:
                amount = line.subtotal
                if not amount:
                    continue

                lines.append((0, 0, {
                    'name': line.product_id.name or line.name,
                    'account_id': line.account_id.id,
                    'debit': amount,
                    'credit': 0.0,
                }))
            lines.append((0, 0, {
                'name': 'Credit Entry',
                'account_id': self.credit_account_id.id,
                'debit': 0.0,
                'credit': sum(
                    bill_quantities_labour_machines_ids.mapped('subtotal')),
            }))

            move = self.env['account.move'].create({
                'journal_id': journal.id,
                'date': fields.Date.today(),
                'ref': self.name or 'Overhead Journal Entry',
                'line_ids': lines,
            })
            self.bill_quantities_labour_machines_ids.filtered(
                lambda r: not r.journal_created).write(
                {'journal_created': True})
            self.write({'move_ids': [(4, move.id)]})

    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        for rec in self:
            rec.purchase_order_count = len(rec.purchase_order_ids)

    def action_view_purchase_orders(self):
        self.ensure_one()
        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('detailed_boq_id', '=', self.id)],
            'context': {'default_detailed_boq_id': self.id},
        }

    def action_create_purchase_orders(self):
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']

        for record in self:
            grouped_lines = {}

            for line in record.bill_of_quantities_line_ids.filtered(
                    lambda r: not r.create_purchase):
                if not line.partner_id:
                    raise UserError(
                        "Please set a Vendor on all BOQ lines before creating purchase orders.")

                partner = line.partner_id
                if partner not in grouped_lines:
                    grouped_lines[partner] = []
                grouped_lines[partner].append(line)

            for vendor, lines in grouped_lines.items():
                po_lines = []
                for line in lines:
                    if not line.product_id or not line.uom_id or not line.quantity:
                        raise UserError(
                            "Missing product, quantity, or UOM in some lines.")

                    po_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.product_id.display_name,
                        'product_uom': line.uom_id.id,
                        'product_qty': line.quantity,
                        'price_unit': line.unit_price,
                    }))

                po = PurchaseOrder.create({
                    'partner_id': vendor.id,
                    'order_line': po_lines,
                    'origin': record.name or 'Construction Business Item',
                    'construction_project_id': record.project_id.id,
                    'project_name': record.project_name,
                    'project_number': record.project_number,
                    'detailed_boq_id': record.id,
                })
            self.bill_of_quantities_line_ids.filtered(
                lambda r: not r.create_purchase).write(
                {'create_purchase': True})

            # Uncomment if you want to confirm the order automatically
            # po.button_confirm()

    def send_to_assay(self):
        """ Pricing Done """
        for rec in self:
            items = [(0, 0, {
                'name': rec.item_code,
                'business_item_id': rec.business_item_id.id,
                'detailed_bill_of_quantities_id': rec.id,
                'business_items_types_id': rec.business_items_types_id.id,
                'description': rec.description,
                'uom_id': rec.uom_id.id,
                'quantity': rec.quantity,
                'rate': rec.item_total_cost,
                'currency_id': rec.currency_id.id,
                'total_cost': rec.item_total_cost * rec.quantity
            })]

            if rec.boq_cost_estimation_id:
                rec.boq_cost_estimation_id.write({

                    'boq_cost_estimation_ids': items
                })
            rec.state = 'send_to_assay'

    @api.depends('total_material_cost', 'total_labour_cost',
                 'total_overhead_cost', 'vat', 'margin', 'brokerage_margin')
    def _compute_item_total_cost(self):
        """ Compute item_total_cost value """
        for rec in self:
            rec.item_total_cost = int(
                rec.total_material_cost + rec.total_labour_cost + rec.total_overhead_cost
            )
            rec.item_total_margin = int(
                rec.margin_amount + rec.labour_margin_amount + rec.overhead_margin_amount
            )
            rec.item_total_brokerage_margin = int(
                rec.brokerage_margin_amount + rec.labour_brokerage_margin_amount + rec.overhead_brokerage_margin_amount
            )
            rec.item_total_vat = int(
                rec.material_vat_amount + rec.labour_vat_amount
            )
            rec.item_total_vat_margin = int(
                rec.material_total_margin_vat + rec.labour_total_margin_vat + rec.overhead_total_margin_vat
            )

    @api.depends('bill_of_quantities_line_ids', 'total_material_cost', 'margin',
                 'total_labour_cost', 'total_overhead_cost')
    def _compute_margin_amount(self):
        """ Compute total_margin value """
        for rec in self:
            rec.margin_amount = rec.margin * rec.total_material_cost / 100
            rec.labour_margin_amount = rec.margin * rec.total_labour_cost / 100
            rec.overhead_margin_amount = rec.margin * rec.total_overhead_cost / 100

    @api.depends('bill_of_quantities_line_ids', 'total_material_cost',
                 'brokerage_margin',
                 'total_labour_cost', 'total_overhead_cost')
    def _compute_brokerage_margin_amount(self):
        """ Compute total_margin value """
        for rec in self:
            rec.brokerage_margin_amount = rec.brokerage_margin * rec.total_material_cost / 100
            rec.labour_brokerage_margin_amount = rec.brokerage_margin * rec.total_labour_cost / 100
            rec.overhead_brokerage_margin_amount = rec.brokerage_margin * rec.total_overhead_cost / 100

    @api.depends('total_material_cost', 'margin_amount', 'material_vat_amount',
                 'total_labour_cost', 'labour_margin_amount',
                 'labour_vat_amount', 'total_overhead_cost',
                 'overhead_margin_amount', 'margin', 'brokerage_margin', 'vat')
    def _compute_total_margin_vat(self):
        """ Compute total_margin_vat value """
        for rec in self:
            rec.material_total_margin_vat = rec.total_material_cost + rec.margin_amount + rec.brokerage_margin + rec.material_vat_amount
            rec.labour_total_margin_vat = rec.total_labour_cost + rec.labour_margin_amount + rec.labour_brokerage_margin_amount + rec.labour_vat_amount
            rec.overhead_total_margin_vat = rec.total_overhead_cost + rec.overhead_margin_amount + rec.overhead_brokerage_margin_amount

    @api.depends('bill_of_quantities_line_ids', 'total_material_cost',
                 'total_labour_cost', 'vat', 'total_overhead_cost')
    def _compute_vat_amount(self):
        """ Compute vat_amount value """
        for rec in self:
            rec.material_vat_amount = rec.vat * rec.total_material_cost / 100
            rec.labour_vat_amount = rec.vat * rec.total_labour_cost / 100
            # rec.overhead_vat_amount = rec.vat * rec.total_overhead_cost / 100

    @api.depends('bill_of_quantities_line_ids')
    def _compute_total_material_cost(self):
        """ Compute total_material_cost value """
        for rec in self:
            rec.total_material_cost = 0
            for b in rec.bill_of_quantities_line_ids:
                rec.total_material_cost += b.subtotal

    @api.depends('bill_quantities_labour_machines_ids')
    def _compute_total_labour_cost(self):
        """ Compute total_labour_cost value """
        for rec in self:
            rec.total_labour_cost = 0
            for b in rec.bill_quantities_labour_machines_ids:
                rec.total_labour_cost += b.subtotal

    @api.depends('bill_quantities_overhead_ids')
    def _compute_total_overhead_cost(self):
        """ Compute total_overhead_cost value """
        for rec in self:
            rec.total_overhead_cost = 0
            for b in rec.bill_quantities_overhead_ids:
                rec.total_overhead_cost += b.subtotal

    def confirm(self):
        """ Confirm """
        for rec in self:
            rec.state = 'confirm'

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'detailed.bill.of.quantities') or '/'
        return super(DetailedBillOfQuantities, self).create(vals)


class BillOfQuantitiesLine(models.Model):
    """ Bill Of Quantities Line """
    _name = 'bill.of.quantities.line'
    _description = 'Bill Of Quantities Line'

    detailed_bill_of_quantities_id = fields.Many2one(
        'detailed.bill.of.quantities')
    productivity_per_unit_item = fields.Float(
        string="Productivity per unit item")
    construction_business_id = fields.Many2one(
        'construction.business.items.line')
    product_id = fields.Many2one('product.product')
    name = fields.Char(string="Description")
    quantity = fields.Float(string="Planned Quantity")
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    unit_price = fields.Monetary(currency_field='currency_id', digits=(16, 0))
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    subtotal = fields.Monetary(currency_field='currency_id', digits=(16, 0))
    cost_per_item_unit = fields.Monetary(currency_field='currency_id',
                                         digits=(16, 0))
    damaged_percentage = fields.Float(string="Damaged Percentage(%)",
                                      digits=(16, 0))
    partner_id = fields.Many2one('res.partner', string='Vendor', )
    business_item_id = fields.Many2one('detailed.business.items')
    business_items_types_id = fields.Many2one('business.items.types')
    description = fields.Text(translate=True)
    item_code = fields.Char()
    create_purchase = fields.Boolean()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.unit_price = rec.product_id.lst_price
            rec.uom_id = rec.product_id.uom_id.id

    @api.onchange('quantity', 'unit_price', 'damaged_percentage',
                  'productivity_per_unit_item')
    def _onchange_subtotal(self):
        """ subtotal """
        for rec in self:
            damaged_percentage = rec.damaged_percentage * rec.quantity / 100
            rec.quantity += damaged_percentage
            rec.subtotal = rec.quantity * rec.unit_price
            if rec.productivity_per_unit_item > 0 and rec.subtotal > 0:
                rec.cost_per_item_unit = rec.subtotal / rec.productivity_per_unit_item


class BillQuantitiesLabourMachines(models.Model):
    """ Bill Quantities Labour Machines """
    _name = 'bill.quantities.labour.machines'
    _description = 'Bill Quantities Labour Machines'

    name = fields.Char(default="New", string="name")
    # code = fields.Char(default="New", string="Code")
    # display_type = fields.Selection([
    #     ('line_section', 'Section'),
    #     ('line_note', 'Note')
    # ], string='Line Type', default=False)
    construction_business_id = fields.Many2one(
        'construction.business.items.line')

    detailed_bill_of_quantities_id = fields.Many2one(
        'detailed.bill.of.quantities')
    productivity_per_unit_item = fields.Float(
        string="Productivity per unit item/day")
    product_id = fields.Many2one('product.product')
    description = fields.Char(string="Description")
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    unit_price = fields.Monetary(currency_field='currency_id', digits=(16, 0))
    subtotal = fields.Monetary(currency_field='currency_id',
                               related='paid_amount_worker')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    cost_per_item_unit = fields.Monetary(currency_field='currency_id',
                                         digits=(16, 0))
    the_date = fields.Date(
        string="التاريخ",
        default=fields.Date.context_today,
    )
    worker_name = fields.Char(string="العامل")
    boq_item_name = fields.Char(string="اسم البند")

    total_amount_worker = fields.Monetary(string="إجمالي مستحقات العامل",
                                          currency_field='currency_id')
    paid_amount_worker = fields.Monetary(string="المدفوع للعامل",
                                         currency_field='currency_id')
    remaining_amount_worker = fields.Monetary(string="المتبقي للعامل",
                                              compute="_compute_remaining_amount_worker",
                                              store=True,
                                              currency_field='currency_id')
    working_hours = fields.Float()
    account_id = fields.Many2one(
        'account.account'
    )
    journal_created = fields.Boolean()

    @api.depends('total_amount_worker', 'paid_amount_worker')
    def _compute_remaining_amount_worker(self):
        for record in self:
            record.remaining_amount_worker = (
                                                     record.total_amount_worker or 0.0) - (
                                                     record.paid_amount_worker or 0.0)

    @api.onchange('unit_price', 'productivity_per_unit_item')
    def _onchange_subtotal(self):
        """ subtotal """
        for rec in self:
            rec.subtotal = rec.working_hours * rec.unit_price
            if rec.productivity_per_unit_item > 0 and rec.subtotal > 0:
                rec.cost_per_item_unit = rec.subtotal / rec.productivity_per_unit_item

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.unit_price = rec.product_id.lst_price
            rec.uom_id = rec.product_id.uom_id.id

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'bill.quantities.labour.machines') or '/'
        return super(BillQuantitiesLabourMachines, self).create(vals)


class BillQuantitiesOverhead(models.Model):
    """ Bill Quantities Overhead """
    _name = 'bill.quantities.overhead'
    _description = 'Bill Quantities Overhead'

    construction_business_id = fields.Many2one(
        'construction.business.items.line')
    detailed_bill_of_quantities_id = fields.Many2one(
        'detailed.bill.of.quantities')
    productivity_per_unit_item = fields.Float(
        string="Productivity per unit item")
    product_id = fields.Many2one('product.product')
    name = fields.Char(string="Description")
    quantity = fields.Float()
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    unit_price = fields.Monetary(currency_field='currency_id', digits=(16, 0))
    currency_id = fields.Many2one('res.currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    subtotal = fields.Monetary(currency_field='currency_id', digits=(16, 0))
    cost_per_item_unit = fields.Monetary(currency_field='currency_id',
                                         digits=(16, 0))
    partner_id = fields.Many2one('res.partner', string="Partner")
    account_id = fields.Many2one('account.account', string="Account",
                                 required=True)
    journal_created = fields.Boolean()

    @api.onchange('quantity', 'unit_price', 'productivity_per_unit_item')
    def _onchange_subtotal(self):
        """ subtotal """
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price
            if rec.productivity_per_unit_item > 0 and rec.subtotal > 0:
                rec.cost_per_item_unit = rec.subtotal / rec.productivity_per_unit_item

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.unit_price = rec.product_id.lst_price
            rec.uom_id = rec.product_id.uom_id.id
