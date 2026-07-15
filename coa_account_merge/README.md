# COA Account Merge

<p align="center">
  <img src="coa_account_merge/static/description/icon.png" width="120" alt="COA Account Merge Icon"/>
</p>

<p align="center">
  <strong>Safely merge two or more GL accounts in Odoo 18 — all journal items and every database reference move to the destination account automatically.</strong>
</p>

<p align="center">
  <a href="https://wa.me/201013907174">
    <img src="https://img.shields.io/badge/Support-WhatsApp-25d366?logo=whatsapp&style=for-the-badge" alt="WhatsApp Support"/>
  </a>
  <img src="https://img.shields.io/badge/Odoo-18.0-blueviolet?style=for-the-badge&logo=odoo" alt="Odoo 18"/>
  <img src="https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge" alt="License LGPL-3"/>
</p>

---

## Overview

**COA Account Merge** adds a *"Merge Accounts"* action to Odoo's Chart of Accounts list view — similar to the native Contacts merge — but for GL accounts.

Select 2+ accounts, pick a destination account, and the module will:

- Repoint **all journal items** (`account.move.line`) to the destination.
- Update **every foreign-key reference** in the database (journals, taxes, products, partners, reconciliation models, fiscal positions, assets, etc.) using a generic FK scan.
- Handle **company-dependent (`jsonb`) fields** (e.g. partner receivable/payable accounts, product income/expense accounts) — something a plain FK scan cannot reach.
- **Archive** the source accounts (not delete) to keep the chart clean while remaining reversible from the archived filter.

---

## Features

| Feature | Details |
|---|---|
| GL Account Merge | All `account.move.line` repointed via direct SQL |
| Full Reference Update | Generic FK scan across all database tables |
| Company-Dependent Fields | jsonb field handling (Odoo 17+/18) |
| Source Account Archival | Safe archival, no deletion |
| Wizard UI | Simple action from Chart of Accounts list view |
| Arabic Language Support | Full Arabic translation included |
| Safety Guards | Company scope, type, and hash checks |

---

## Safety Guards

The merge is blocked if any of the following conditions are not met:

- **Permission**: Only users in the `Accounting Administrator` group can run the merge.
- **Company Scope**: All selected accounts must share the same company (or company set in multi-company).
- **Account Type**: Accounts must have the same type, unless *"Allow Different Types"* is explicitly checked.
- **Hashed Entries**: The merge is blocked if any journal item on a source account belongs to a hashed (inalterable) entry.
- **Reconcilable**: If any source account is reconcilable, the destination is made reconcilable automatically so existing reconciliations remain valid.

> ⚠️ **WARNING**: This action **cannot be undone**. Always take a database backup before merging accounts.

---

## Installation

### Option 1 — Manual (Recommended for testing)

1. Download or clone this repository.
2. Copy the `coa_account_merge` folder to your Odoo `addons` path.
3. Restart the Odoo server.
4. Enable **Developer Mode** in Odoo settings.
5. Go to **Apps → Update Apps List**.
6. Search for **COA Account Merge** and click **Install**.

### Option 2 — Via Odoo Apps Store

Available on the Odoo Apps marketplace:  
🔗 [apps.odoo.com](https://apps.odoo.com)

---

## Usage

1. Go to **Accounting → Configuration → Chart of Accounts**.
2. Switch to **List View**.
3. Select 2 or more accounts you want to merge.
4. Click **Action → Merge Accounts**.
5. In the wizard, choose the **Destination Account**.
6. Optionally check **Allow Different Types** if needed.
7. Review the **Journal Items to Move** count.
8. Click **Merge Accounts** and confirm.

---

## Compatibility

| Parameter | Value |
|---|---|
| Odoo Version | 18.0 |
| Module Version | 18.0.1.0.0 |
| Dependencies | `account` |
| License | LGPL-3 |
| Database | PostgreSQL (direct SQL) |
| Languages | English, Arabic |

---

## Support & Contact

For installation help, customization requests, or any questions:

📱 **WhatsApp**: [wa.me/201013907174](https://wa.me/201013907174)

---

## Author

**COA — Community of Accountants**  
🌐 [wa.me/201013907174](https://wa.me/201013907174)

---

## License

This module is licensed under the [GNU Lesser General Public License v3.0 (LGPL-3)](https://www.gnu.org/licenses/lgpl-3.0.html).
