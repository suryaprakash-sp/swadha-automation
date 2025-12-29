-- ============================================================
-- MyBillBook Analytics Database Schema
-- PostgreSQL 12+ Compatible
-- ============================================================
--
-- This schema provides a normalized, analytics-grade structure
-- for MyBillBook data with proper constraints, indexes, and views
-- ============================================================

-- Drop existing objects (for clean reinstall)
DROP SCHEMA IF EXISTS mybillbook CASCADE;
CREATE SCHEMA mybillbook;
SET search_path TO mybillbook;

-- ============================================================
-- MASTER DATA TABLES
-- ============================================================

-- Contacts (Customers & Vendors)
CREATE TABLE contacts (
    contact_id VARCHAR(100) PRIMARY KEY,
    contact_name VARCHAR(255) NOT NULL,
    contact_type VARCHAR(50), -- 'Customer', 'Vendor', etc.
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_contact_type CHECK (contact_type IN ('Customer', 'Vendor', 'Both', NULL))
);

CREATE INDEX idx_contacts_name ON contacts(contact_name);
CREATE INDEX idx_contacts_type ON contacts(contact_type);

COMMENT ON TABLE contacts IS 'Master table for all customers and vendors';
COMMENT ON COLUMN contacts.contact_id IS 'Unique identifier from MyBillBook';


-- Product Categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    category_type VARCHAR(50), -- 'Product', 'Expense', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_type ON categories(category_type);

COMMENT ON TABLE categories IS 'Product and expense categories';


-- Products (Inventory Items)
CREATE TABLE products (
    product_id VARCHAR(100) PRIMARY KEY,
    product_name VARCHAR(500) NOT NULL,
    sku_code VARCHAR(100) UNIQUE,
    category_id INTEGER REFERENCES categories(category_id),

    -- Pricing
    mrp NUMERIC(15,2),
    selling_price NUMERIC(15,2),
    sales_price NUMERIC(15,2),
    purchase_price NUMERIC(15,2),
    wholesale_price NUMERIC(15,2),
    wholesale_min_qty NUMERIC(15,3),

    -- Inventory
    quantity NUMERIC(15,3) DEFAULT 0,
    minimum_quantity NUMERIC(15,3),
    unit VARCHAR(20),
    unit_long VARCHAR(100),
    conversion_factor NUMERIC(15,6),

    -- Tax
    gst_percentage NUMERIC(5,2),
    sales_tax_included BOOLEAN,
    purchase_tax_included BOOLEAN,

    -- Metadata
    description TEXT,
    item_type VARCHAR(50),
    identification_code VARCHAR(100),
    show_on_store BOOLEAN DEFAULT false,
    excel_imported BOOLEAN DEFAULT false,
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_prices_positive CHECK (
        mrp >= 0 AND selling_price >= 0 AND sales_price >= 0
        AND purchase_price >= 0 AND wholesale_price >= 0
    ),
    CONSTRAINT chk_quantity_positive CHECK (quantity >= 0),
    CONSTRAINT chk_gst_valid CHECK (gst_percentage >= 0 AND gst_percentage <= 100)
);

CREATE INDEX idx_products_sku ON products(sku_code);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_name ON products(product_name);
CREATE INDEX idx_products_quantity ON products(quantity);

COMMENT ON TABLE products IS 'Inventory master data with pricing and stock information';
COMMENT ON COLUMN products.conversion_factor IS 'Unit conversion factor for multi-unit products';


