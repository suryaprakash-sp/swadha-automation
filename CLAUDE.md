# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Swadha Automation is a Python data pipeline for inventory management with MyBillBook API integration. It consolidates inventory data from Google Sheets, transforms it for MyBillBook import, and syncs with a PostgreSQL analytics database.

## Development Environment

- **IDE:** IntelliJ IDEA
- **Platform:** Windows

## Commands

### Running the Application

```bash
# Web UI (recommended)
streamlit run scripts/app.py

# CLI interactive menu
python scripts/main.py

# Label generator
python scripts/generate_labels.py
```

### Standalone Sync Scripts

```bash
# Sync MyBillBook inventory to Google Sheets
python scripts/mybillbook/sync_inventory.py

# Sync sales invoices (with pagination)
python scripts/mybillbook/sync_sales_invoices.py

# Sync expenses
python scripts/mybillbook/sync_expenses.py

# Extract invoice line items
python scripts/mybillbook/sync_invoice_line_items.py

# Extract expense line items
python scripts/mybillbook/sync_expense_line_items.py

# Sync to PostgreSQL analytics database
python database/sync_to_postgres.py
```

### Setup

```bash
pip install -r requirements.txt
```

## Architecture

### Data Flow Pipeline

```
MyBillBook API → Google Sheets ("myBillBook Inventory")
                          ↓
Google Sheets ("Inventory RAW") - Manual data entry
                          ↓
Transform 1: Consolidate + Smart Match (transforms/transform1_consolidate.py)
  - Consolidates duplicates
  - 4-criteria matching: Category + Cost Price + Selling Price + Name variant
  - Outputs to "Inventory" sheet with Column I (Already Present) and Column J (Barcode)
                          ↓
Transform 2: MyBillBook Export (transforms/transform2_mybillbook.py)
  - Splits by Column I: "Yes" → "myBillBook update", "No" → "myBillBook add"
                          ↓
Transform 3: WePrint Labels (transforms/transform3_weprint.py)
  - Generates label rows duplicated by quantity
                          ↓
CSV Exports (csv_exports/) + PostgreSQL Analytics (database/)
```

### Project Structure

```
swadha-automation/
├── config.py                 # Google Sheets IDs and sheet names
├── requirements.txt          # Python dependencies
├── credentials.json          # Google OAuth credentials (not in git)
├── token.json                # OAuth token (auto-generated)
├── .env                      # MyBillBook + PostgreSQL credentials
│
├── scripts/                  # Entry points
│   ├── app.py                # Streamlit web UI
│   ├── main.py               # CLI interactive menu
│   ├── generate_labels.py    # WePrint label generator
│   └── mybillbook/           # Standalone sync scripts
│       ├── sync_inventory.py
│       ├── sync_sales_invoices.py
│       ├── sync_expenses.py
│       ├── sync_invoice_line_items.py
│       └── sync_expense_line_items.py
│
├── mybillbook/               # API Integration
│   ├── api_client.py         # REST API client with retry logic
│   ├── config.py             # Reads credentials from .env
│   └── sync.py               # Inventory sync to Google Sheets
│
├── transforms/               # Data Pipeline
│   ├── transform1_consolidate.py
│   ├── transform2_mybillbook.py
│   └── transform3_weprint.py
│
├── utils/                    # Shared Utilities
│   ├── sheets.py             # Google Sheets API wrapper (OAuth, retry)
│   └── csv_exporter.py       # Timestamped CSV exports
│
├── database/                 # PostgreSQL Analytics
│   ├── schema.sql            # Complete schema (tables, views, indexes)
│   └── sync_to_postgres.py   # Google Sheets → PostgreSQL sync
│
├── docs/                     # Documentation
└── csv_exports/              # Timestamped CSV backups
```

### Environment Variables (.env)

```
MYBILLBOOK_AUTH_TOKEN=Bearer [JWT token]
MYBILLBOOK_COMPANY_ID=[UUID]
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=mybillbook_analytics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=[password]
```

## Google Sheets Structure

| Sheet Name | Purpose |
|------------|---------|
| `myBillBook Inventory` | Synced from MyBillBook API |
| `Inventory RAW` | Manual data entry source |
| `Inventory` | Consolidated output with match status |
| `myBillBook add` | New items for MyBillBook import |
| `myBillBook update` | Existing items for MyBillBook update |
| `WePrint` | Label data for printing |
| `Sales Invoices` | Synced invoice headers |
| `Invoice Line Items` | Individual products from invoices |
| `Expenses` | Synced expense records |

## PostgreSQL Analytics Database

Schema in `database/schema.sql` uses `mybillbook` schema with:

**Master tables:** `contacts`, `categories`, `products`, `bank_accounts`, `addresses`

**Transaction tables:** `sales_invoices`, `sales_invoice_line_items`, `expenses`, `expense_line_items`

**Analytics views:** `v_customer_sales_summary`, `v_product_profitability`, `v_monthly_financials`, `v_top_products_by_revenue`, `v_expense_category_summary`, `v_tax_summary`, `v_customer_payment_behavior`, `v_low_stock_alert`, `v_invoice_validation`
