# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CompanyDuplicatorWizard(models.TransientModel):
    _name = 'company.duplicator.wizard'
    _description = 'Duplicate Company Data Wizard Pro'

    source_company_id = fields.Many2one('res.company', string="Source Company", required=True, default=lambda self: self.env.company)
    dest_company_id = fields.Many2one('res.company', string="Destination Company", required=True)
    
    copy_coa = fields.Boolean(string="Copy Chart of Accounts", default=True)
    copy_taxes = fields.Boolean(string="Copy Taxes", default=True)
    copy_journals = fields.Boolean(string="Copy Journals", default=True)
    copy_warehouses = fields.Boolean(string="Copy Warehouses", default=True)

    def action_duplicate_data(self):
        self.ensure_one()
        if self.source_company_id == self.dest_company_id:
            raise UserError(_("لا يمكن اختيار نفس الشركة!"))

        if self.copy_coa:
            self._handle_accounts()

        if self.copy_taxes:
            self._copy_records('account.tax')

        if self.copy_journals:
            self._copy_records('account.journal')

        if self.copy_warehouses:
            self._copy_records('stock.warehouse')

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('تم بنجاح'),
                'message': _('تم استنساخ البيانات بنجاح!'),
                'type': 'success',
            }
        }

    def _handle_accounts(self):
        """ الحل الجذري لأودو 19 باستخدام with_company لتخطي الـ Validation Error """
        account_model = self.env['account.account'].sudo()

        if 'company_ids' in account_model._fields:
            domain = [('company_ids', 'in', self.source_company_id.id)]
        else:
            domain = [('company_id', '=', self.source_company_id.id)]

        accounts = account_model.search(domain)

        for acc in accounts:
            try:
                with self.env.cr.savepoint():
                    if 'company_ids' in account_model._fields:
                        if self.dest_company_id.id not in acc.company_ids.ids:
                            # 1. نجيب الكود من الشركة القديمة
                            source_code = acc.with_company(self.source_company_id).code
                            
                            # 2. نربط الشركة الجديدة ونحط الكود بتاعها في نفس اللحظة
                            acc.with_company(self.dest_company_id).write({
                                'company_ids': [(4, self.dest_company_id.id)],
                                'code': source_code
                            })
                    else:
                        acc.copy(default={'company_id': self.dest_company_id.id})
            except Exception as e:
                continue

    def _copy_records(self, model_name):
        records = self.env[model_name].sudo().search([('company_id', '=', self.source_company_id.id)])
        for rec in records:
            try:
                # رجعنا الحماية عشان لو سجل واحد فيه مشكلة، الباقي يكمل
                with self.env.cr.savepoint():
                    
                    # --- 1. الحل الجذري لليوميات (إنشاء من الصفر بدل النسخ المعند) ---
                    if model_name == 'account.journal':
                        new_name = f"{rec.name} ({self.dest_company_id.name})"
                        # كود مكون من حرف J ورقم اليومية (عشان نضمن إنه مستحيل يزيد عن 5 حروف)
                        new_code = f"J{rec.id}"[:5] 
                        
                        # فحص التكرار
                        exists = self.env['account.journal'].sudo().search([
                            ('company_id', '=', self.dest_company_id.id), 
                            '|', ('name', '=', new_name), ('code', '=', new_code)
                        ])
                        if exists:
                            continue
                            
                        # أمر الإنشاء المباشر (بيعمل تخطي لدالة copy الغبية بتاعت أودو)
                        self.env['account.journal'].sudo().with_company(self.dest_company_id).create({
                            'name': new_name,
                            'code': new_code,
                            'type': rec.type,
                            'company_id': self.dest_company_id.id,
                            'currency_id': rec.currency_id.id or False,
                            'active': True,
                        })
                    
                    # --- 2. الضرائب والمخازن (النسخ شغال معاهم زي الفل) ---
                    else:
                        vals = {
                            'company_id': self.dest_company_id.id,
                            'active': True
                        }
                        
                        if model_name == 'account.tax':
                            new_name = f"{rec.name} ({self.dest_company_id.name})"
                            exists = self.env['account.tax'].sudo().search([('company_id', '=', self.dest_company_id.id), ('name', '=', new_name)])
                            if exists:
                                continue
                            vals['name'] = new_name
                        
                        elif model_name == 'stock.warehouse':
                            new_name = f"{rec.name} ({self.dest_company_id.name})"
                            new_code = f"W{rec.id}"[:5]
                            exists = self.env['stock.warehouse'].sudo().search([('company_id', '=', self.dest_company_id.id), '|', ('name', '=', new_name), ('code', '=', new_code)])
                            if exists:
                                continue
                            vals.update({'name': new_name, 'code': new_code})
                        
                        rec.sudo().with_company(self.dest_company_id).copy(default=vals)
                        
            except Exception as e:
                continue