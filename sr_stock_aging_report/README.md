# Stock Aging Report – Odoo 19.0

A free, open-source alternative to the commercial `sr_stock_aging_report` module.

## Features

| Feature | Description |
|---------|-------------|
| **By Warehouse** | Aggregate aging data per warehouse |
| **By Location** | Breakdown at individual stock location level |
| **Product Filter** | Filter by specific products |
| **Category Filter** | Filter by product category |
| **As-of Date** | Historical aging as of any past date |
| **Custom Periods** | Configure your own aging buckets (default 30/60/90/120 days) |
| **PDF Report** | Printable QWeb PDF with totals and subtotals |
| **FIFO Algorithm** | Accurate age calculation using FIFO stock move matching |

## Installation

1. Copy the `sr_stock_aging_report` folder to your Odoo addons directory.
2. Update the app list: **Settings → Apps → Update Apps List**.
3. Search for **"Stock Aging Report"** and click **Install**.

## Usage

Go to **Inventory → Reporting → Stock Aging Report**.

A wizard will open with the following options:

### Report Type
- **By Warehouse** – shows one section per warehouse
- **By Location** – shows one section per internal stock location

### Filters
- **Warehouses / Locations** – leave empty to include all
- **Products** – leave empty to include all storable/consumable products
- **Product Categories** – leave empty for all categories

### Aging Periods
Configure the day thresholds for the 5 columns. Defaults:
```
0–30  |  31–60  |  61–90  |  91–120  |  >120
```

Click **Print PDF Report** to generate the report.

## Technical Notes

- Uses `stock.move.line` with state `done` for accurate FIFO matching.
- Quantities are the **net remaining** after applying outgoing moves in FIFO order.
- Values use the **unit cost at the time of receipt** (`stock.move.price_unit`).
- Compatible with **AVCO**, **FIFO**, and **Standard Price** costing methods
  (age is based on move date, not costing layer).

## Module Structure

```
sr_stock_aging_report/
├── __init__.py
├── __manifest__.py
├── models/
│   └── __init__.py
├── wizard/
│   ├── __init__.py
│   ├── stock_aging_wizard.py          ← core logic
│   └── stock_aging_wizard_view.xml    ← form view
├── report/
│   ├── stock_aging_report_action.xml  ← ir.actions.report
│   └── stock_aging_report_template.xml← QWeb PDF template
├── security/
│   └── ir.model.access.csv
├── data/
│   └── stock_aging_menu.xml           ← Inventory > Reporting menu
└── README.md
```

## License

LGPL-3 – Free to use, modify, and distribute.
