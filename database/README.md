# MyBillBook Analytics Database

PostgreSQL schema for analytics-grade storage of MyBillBook data.

## Quick Setup

### 1. Create Database

```sql
CREATE DATABASE mybillbook_analytics;
```

### 2. Run Schema

```bash
psql -d mybillbook_analytics -f schema.sql
```

### 3. Configure Connection

Edit `sync_to_postgres.py` and update `DB_CONFIG`:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "mybillbook_analytics",
    "user": "postgres",
    "password": "your_password_here",
}
```

### 4. Install Dependencies

```bash
pip install psycopg2-binary
```

### 5. Sync Data

```bash
python database/sync_to_postgres.py
```

## Schema Overview

### Master Tables

| Table | Description |
|-------|-------------|
| `contacts` | Customers and vendors |
| `categories` | Product and expense categories |
| `products` | Inventory with pricing |
| `bank_accounts` | Payment accounts |
| `addresses` | Billing/shipping addresses |

### Transaction Tables

| Table | Description |
|-------|-------------|
| `sales_invoices` | Invoice headers |
| `sales_invoice_line_items` | Products sold per invoice |
| `expenses` | Expense headers |
| `expense_line_items` | Individual expense items |

### Analytics Views

| View | Description |
|------|-------------|
| `v_customer_sales_summary` | Customer performance metrics |
| `v_product_profitability` | Product margins and sales |
| `v_monthly_financials` | Revenue/expense trends |
| `v_top_products_by_revenue` | Best sellers |
| `v_expense_category_summary` | Expense breakdown |
| `v_tax_summary` | GST/TCS/TDS tracking |
| `v_customer_payment_behavior` | AR aging analysis |
| `v_low_stock_alert` | Inventory reorder alerts |
| `v_invoice_validation` | Data quality checks |

## Example Queries

### Customer Sales Summary
```sql
SELECT * FROM mybillbook.v_customer_sales_summary
ORDER BY total_sales DESC
LIMIT 10;
```

### Product Profitability
```sql
SELECT * FROM mybillbook.v_product_profitability
WHERE avg_profit_margin_pct > 50
ORDER BY total_profit DESC;
```

### Monthly Revenue Trend
```sql
SELECT
    TO_CHAR(month, 'Mon YYYY') as month,
    sales,
    expenses,
    net_revenue,
    profit_margin_pct
FROM mybillbook.v_monthly_financials
ORDER BY month DESC
LIMIT 12;
```

### Outstanding Payments
```sql
SELECT * FROM mybillbook.v_customer_payment_behavior
WHERE total_outstanding > 0
ORDER BY total_outstanding DESC;
```

### Low Stock Items
```sql
SELECT * FROM mybillbook.v_low_stock_alert;
```

## Data Flow

```
MyBillBook API
     |
     v
Google Sheets (sync scripts)
     |
     v
PostgreSQL (this schema)
     |
     v
Analytics / BI Tools
```

## Files

- `schema.sql` - Database DDL with tables, indexes, views
- `sync_to_postgres.py` - Python script to sync from Sheets to PostgreSQL
