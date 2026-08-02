============================
Warehouse Location Restriction
============================
Version: 19.0.1.0.0

Overview
--------
Restrict inventory users' access to specific warehouses, stock locations,
and operation types on a per-user basis.

Key changes vs 16.0
--------------------
* Uses ``_search()`` hook instead of overriding ``search()`` (Odoo 19 API).
* View XML uses ``invisible=`` attribute directly — no legacy ``attrs={}``.
* ``self.env.su`` guard prevents admin bypass loops.

Features
--------
* Enable/Disable restriction per user (toggle).
* Allowed Warehouses — user only sees their assigned warehouses.
* Allowed Locations — including child locations automatically.
* Allowed Operation Types — Receipts, Deliveries, Internal, etc.
* Transfer Validation Guard — clear error on forbidden transfers.
* Inventory / Stock Quant filter — scoped to allowed locations.

Installation
------------
1. Copy folder to your Odoo addons path.
2. Restart Odoo and update the apps list.
3. Install "Warehouse Location Restriction".
4. Go to Settings → Users, open a user, and configure the
   **Location Restrictions** tab.

License
-------
AGPL-3
