from odoo import models, api
from datetime import date


class PartnerStatementReport(models.AbstractModel):
    _name = 'report.partner_statement.partner_statement_template'
    _description = 'Partner Statement Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data:
            data = {}

        date_from    = data.get('date_from')
        date_to      = data.get('date_to')
        all_accounts = data.get('all_accounts', False)
        account_id   = data.get('account_id', False)
        partner_id   = data.get('partner_id')
        partner_name = data.get('partner_name', '')
        account_name = data.get('account_name', '')

        MoveLine = self.env['account.move.line']

        # ── Base domain ──────────────────────────────────────────────
        base_domain = [
            ('partner_id', '=', partner_id),
            ('parent_state', '=', 'posted'),
            ('display_type', 'not in', ['line_section', 'line_note']),
        ]
        if not all_accounts and account_id:
            base_domain.append(('account_id', '=', account_id))

        # ── Opening balance (lines BEFORE date_from) ──────────────────
        opening_domain = base_domain + [('date', '<', date_from)]
        opening_lines  = MoveLine.search(opening_domain)
        opening_balance = sum(opening_lines.mapped('debit')) - sum(opening_lines.mapped('credit'))

        # ── Period lines ──────────────────────────────────────────────
        period_domain = base_domain + [
            ('date', '>=', date_from),
            ('date', '<=', date_to),
        ]
        period_lines = MoveLine.search(period_domain, order='date asc, id asc')

        # ── Build lines list ──────────────────────────────────────────
        lines = []
        running_balance = opening_balance
        total_debit  = 0.0
        total_credit = 0.0

        # Opening balance row
        lines.append({
            'date':        '',
            'journal':     '',
            'ref':         '',
            'label':       'Opening Balance / الرصيد الافتتاحي',
            'match':       '',
            'debit':       0.0,
            'credit':      0.0,
            'balance':     opening_balance,
            'is_opening':  True,
        })

        for ml in period_lines:
            running_balance += ml.debit - ml.credit
            total_debit     += ml.debit
            total_credit    += ml.credit

            lines.append({
                'date':       ml.date,
                'journal':    ml.move_id.name or '',
                'ref':        ml.ref or ml.move_id.ref or '',
                'label':      ml.name or ml.move_id.payment_reference or '',
                'match':      ml.matching_number or '',
                'debit':      ml.debit,
                'credit':     ml.credit,
                'balance':    running_balance,
                'is_opening': False,
            })

        # Total row
        lines.append({
            'date':        '',
            'journal':     '',
            'ref':         '',
            'label':       'Total / الإجمالي',
            'match':       '',
            'debit':       total_debit,
            'credit':      total_credit,
            'balance':     running_balance,
            'is_total':    True,
            'is_opening':  False,
        })

        return {
            'doc_ids':      docids,
            'doc_model':    'partner.statement.wizard',
            'data':         data,
            'lines':        lines,
            'date_from':    date_from,
            'date_to':      date_to,
            'partner_name': partner_name,
            'account_name': account_name,
            'company':      self.env.company,
        }