-- Bank Accounts
CREATE TABLE bank_accounts (
    bank_account_id VARCHAR(100) PRIMARY KEY,
    account_name VARCHAR(255),
    bank_name VARCHAR(255),
    account_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE bank_accounts IS 'Bank account master data for payment tracking';


-- Addresses
CREATE TABLE addresses (
    address_id VARCHAR(100) PRIMARY KEY,
    contact_id VARCHAR(100) REFERENCES contacts(contact_id),
    address_type VARCHAR(50), -- 'Billing', 'Shipping'
    address_line1 TEXT,
    address_line2 TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_address_type CHECK (address_type IN ('Billing', 'Shipping', NULL))
);

CREATE INDEX idx_addresses_contact ON addresses(contact_id);
CREATE INDEX idx_addresses_type ON addresses(address_type);

COMMENT ON TABLE addresses IS 'Customer and vendor addresses';


-- ============================================================
-- SALES TRANSACTION TABLES
-- ============================================================

-- Sales Invoices (Header)
CREATE TABLE sales_invoices (
    invoice_id VARCHAR(100) PRIMARY KEY,
    mbb_id VARCHAR(100),
    invoice_number VARCHAR(100) NOT NULL UNIQUE,
    serial_number VARCHAR(100),
    invoice_date DATE NOT NULL,
    due_date DATE,

    -- Contact Information
    contact_id VARCHAR(100) REFERENCES contacts(contact_id),
    contact_name VARCHAR(255),
    contact_type VARCHAR(50),

    -- Amounts
    total_amount NUMERIC(15,2) NOT NULL DEFAULT 0,
    paid_amount NUMERIC(15,2) DEFAULT 0,
    remaining_amount NUMERIC(15,2) DEFAULT 0,

    -- Payment Details
    payment_mode VARCHAR(100),
    payment_type VARCHAR(100),
    bank_account_id VARCHAR(100) REFERENCES bank_accounts(bank_account_id),

    -- Status & Metadata
    status VARCHAR(50),
    ledger_category VARCHAR(100),
    source VARCHAR(100),
    einvoice_status VARCHAR(50),
    share_link TEXT,
    notes TEXT,

    -- References
    convertable_id VARCHAR(100), -- Quotation/Order converted to invoice
    recurring_id VARCHAR(100), -- Recurring invoice template

    -- Timestamps
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_amounts_positive CHECK (
        total_amount >= 0 AND paid_amount >= 0 AND remaining_amount >= 0
    ),
    CONSTRAINT chk_payment_logic CHECK (remaining_amount = total_amount - paid_amount),
    CONSTRAINT chk_invoice_status CHECK (status IN ('draft', 'final', 'cancelled', NULL))
);

CREATE INDEX idx_sales_invoices_date ON sales_invoices(invoice_date);
CREATE INDEX idx_sales_invoices_contact ON sales_invoices(contact_id);
CREATE INDEX idx_sales_invoices_status ON sales_invoices(status);
CREATE INDEX idx_sales_invoices_number ON sales_invoices(invoice_number);
CREATE INDEX idx_sales_invoices_payment_mode ON sales_invoices(payment_mode);

COMMENT ON TABLE sales_invoices IS 'Sales invoice header with summary information';
COMMENT ON COLUMN sales_invoices.remaining_amount IS 'Outstanding amount to be collected';


-- Sales Invoice Line Items (Detail)
CREATE TABLE sales_invoice_line_items (
    line_item_id SERIAL PRIMARY KEY,
    invoice_id VARCHAR(100) NOT NULL REFERENCES sales_invoices(invoice_id) ON DELETE CASCADE,

    -- Invoice Header Info (denormalized for analytics)
    invoice_number VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    customer_name VARCHAR(255),
    contact_id VARCHAR(100) REFERENCES contacts(contact_id),
    invoice_total NUMERIC(15,2),
    payment_mode VARCHAR(100),

    -- Invoice-Level Adjustments (denormalized)
    invoice_discount NUMERIC(15,2) DEFAULT 0,
    invoice_discount_type VARCHAR(50),
    round_off NUMERIC(15,2) DEFAULT 0,
    tcs_amount NUMERIC(15,2) DEFAULT 0, -- Tax Collected at Source
    tds_amount NUMERIC(15,2) DEFAULT 0, -- Tax Deducted at Source
    cess_amount NUMERIC(15,2) DEFAULT 0,
    additional_charges NUMERIC(15,2) DEFAULT 0,

    -- Address References
    billing_address_id VARCHAR(100) REFERENCES addresses(address_id),
    shipping_address_id VARCHAR(100) REFERENCES addresses(address_id),

    -- Product Information
    item_name VARCHAR(500) NOT NULL,
    sku_code VARCHAR(100),
    item_type VARCHAR(50),
    description TEXT,

    -- Quantity & Pricing
    quantity NUMERIC(15,3) NOT NULL,
    unit VARCHAR(20),
    selling_price NUMERIC(15,2) NOT NULL, -- Price per unit (selling)
    cost_price NUMERIC(15,2), -- Cost per unit (for profit calc)
    mrp NUMERIC(15,2),

    -- Calculated Profit Fields
    profit NUMERIC(15,2), -- Item Final Amount - (Cost Price × Quantity)
    profit_margin_percent NUMERIC(8,4), -- (Profit / Item Final Amount) × 100

    -- Item-Level Discount
    item_discount NUMERIC(15,2) DEFAULT 0,
    item_discount_type VARCHAR(50),
    item_discount_amount NUMERIC(15,2) DEFAULT 0,

    -- Tax
    gst_percentage NUMERIC(5,2),
    tax_included BOOLEAN,

    -- Final Amount
    item_final_amount NUMERIC(15,2) NOT NULL,

    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_prices_positive CHECK (
        selling_price >= 0 AND COALESCE(cost_price, 0) >= 0
        AND COALESCE(mrp, 0) >= 0 AND item_final_amount >= 0
    ),
    CONSTRAINT chk_gst_valid CHECK (gst_percentage >= 0 AND gst_percentage <= 100),
    CONSTRAINT chk_discount_type CHECK (
        item_discount_type IN ('percentage', 'amount', 'none', NULL)
    )
);

CREATE INDEX idx_invoice_line_items_invoice ON sales_invoice_line_items(invoice_id);
CREATE INDEX idx_invoice_line_items_date ON sales_invoice_line_items(invoice_date);
CREATE INDEX idx_invoice_line_items_product ON sales_invoice_line_items(sku_code);
CREATE INDEX idx_invoice_line_items_contact ON sales_invoice_line_items(contact_id);
CREATE INDEX idx_invoice_line_items_profit ON sales_invoice_line_items(profit_margin_percent);

COMMENT ON TABLE sales_invoice_line_items IS 'Individual line items from sales invoices with profit analysis';
COMMENT ON COLUMN sales_invoice_line_items.profit IS 'Gross profit per line item';
COMMENT ON COLUMN sales_invoice_line_items.profit_margin_percent IS 'Profit margin percentage for analytics';


-- ============================================================
-- EXPENSE TRANSACTION TABLES
-- ============================================================

-- Expenses (Header)
CREATE TABLE expenses (
    expense_id VARCHAR(100) PRIMARY KEY,
    mbb_id VARCHAR(100),
    expense_number VARCHAR(100) NOT NULL UNIQUE,
    serial_number VARCHAR(100),
    expense_date DATE NOT NULL,

    -- Category
    ledger_category_id VARCHAR(100),
    ledger_category_name VARCHAR(255),

    -- Contact Information
    contact_id VARCHAR(100) REFERENCES contacts(contact_id),
    contact_name VARCHAR(255),

    -- Amounts
    total_amount NUMERIC(15,2) NOT NULL DEFAULT 0,
    paid_amount NUMERIC(15,2) DEFAULT 0,

    -- Payment Details
    payment_mode VARCHAR(100),
    payment_type VARCHAR(100),
    bank_account_id VARCHAR(100) REFERENCES bank_accounts(bank_account_id),

    -- Metadata
    source VARCHAR(100),
    notes TEXT,
    share_link TEXT,

    -- Line Items Count
    line_items_count INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_expense_amounts_positive CHECK (
        total_amount >= 0 AND paid_amount >= 0
    )
);

CREATE INDEX idx_expenses_date ON expenses(expense_date);
CREATE INDEX idx_expenses_category ON expenses(ledger_category_name);
CREATE INDEX idx_expenses_contact ON expenses(contact_id);
CREATE INDEX idx_expenses_number ON expenses(expense_number);

COMMENT ON TABLE expenses IS 'Expense header with summary information';


-- Expense Line Items (Detail)
CREATE TABLE expense_line_items (
    line_item_id SERIAL PRIMARY KEY,
    expense_id VARCHAR(100) NOT NULL REFERENCES expenses(expense_id) ON DELETE CASCADE,

    -- Expense Header Info (denormalized for analytics)
    expense_number VARCHAR(100) NOT NULL,
    expense_date DATE NOT NULL,
    expense_category VARCHAR(255),
    expense_category_id VARCHAR(100),
    expense_total NUMERIC(15,2),
    payment_mode VARCHAR(100),
    payment_type VARCHAR(100),

    -- Expense-Level Adjustments (denormalized)
    expense_discount NUMERIC(15,2) DEFAULT 0,
    expense_discount_type VARCHAR(50),
    round_off NUMERIC(15,2) DEFAULT 0,
    place_of_supply VARCHAR(100),

    -- Contact (denormalized)
    contact_id VARCHAR(100) REFERENCES contacts(contact_id),
    contact_name VARCHAR(255),

    -- Item Information
    item_name VARCHAR(500) NOT NULL,
    item_id VARCHAR(100),
    ledger_id VARCHAR(100),
    identification_code VARCHAR(100),
    item_type VARCHAR(50),

    -- Quantity & Pricing
    quantity NUMERIC(15,3) NOT NULL,
    unit VARCHAR(20),
    unit_long VARCHAR(100),
    price_per_unit NUMERIC(15,2) NOT NULL,
    rate NUMERIC(15,2), -- Effective rate after discounts
    item_total_amount NUMERIC(15,2) NOT NULL,

    -- Item-Level Discount
    item_discount NUMERIC(15,2) DEFAULT 0,
    item_discount_type VARCHAR(50),

    -- Tax
    gst_percentage NUMERIC(5,2),
    tax_included BOOLEAN,
    tax_applicable BOOLEAN,
    tax_exempted BOOLEAN,
    itc_type VARCHAR(100), -- Input Tax Credit eligibility

    -- Metadata
    notes TEXT,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_expense_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_expense_prices_positive CHECK (
        price_per_unit >= 0 AND item_total_amount >= 0
    ),
    CONSTRAINT chk_expense_gst_valid CHECK (gst_percentage >= 0 AND gst_percentage <= 100)
);

CREATE INDEX idx_expense_line_items_expense ON expense_line_items(expense_id);
CREATE INDEX idx_expense_line_items_date ON expense_line_items(expense_date);
CREATE INDEX idx_expense_line_items_category ON expense_line_items(expense_category);
CREATE INDEX idx_expense_line_items_contact ON expense_line_items(contact_id);
CREATE INDEX idx_expense_line_items_item ON expense_line_items(item_name);

COMMENT ON TABLE expense_line_items IS 'Individual line items from expenses with tax details';
COMMENT ON COLUMN expense_line_items.itc_type IS 'Input Tax Credit eligibility type';


-- ============================================================
-- ANALYTICS VIEWS
-- ============================================================

-- Customer Sales Summary
CREATE OR REPLACE VIEW v_customer_sales_summary AS
SELECT
    c.contact_id,
    c.contact_name,
    COUNT(DISTINCT si.invoice_id) as total_invoices,
    SUM(si.total_amount) as total_sales,
    SUM(si.paid_amount) as total_collected,
    SUM(si.remaining_amount) as total_outstanding,
    MIN(si.invoice_date) as first_purchase_date,
    MAX(si.invoice_date) as last_purchase_date,
    AVG(si.total_amount) as avg_invoice_value,
    COUNT(DISTINCT DATE_TRUNC('month', si.invoice_date)) as months_active
FROM contacts c
LEFT JOIN sales_invoices si ON c.contact_id = si.contact_id
WHERE si.status = 'final'
GROUP BY c.contact_id, c.contact_name
ORDER BY total_sales DESC NULLS LAST;

COMMENT ON VIEW v_customer_sales_summary IS 'Customer-wise sales analytics summary';


-- Product Profitability Analysis
CREATE OR REPLACE VIEW v_product_profitability AS
SELECT
    p.product_id,
    p.product_name,
    p.sku_code,
    p.category_id,
    COUNT(DISTINCT li.invoice_id) as times_sold,
    SUM(li.quantity) as total_qty_sold,
    SUM(li.item_final_amount) as total_revenue,
    SUM(li.profit) as total_profit,
    AVG(li.profit_margin_percent) as avg_profit_margin_pct,
    MIN(li.invoice_date) as first_sold_date,
    MAX(li.invoice_date) as last_sold_date,
    p.quantity as current_stock
FROM products p
LEFT JOIN sales_invoice_line_items li ON p.sku_code = li.sku_code
GROUP BY p.product_id, p.product_name, p.sku_code, p.category_id, p.quantity
ORDER BY total_profit DESC NULLS LAST;

COMMENT ON VIEW v_product_profitability IS 'Product-wise profitability and sales metrics';


-- Monthly Revenue & Expense Trend
CREATE OR REPLACE VIEW v_monthly_financials AS
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', invoice_date) as month,
        SUM(total_amount) as sales_amount,
        COUNT(*) as invoice_count
    FROM sales_invoices
    WHERE status = 'final'
    GROUP BY DATE_TRUNC('month', invoice_date)
),
monthly_expenses AS (
    SELECT
        DATE_TRUNC('month', expense_date) as month,
        SUM(total_amount) as expense_amount,
        COUNT(*) as expense_count
    FROM expenses
    GROUP BY DATE_TRUNC('month', expense_date)
),
monthly_profit AS (
    SELECT
        DATE_TRUNC('month', invoice_date) as month,
        SUM(profit) as gross_profit,
        SUM(item_final_amount) as revenue
    FROM sales_invoice_line_items
    GROUP BY DATE_TRUNC('month', invoice_date)
)
SELECT
    COALESCE(ms.month, me.month, mp.month) as month,
    COALESCE(ms.sales_amount, 0) as sales,
    COALESCE(ms.invoice_count, 0) as invoices,
    COALESCE(me.expense_amount, 0) as expenses,
    COALESCE(me.expense_count, 0) as expense_vouchers,
    COALESCE(mp.gross_profit, 0) as gross_profit,
    COALESCE(ms.sales_amount, 0) - COALESCE(me.expense_amount, 0) as net_revenue,
    CASE
        WHEN COALESCE(mp.revenue, 0) > 0
        THEN (mp.gross_profit / mp.revenue * 100)
        ELSE 0
    END as profit_margin_pct
