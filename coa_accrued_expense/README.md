# COA Accrued Expenses (Odoo 18)

Spread a vendor bill expense over a period as an **Accrued** expense — a separate
feature from Odoo's built-in Deferred expense.

## Setup
1. Install the module (depends on `account`).
2. Accounting → Configuration → Settings → **Accrued Expenses**:
   - **Accrued Account** — the intermediate account.
   - **Accrual Journal** — a `Miscellaneous` (general) journal.

## Usage
On a vendor bill line, enable the optional columns (list options icon) and:
- tick **Accrued**,
- set **Accrual Start** and **Accrual End**.

Post the bill. The module then books:

| When | Entry |
|------|-------|
| Bill date | Dr **Accrued** / Cr **Expense** (full amount) |
| End of each month | Dr **Expense** / Cr **Accrued** (that month's share) |

Combined with the bill itself (Dr Expense / Cr Vendor), the net effect at bill
date is **Dr Accrued / Cr Vendor**, and the expense lands on the P&L month by
month. Future months are created in draft and posted automatically by the daily
cron **"Post Due Accrued Expense Entries"** when their date arrives.

Use the **Accrued** smart button on the bill to review the generated entries.

## Notes / limitations
- Amounts are computed in the company currency.
- Monthly amounts are day-prorated; the last month absorbs rounding.
- Resetting a posted bill to draft deletes only the *unposted* accrued entries;
  already-posted recognition entries stay and must be reversed manually.
- Changing the accrual dates after posting requires removing the generated
  entries first.
