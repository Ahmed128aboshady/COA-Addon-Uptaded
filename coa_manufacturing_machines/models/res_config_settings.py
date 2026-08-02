# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ═══════════════════════════════════════════════
    # Machine Accounts (Machine Costs)
    # ═══════════════════════════════════════════════
    machine_cost_account_id = fields.Many2one(
        'account.account',
        string='Machine Cost Account (Debit)',
        config_parameter='manufacturing_machines.machine_cost_account_id',
        domain=[('account_type', 'in', ['expense', 'asset_current'])],
    )

    # ═══════════════════════════════════════════════
    # Labor Accounts (Labor Costs)
    # ═══════════════════════════════════════════════
    labor_cost_account_id = fields.Many2one(
        'account.account',
        string='Labor Cost Account (Debit)',
        config_parameter='manufacturing_machines.labor_cost_account_id',
        domain=[('account_type', 'in', ['expense', 'asset_current'])],
    )

    # ═══════════════════════════════════════════════
    # Maintenance Accounts (Maintenance Costs)
    # ═══════════════════════════════════════════════
    maintenance_cost_account_id = fields.Many2one(
        'account.account',
        string='Maintenance Cost Account (Debit)',
        config_parameter='manufacturing_machines.maintenance_cost_account_id',
        domain=[('account_type', 'in', ['expense', 'asset_current'])],
    )

    # ═══════════════════════════════════════════════
    # Overhead Accounts (Overhead Costs)
    # ═══════════════════════════════════════════════
    overhead_cost_account_id = fields.Many2one(
        'account.account',
        string='Overhead Cost Account (Debit)',
        config_parameter='manufacturing_machines.overhead_cost_account_id',
        domain=[('account_type', 'in', ['expense', 'asset_current'])],
    )

    # ═══════════════════════════════════════════════
    # Contra Account + Journal (Contra + Journal)
    # ═══════════════════════════════════════════════
    contra_account_id = fields.Many2one(
        'account.account',
        string='Contra Account (Credit)',
        config_parameter='manufacturing_machines.contra_account_id',
        domain=[('account_type', 'in', ['liability_current', 'asset_current'])],
    )
    machine_journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        config_parameter='manufacturing_machines.machine_journal_id',
        domain=[('type', 'in', ['general'])],
    )