FROM monthly_sales ms
FULL OUTER JOIN monthly_expenses me ON ms.month = me.month
FULL OUTER JOIN monthly_profit mp ON ms.month = mp.month
ORDER BY month DESC;

COMMENT ON VIEW v_monthly_financials IS 'Monthly financial summary with revenue, expenses, and profit';


-- Top Selling Products (by Revenue)
CREATE OR REPLACE VIEW v_top_products_by_revenue AS
SELECT
    item_name,
    sku_code,
    SUM(quantity) as total_quantity_sold,
    SUM(item_final_amount) as total_revenue,
    AVG(selling_price) as avg_selling_price,
    AVG(profit_margin_percent) as avg_margin_pct,
    COUNT(DISTINCT invoice_id) as times_sold
FROM sales_invoice_line_items
GROUP BY item_name, sku_code
ORDER BY total_revenue DESC
LIMIT 50;

COMMENT ON VIEW v_top_products_by_revenue IS 'Top 50 products by revenue';


-- Expense Category Analysis
CREATE OR REPLACE VIEW v_expense_category_summary AS
SELECT
    expense_category,
    COUNT(DISTINCT expense_id) as expense_count,
    SUM(item_total_amount) as total_amount,
    AVG(item_total_amount) as avg_expense_amount,
    SUM(CASE WHEN tax_applicable THEN item_total_amount ELSE 0 END) as taxable_amount,
    SUM(CASE WHEN tax_exempted THEN item_total_amount ELSE 0 END) as tax_exempt_amount,
    MIN(expense_date) as earliest_expense,
    MAX(expense_date) as latest_expense
