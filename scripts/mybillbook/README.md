# MyBillBook Scripts

This folder contains all MyBillBook-related automation scripts.

## Available Scripts

### 1. `sync_inventory.py`
**Sync MyBillBook Inventory to Google Sheets**

Fetches the latest inventory from MyBillBook API and syncs it to Google Sheets.

**Usage:**
```bash
python scripts/mybillbook/sync_inventory.py
```

**What it does:**
- Connects to MyBillBook API with your credentials
- Fetches all inventory items (products, SKUs, prices, quantities)
- Writes to Google Sheets in the "myBillBook Inventory" sheet
- Formats data with proper types (text for SKUs, numbers for prices)
- Creates automatic safety backups before clearing
- Optionally exports to CSV for offline backup

**Requirements:**
- MyBillBook API credentials configured in `.env` file
- See `docs/MYBILLBOOK_SETUP.md` for setup instructions

---

### 2. `sync_sales_invoices.py`
**Sync MyBillBook Sales Invoices to Google Sheets**

Fetches ALL sales invoices from MyBillBook API with automatic pagination and syncs them to Google Sheets.

**Usage:**
```bash
python scripts/mybillbook/sync_sales_invoices.py
```

**What it does:**
- Connects to MyBillBook API with your credentials
- Fetches ALL sales invoices with automatic pagination (handles 100s or 1000s of invoices)
- Lets you choose date range:
  - Last 30 days
  - Last 90 days
  - Last 1 year (default)
  - Custom date range
- Writes to Google Sheets in the "Sales Invoices" sheet
- Includes all invoice data: invoice number, date, customer, amounts, payment details
- Formats data with proper types
- Creates automatic safety backups before clearing
- Optionally exports to CSV for offline backup

**Data Fields Synced:**
- Invoice Number, Date, Serial Number
- Contact Name & Type
- Total Amount, Paid Amount, Remaining Amount
- Payment Mode & Type
- Due Date, Status
- Share Link, Notes
- And more...

**Requirements:**
- MyBillBook API credentials configured in `.env` file
- See `docs/MYBILLBOOK_SETUP.md` for setup instructions

---

### 3. `sync_expenses.py`
**Sync MyBillBook Expenses to Google Sheets**

Fetches ALL expenses from MyBillBook API with automatic pagination and syncs them to Google Sheets.

**Usage:**
```bash
python scripts/mybillbook/sync_expenses.py
```

**What it does:**
- Connects to MyBillBook API with your credentials
- Fetches ALL expenses with automatic pagination (handles 100s or 1000s of expenses)
- Lets you choose date range:
  - Last 30 days
  - Last 90 days
  - Last 1 year (default)
  - Custom date range
- Writes to Google Sheets in the "Expenses" sheet
- Includes all expense data: expense number, date, category, amounts, payment details
- Extracts expense line items from txn_ledgers array
- Formats data with proper types
- Creates automatic safety backups before clearing
- Optionally exports to CSV for offline backup

**Data Fields Synced:**
- Expense Number, Date, Serial Number
- Expense Category (Rent, Food & Snacks, Transportation, etc.)
- Expense Item (first line item name)
- Line Items Count
- Total Amount, Paid Amount
- Payment Mode & Type
- Created At, Notes
- IDs, Share Link
- And more...

**Requirements:**
- MyBillBook API credentials configured in `.env` file
- See `docs/MYBILLBOOK_SETUP.md` for setup instructions

---

### 4. `sync_invoice_line_items.py`
**Sync Individual Products Sold in Each Invoice to Google Sheets**

Extracts every individual product sold from each sales invoice and creates a denormalized table with one row per product. This is useful for product-level sales analysis.

**Usage:**
```bash
python scripts/mybillbook/sync_invoice_line_items.py
```

**What it does:**
- Fetches ALL sales invoices from MyBillBook API
- For each invoice, calls the detail API to get line items (products sold)
- Creates one row per product with both invoice details AND product details
- Lets you choose date range (last 30/90/365 days or custom)
- Writes to Google Sheets in the "Invoice Line Items" sheet
- Invoice number serves as the join key to link with sales invoices
- Formats data with proper types
- Creates automatic safety backups before clearing
- Optionally exports to CSV for offline backup

**Data Fields Synced (20 fields per line item):**
- **Invoice Info**: Invoice Number, Date, Customer Name, Total, Payment Mode
- **Product Info**: Item Name, SKU Code, Quantity, Unit
- **Pricing**: Price Per Unit, MRP, Item Final Amount
- **Discounts**: Discount, Discount Type, Discount Amount
- **Tax**: GST %, Tax Included (Yes/No)
- **Other**: Item Type, Description, Notes

**Example Output:**
```
Invoice #525 | 2025-01-15 | John Doe | 390 | Cash | Charms 40 VBOC | CH40 | 6 | Pcs | 40 | 0 | | 0 | 18 | No | 240 | ...
Invoice #525 | 2025-01-15 | John Doe | 390 | Cash | Bracelets 150 UVPV | BR150 | 1 | Pcs | 150 | 0 | | 0 | 18 | No | 150 | ...
```

**Requirements:**
- MyBillBook API credentials configured in `.env` file
- See `docs/MYBILLBOOK_SETUP.md` for setup instructions

**Performance:**
- Processes 500 invoices with ~1000 line items in about 3-5 minutes
- Includes API rate limiting (0.5s delay every 10 invoices)

---

## Coming Soon

More MyBillBook scripts will be added here for different use cases:
- Purchase invoices sync
- Customer data sync
- Custom reports
- Bulk updates

---

## Quick Reference

**Current Structure:**
```
scripts/mybillbook/
├── README.md                      # This file
├── sync_inventory.py              # Inventory sync script
├── sync_sales_invoices.py         # Sales invoices sync script
├── sync_expenses.py               # Expenses sync script
└── sync_invoice_line_items.py     # Invoice line items (products) sync script
```

**Run from project root:**
```bash
# Sync inventory
python scripts/mybillbook/sync_inventory.py

# Sync sales invoices
python scripts/mybillbook/sync_sales_invoices.py

# Sync expenses
python scripts/mybillbook/sync_expenses.py

# Sync invoice line items (individual products per invoice)
python scripts/mybillbook/sync_invoice_line_items.py
```