FROM expense_line_items
GROUP BY expense_category
ORDER BY total_amount DESC;

COMMENT ON VIEW v_expense_category_summary IS 'Expense analysis by category with tax breakdown';


-- Tax Summary (GST Collections & Payments)
CREATE OR REPLACE VIEW v_tax_summary AS
WITH sales_tax AS (
    SELECT
        DATE_TRUNC('month', invoice_date) as month,
        SUM(item_final_amount * gst_percentage / 100) as gst_collected,
        SUM(tcs_amount) as tcs_collected,
        SUM(tds_amount) as tds_deducted
    FROM sales_invoice_line_items
    WHERE tax_included = false
    GROUP BY DATE_TRUNC('month', invoice_date)
),
expense_tax AS (
    SELECT
        DATE_TRUNC('month', expense_date) as month,
        SUM(item_total_amount * gst_percentage / 100) as gst_paid
    FROM expense_line_items
    WHERE tax_applicable = true AND tax_included = false
    GROUP BY DATE_TRUNC('month', expense_date)
)
SELECT
    COALESCE(st.month, et.month) as month,
    COALESCE(st.gst_collected, 0) as gst_collected,
    COALESCE(et.gst_paid, 0) as gst_paid,
    COALESCE(st.gst_collected, 0) - COALESCE(et.gst_paid, 0) as gst_payable,
    COALESCE(st.tcs_collected, 0) as tcs_collected,
    COALESCE(st.tds_deducted, 0) as tds_deducted
FROM sales_tax st
FULL OUTER JOIN expense_tax et ON st.month = et.month
ORDER BY month DESC;

COMMENT ON VIEW v_tax_summary IS 'Monthly tax summary including GST, TCS, and TDS';


-- Customer Payment Analysis
CREATE OR REPLACE VIEW v_customer_payment_behavior AS
SELECT
    contact_id,
    contact_name,
    COUNT(*) as total_invoices,
    SUM(total_amount) as total_billed,
    SUM(paid_amount) as total_paid,
    SUM(remaining_amount) as total_outstanding,
    ROUND(AVG(EXTRACT(EPOCH FROM (CURRENT_DATE - invoice_date))/86400), 0) as avg_invoice_age_days,
    COUNT(CASE WHEN remaining_amount > 0 THEN 1 END) as unpaid_invoices,
    ROUND((SUM(paid_amount)::NUMERIC / NULLIF(SUM(total_amount), 0) * 100), 2) as payment_rate_pct
FROM sales_invoices
WHERE status = 'final'
GROUP BY contact_id, contact_name
HAVING SUM(total_amount) > 0
ORDER BY total_outstanding DESC;

COMMENT ON VIEW v_customer_payment_behavior IS 'Customer payment behavior and outstanding analysis';


-- Low Stock Alert
CREATE OR REPLACE VIEW v_low_stock_alert AS
SELECT
    product_id,
    product_name,
    sku_code,
    quantity as current_stock,
    minimum_quantity as reorder_level,
    (minimum_quantity - quantity) as qty_to_reorder,
    selling_price,
    purchase_price,
    (minimum_quantity - quantity) * purchase_price as reorder_cost
FROM products
WHERE quantity <= minimum_quantity
  AND minimum_quantity > 0
ORDER BY (minimum_quantity - quantity) DESC;

COMMENT ON VIEW v_low_stock_alert IS 'Products below reorder level requiring restocking';


-- Invoice vs Line Items Validation
CREATE OR REPLACE VIEW v_invoice_validation AS
SELECT
    si.invoice_id,
    si.invoice_number,
    si.invoice_date,
    si.total_amount as invoice_total,
    COALESCE(SUM(li.item_final_amount), 0) as line_items_sum,
    si.total_amount - COALESCE(SUM(li.item_final_amount), 0) as difference,
    COUNT(li.line_item_id) as line_item_count,
    CASE
        WHEN ABS(si.total_amount - COALESCE(SUM(li.item_final_amount), 0)) > 1 THEN 'MISMATCH'
        WHEN COUNT(li.line_item_id) = 0 THEN 'NO_ITEMS'
        ELSE 'OK'
    END as validation_status
FROM sales_invoices si
LEFT JOIN sales_invoice_line_items li ON si.invoice_id = li.invoice_id
GROUP BY si.invoice_id, si.invoice_number, si.invoice_date, si.total_amount
HAVING ABS(si.total_amount - COALESCE(SUM(li.item_final_amount), 0)) > 1
   OR COUNT(li.line_item_id) = 0
ORDER BY ABS(si.total_amount - COALESCE(SUM(li.item_final_amount), 0)) DESC;

COMMENT ON VIEW v_invoice_validation IS 'Data validation: invoices with mismatched totals or missing line items';


-- ============================================================
-- UTILITY FUNCTIONS
-- ============================================================

-- Function to calculate profit margin percentage
CREATE OR REPLACE FUNCTION calculate_profit_margin(
    item_amount NUMERIC,
    cost NUMERIC
) RETURNS NUMERIC AS $$
BEGIN
    IF item_amount IS NULL OR item_amount = 0 THEN
        RETURN 0;
    END IF;
    RETURN ((item_amount - cost) / item_amount * 100);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION calculate_profit_margin IS 'Calculate profit margin percentage from revenue and cost';


-- ============================================================
-- PERMISSIONS (Optional - adjust based on your setup)
-- ============================================================

-- Grant read-only access to analytics role
-- CREATE ROLE analytics_readonly;
-- GRANT USAGE ON SCHEMA mybillbook TO analytics_readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA mybillbook TO analytics_readonly;
-- GRANT SELECT ON ALL VIEWS IN SCHEMA mybillbook TO analytics_readonly;

-- Grant read-write access to application role
-- CREATE ROLE mybillbook_app;
-- GRANT USAGE ON SCHEMA mybillbook TO mybillbook_app;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mybillbook TO mybillbook_app;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA mybillbook TO mybillbook_app;


-- ============================================================
-- INDEXES FOR COMMON ANALYTICS QUERIES
-- ============================================================

-- Date range queries
CREATE INDEX idx_sales_invoices_date_range ON sales_invoices(invoice_date, status);
CREATE INDEX idx_expenses_date_range ON expenses(expense_date);

-- Customer analytics
CREATE INDEX idx_sales_invoice_items_customer_date ON sales_invoice_line_items(contact_id, invoice_date);

-- Product analytics
CREATE INDEX idx_sales_invoice_items_product_date ON sales_invoice_line_items(sku_code, invoice_date);

-- Profit analysis
CREATE INDEX idx_sales_invoice_items_profit_date ON sales_invoice_line_items(invoice_date, profit);

-- Payment tracking
CREATE INDEX idx_sales_invoices_outstanding ON sales_invoices(remaining_amount) WHERE remaining_amount > 0;


-- ============================================================
-- TRIGGER: Auto-update timestamps
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sales_invoices_updated_at BEFORE UPDATE ON sales_invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_expenses_updated_at BEFORE UPDATE ON expenses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================================
-- SUMMARY
-- ============================================================

-- Master Tables:
--   • contacts (customers/vendors)
--   • categories (product/expense categories)
--   • products (inventory with pricing)
--   • bank_accounts (payment accounts)
--   • addresses (billing/shipping)
--
-- Transaction Tables:
--   • sales_invoices (invoice headers)
--   • sales_invoice_line_items (individual products sold)
--   • expenses (expense headers)
--   • expense_line_items (individual expense items)
--
-- Analytics Views:
--   • v_customer_sales_summary (customer performance)
--   • v_product_profitability (product margins & sales)
--   • v_monthly_financials (revenue/expense trends)
--   • v_top_products_by_revenue (best sellers)
--   • v_expense_category_summary (expense breakdown)
--   • v_tax_summary (GST/TCS/TDS tracking)
--   • v_customer_payment_behavior (AR aging)
--   • v_low_stock_alert (inventory reorders)
--   • v_invoice_validation (data quality checks)

SELECT 'Schema created successfully!' as status;
