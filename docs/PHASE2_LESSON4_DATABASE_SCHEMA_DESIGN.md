# Phase 2 - Lesson 4: Database Schema Design
## Designing Your Inventory Database from Scratch

---

## Table of Contents
1. [Database Design Fundamentals](#database-design-fundamentals)
2. [Analyzing Your Data](#analyzing-your-data)
3. [Schema Design Process](#schema-design-process)
4. [Complete Schema Definition](#complete-schema-definition)
5. [Understanding Relationships](#understanding-relationships)
6. [Indexing Strategy](#indexing-strategy)
7. [Testing Your Design](#testing-your-design)
8. [Migration Considerations](#migration-considerations)

---

## Database Design Fundamentals

### What is Database Schema?

**Simple Definition:**
```
Schema = Blueprint of your database

Like building a house:
  Blueprint → Shows rooms, walls, doors
  Schema   → Shows tables, columns, relationships

Good blueprint = Strong house
Good schema = Fast, reliable database
```

### Why Design Matters

**Bad Design:**
```sql
-- Everything in ONE table (nightmare!)
CREATE TABLE everything (
    item_data TEXT  -- "Ear Rings,110,250,4,Yes,..."
);

Problems:
  ✗ Can't query specific columns
  ✗ Can't calculate totals
  ✗ Data duplicated everywhere
  ✗ Impossible to maintain
```

**Good Design:**
```sql
-- Organized into logical tables
CREATE TABLE categories (...);
CREATE TABLE inventory_items (...);
CREATE TABLE sales (...);

Benefits:
  ✓ Each piece of data stored once
  ✓ Easy to query
  ✓ Fast performance
  ✓ Easy to maintain
```

---

## Analyzing Your Data

### Your Current Google Sheets Structure

**From Phase 1, you have:**

```
Inventory Sheet (10 columns):
├─ A: Type (Category)              Example: "Ear Rings"
├─ B: Name                         Example: "Ear Rings XCNR"
├─ C: Per Item (Cost Price)        Example: 110.00
├─ D: Quantity                     Example: 4
├─ E: Per Item (Selling Price)     Example: 250.00
├─ F: Total Cost Price             Formula: =C*D
├─ G: Total Selling Price          Formula: =D*E
├─ H: Barcode                      Example: "24 0118"
├─ I: Already Present              Example: "Yes"
└─ J: Inventory Item Barcode       Example: "84 0110"
```

### Data Analysis Questions

**Question 1: What needs to be stored?**
```
Core Data:
  ✓ Product information (name, category)
  ✓ Pricing (cost, selling price)
  ✓ Inventory levels (quantity)
  ✓ Identification (barcodes, SKUs)
  ✓ MyBillBook integration status

Calculated Data (don't store!):
  ✗ Total cost (calculate: cost * quantity)
  ✗ Total selling (calculate: selling * quantity)
  ✗ Profit (calculate: selling - cost)
```

**Question 2: What are the "things" (entities)?**
```
Entity 1: CATEGORY
  - Ear Rings, Bracelets, Necklaces, etc.
  - Each category has a name

Entity 2: INVENTORY ITEM
  - Individual products
  - Each item has: name, prices, quantity
  - Belongs to ONE category

Entity 3: SYNC HISTORY
  - Records of data updates
  - Tracks when data was synced

Entity 4: SALES (future)
  - Sales transactions
  - Which items sold, when, how much
```

**Question 3: What are the relationships?**
```
Category ─┬─→ Inventory Item
          ├─→ Inventory Item
          └─→ Inventory Item

One category has MANY items
One item belongs to ONE category

This is called: "One-to-Many" relationship
```

---

## Schema Design Process

### Step 1: Identify Tables

Based on analysis, we need **4 tables:**

```
1. categories          (Ear Rings, Bracelets, etc.)
2. inventory_items     (Actual products)
3. sync_history        (Track data updates)
4. sales              (Future: sales transactions)
```

### Step 2: Define Columns for Each Table

**Table 1: categories**
```
Purpose: Store product categories
Columns needed:
  - id          (unique identifier)
  - name        (category name like "Ear Rings")
  - created_at  (when category was added)
```

**Table 2: inventory_items**
```
Purpose: Store individual products
Columns needed:
  - id                      (unique identifier)
  - category_id             (which category? links to categories.id)
  - item_name               (product name)
  - cost_price              (how much you paid)
  - selling_price           (how much you sell for)
  - quantity                (how many in stock)
  - barcode                 (unique barcode)
  - already_in_mybillbook   (Yes/No - is it in MyBillBook?)
  - mybillbook_sku          (MyBillBook's SKU if exists)
  - created_at              (when added)
  - updated_at              (when last modified)
```

**Table 3: sync_history**
```
Purpose: Track when data was synced
Columns needed:
  - id            (unique identifier)
  - sync_date     (when sync happened)
  - items_synced  (how many items)
  - source        (where from? "Google Sheets", "Manual", etc.)
  - status        (SUCCESS or FAILED)
  - notes         (any additional info)
```

**Table 4: sales**
```
Purpose: Track sales (future use)
Columns needed:
  - id             (unique identifier)
  - item_id        (which item was sold? links to inventory_items.id)
  - quantity_sold  (how many sold)
  - sale_price     (price sold at)
  - sale_date      (when sold)
  - customer_name  (optional)
  - payment_method (Cash, Card, UPI, etc.)
  - notes          (any notes)
```

### Step 3: Choose Data Types

**PostgreSQL Data Types (2025 Best Practices):**

```sql
-- NUMERIC TYPES
INTEGER           -- Whole numbers: -2B to +2B
BIGINT            -- Large whole numbers (if you need more)
DECIMAL(10,2)     -- Exact decimals: 10 digits total, 2 after decimal
                  -- Use for MONEY (not FLOAT!)
SERIAL            -- Auto-incrementing integer (for IDs)
BIGSERIAL         -- Auto-incrementing bigint

-- TEXT TYPES
VARCHAR(n)        -- Variable length text, max n characters
TEXT              -- Unlimited length text
CHAR(n)           -- Fixed length text (rarely used)

-- BOOLEAN
BOOLEAN           -- TRUE or FALSE

-- DATE/TIME
TIMESTAMP         -- Date and time: 2025-12-22 14:30:00
DATE              -- Just date: 2025-12-22
TIME              -- Just time: 14:30:00

-- SPECIAL
JSONB             -- JSON data (flexible, fast queries)
ARRAY             -- Arrays (advanced)
```

**Why DECIMAL for money, not FLOAT?**
```sql
-- BAD (FLOAT):
SELECT 110.00 + 45.50;  -- Might give: 155.49999999

-- GOOD (DECIMAL):
SELECT 110.00::DECIMAL + 45.50::DECIMAL;  -- Always: 155.50

Rule: ALWAYS use DECIMAL for money!
```

**Choosing sizes:**
```
item_name: VARCHAR(200)
  - Why 200? Product names rarely > 200 chars
  - Saves space vs TEXT
  - Fast to query

barcode: VARCHAR(50)
  - Why 50? Barcodes usually < 50 chars
  - Prevents huge strings by accident

notes: TEXT
  - Why TEXT? Notes can be long, unpredictable
  - No specific size limit needed
```

---

## Complete Schema Definition

### SQL Schema (Ready to Use!)

```sql
-- ============================================
-- SWADHA INVENTORY DATABASE SCHEMA
-- PostgreSQL 16
-- Created: 2025
-- ============================================

-- Enable UUID extension (for future use)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLE 1: categories
-- Purpose: Product categories (Ear Rings, Bracelets, etc.)
-- ============================================

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups by name
CREATE INDEX idx_categories_name ON categories(name);

-- Sample data
COMMENT ON TABLE categories IS 'Product categories (Ear Rings, Bracelets, etc.)';
COMMENT ON COLUMN categories.id IS 'Unique category identifier';
COMMENT ON COLUMN categories.name IS 'Category name (must be unique)';


-- ============================================
-- TABLE 2: inventory_items
-- Purpose: Individual products in inventory
-- ============================================

CREATE TABLE inventory_items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    item_name VARCHAR(200) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL CHECK (cost_price >= 0),
    selling_price DECIMAL(10,2) NOT NULL CHECK (selling_price >= 0),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    barcode VARCHAR(50) UNIQUE,
    already_in_mybillbook BOOLEAN DEFAULT FALSE,
    mybillbook_sku VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_inventory_category ON inventory_items(category_id);
CREATE INDEX idx_inventory_barcode ON inventory_items(barcode);
CREATE INDEX idx_inventory_mybillbook ON inventory_items(already_in_mybillbook);
CREATE INDEX idx_inventory_price ON inventory_items(selling_price);

-- Composite index for common filter combination
CREATE INDEX idx_inventory_category_mybillbook ON inventory_items(category_id, already_in_mybillbook);

-- Comments
COMMENT ON TABLE inventory_items IS 'Individual products in inventory';
COMMENT ON COLUMN inventory_items.category_id IS 'References categories.id';
COMMENT ON COLUMN inventory_items.cost_price IS 'Purchase/cost price per item';
COMMENT ON COLUMN inventory_items.selling_price IS 'Selling price per item';
COMMENT ON COLUMN inventory_items.barcode IS 'Unique barcode (auto-generated or MyBillBook)';
COMMENT ON COLUMN inventory_items.already_in_mybillbook IS 'TRUE if item exists in MyBillBook';
COMMENT ON COLUMN inventory_items.mybillbook_sku IS 'MyBillBook SKU if already present';


-- ============================================
-- TABLE 3: sync_history
-- Purpose: Track data synchronization events
-- ============================================

CREATE TABLE sync_history (
    id SERIAL PRIMARY KEY,
    sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    items_synced INTEGER NOT NULL,
    source VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('SUCCESS', 'FAILED', 'PARTIAL')),
    error_message TEXT,
    notes TEXT
);

-- Index for querying recent syncs
CREATE INDEX idx_sync_date ON sync_history(sync_date DESC);

-- Comments
COMMENT ON TABLE sync_history IS 'Track data synchronization events from Google Sheets';
COMMENT ON COLUMN sync_history.source IS 'Data source (e.g., "Google Sheets", "Manual Entry")';
COMMENT ON COLUMN sync_history.status IS 'Sync result: SUCCESS, FAILED, or PARTIAL';


-- ============================================
-- TABLE 4: sales (Future Use)
-- Purpose: Track sales transactions
-- ============================================

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    quantity_sold INTEGER NOT NULL CHECK (quantity_sold > 0),
    sale_price DECIMAL(10,2) NOT NULL CHECK (sale_price >= 0),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR(100),
    customer_phone VARCHAR(20),
    payment_method VARCHAR(20) CHECK (payment_method IN ('Cash', 'Card', 'UPI', 'Other')),
    notes TEXT
);

-- Indexes for sales queries
CREATE INDEX idx_sales_item ON sales(item_id);
CREATE INDEX idx_sales_date ON sales(sale_date DESC);
CREATE INDEX idx_sales_customer ON sales(customer_name);

-- Comments
COMMENT ON TABLE sales IS 'Sales transactions (future use)';
COMMENT ON COLUMN sales.sale_price IS 'Actual price sold at (may differ from inventory selling_price)';


-- ============================================
-- VIEWS: Pre-computed queries for dashboards
-- ============================================

-- View 1: Inventory with category names (most common query)
CREATE VIEW v_inventory_full AS
SELECT
    i.id,
    c.name AS category,
    i.item_name,
    i.cost_price,
    i.selling_price,
    i.quantity,
    (i.selling_price - i.cost_price) AS profit_per_item,
    ((i.selling_price - i.cost_price) / i.cost_price * 100) AS profit_margin_percent,
    (i.cost_price * i.quantity) AS total_cost_value,
    (i.selling_price * i.quantity) AS total_selling_value,
    ((i.selling_price - i.cost_price) * i.quantity) AS total_profit_potential,
    i.barcode,
    i.already_in_mybillbook,
    i.mybillbook_sku,
    i.created_at,
    i.updated_at
FROM inventory_items i
JOIN categories c ON i.category_id = c.id;

COMMENT ON VIEW v_inventory_full IS 'Complete inventory with calculations (use this for dashboards)';


-- View 2: Low stock alert
CREATE VIEW v_low_stock AS
SELECT
    c.name AS category,
    i.item_name,
    i.quantity,
    i.selling_price,
    (i.selling_price * i.quantity) AS current_value
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE i.quantity < 5
ORDER BY i.quantity ASC;

COMMENT ON VIEW v_low_stock IS 'Items with quantity < 5 (reorder alert)';


-- View 3: Category summary
CREATE VIEW v_category_summary AS
SELECT
    c.name AS category,
    COUNT(i.id) AS item_count,
    SUM(i.quantity) AS total_quantity,
    SUM(i.cost_price * i.quantity) AS total_cost_value,
    SUM(i.selling_price * i.quantity) AS total_selling_value,
    SUM((i.selling_price - i.cost_price) * i.quantity) AS total_profit_potential
FROM categories c
LEFT JOIN inventory_items i ON c.id = i.category_id
GROUP BY c.id, c.name
ORDER BY total_selling_value DESC;

COMMENT ON VIEW v_category_summary IS 'Summary statistics by category';


-- ============================================
-- FUNCTIONS: Auto-update timestamps
-- ============================================

-- Function to update 'updated_at' timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for categories table
CREATE TRIGGER trigger_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for inventory_items table
CREATE TRIGGER trigger_inventory_updated_at
    BEFORE UPDATE ON inventory_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON FUNCTION update_updated_at_column() IS 'Auto-update updated_at timestamp on UPDATE';


-- ============================================
-- SAMPLE DATA (for testing)
-- ============================================

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
    ('Ear Rings', 'Earring designs'),
    ('Bracelets', 'Bracelet designs'),
    ('Necklaces', 'Necklace designs'),
    ('Rings', 'Ring designs'),
    ('Anklets', 'Anklet designs')
ON CONFLICT (name) DO NOTHING;

-- Insert sample inventory items
INSERT INTO inventory_items
(category_id, item_name, cost_price, selling_price, quantity, barcode, already_in_mybillbook, mybillbook_sku)
VALUES
    (1, 'Ear Rings XCNR', 110.00, 250.00, 4, '84 0110', TRUE, '84 0110'),
    (2, 'Bracelets R AXPZ', 110.00, 250.00, 5, '78 0611', TRUE, '78 0611'),
    (1, 'Ear Rings HXXL', 110.00, 250.00, 4, '24 0118', FALSE, NULL),
    (1, 'Ear Rings GL PWQZ', 45.00, 199.00, 2, '89 5423', FALSE, NULL)
ON CONFLICT (barcode) DO NOTHING;

-- Record initial sync
INSERT INTO sync_history (items_synced, source, status, notes)
VALUES (4, 'Manual Entry', 'SUCCESS', 'Sample data for testing');


-- ============================================
-- SCHEMA COMPLETE!
-- ============================================

-- Verify tables created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

---

## Understanding Relationships

### One-to-Many: Category → Items

**Visual Representation:**
```
CATEGORY: Ear Rings (id=1)
    ├─→ Item: Ear Rings XCNR (category_id=1)
    ├─→ Item: Ear Rings HXXL (category_id=1)
    └─→ Item: Ear Rings GL PWQZ (category_id=1)

CATEGORY: Bracelets (id=2)
    └─→ Item: Bracelets R AXPZ (category_id=2)
```

**In SQL:**
```sql
-- Define relationship with FOREIGN KEY
CREATE TABLE inventory_items (
    ...
    category_id INTEGER REFERENCES categories(id)
    ...
);

-- What this means:
-- category_id MUST exist in categories.id
-- Can't insert item with category_id=999 if category 999 doesn't exist
-- Can't delete category if items still reference it
```

**Querying relationships:**
```sql
-- Get all items in "Ear Rings" category
SELECT *
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE c.name = 'Ear Rings';

-- Count items per category
SELECT
    c.name,
    COUNT(i.id) AS item_count
FROM categories c
LEFT JOIN inventory_items i ON c.id = i.category_id
GROUP BY c.name;
```

### Referential Integrity

**ON DELETE RESTRICT:**
```sql
category_id INTEGER REFERENCES categories(id) ON DELETE RESTRICT

What this does:
  ✓ Prevents deleting a category that has items
  ✓ Ensures data consistency
  ✓ Forces you to delete items first, then category

Example:
  DELETE FROM categories WHERE id = 1;
  → ERROR: items still reference category 1
```

**Alternative options (not recommended for our use):**
```sql
ON DELETE CASCADE  -- Delete items when category deleted (dangerous!)
ON DELETE SET NULL -- Set category_id to NULL (loses relationship)
```

---

## Indexing Strategy

### What is an Index?

**Simple Analogy:**
```
Book without index:
  Find topic "PostgreSQL"
  → Read entire book page by page
  → Takes hours

Book with index:
  Look up "PostgreSQL" in index
  → Index says "Page 342"
  → Jump to page 342
  → Takes seconds

Database works the same way!
```

### Indexes We Created

**1. Primary Key Indexes (Automatic)**
```sql
id SERIAL PRIMARY KEY

PostgreSQL automatically creates index on id
Fastest possible lookup by id
```

**2. Unique Indexes**
```sql
barcode VARCHAR(50) UNIQUE

Automatically creates index
Ensures no duplicate barcodes
Fast lookup by barcode
```

**3. Foreign Key Indexes**
```sql
CREATE INDEX idx_inventory_category ON inventory_items(category_id);

Why?
  - JOIN operations use category_id frequently
  - Without index: Scan entire table (slow!)
  - With index: Jump to matching rows (fast!)
```

**4. Commonly Queried Columns**
```sql
CREATE INDEX idx_inventory_price ON inventory_items(selling_price);

Why?
  - Dashboard queries filter by price
  - "Show items > ₹200"
  - Index makes this instant
```

**5. Composite Indexes**
```sql
CREATE INDEX idx_inventory_category_mybillbook
ON inventory_items(category_id, already_in_mybillbook);

Why?
  - Common query: "Show new items in Ear Rings category"
  - Uses both columns together
  - Composite index faster than two separate indexes
```

### Index Best Practices (2025)

**DO Index:**
```
✓ Primary keys (automatic)
✓ Foreign keys (JOIN performance)
✓ Columns in WHERE clauses
✓ Columns in ORDER BY
✓ Columns in GROUP BY
✓ Unique constraints
```

**DON'T Index:**
```
✗ Small tables (< 1000 rows) - full scan is faster
✗ Columns with low cardinality (e.g., boolean with only TRUE/FALSE)
✗ Columns rarely queried
✗ Every column (indexes slow down INSERT/UPDATE)
```

**How Many Indexes?**
```
Our inventory_items table:
  ✓ 6 indexes total
  ✓ Not too many (< 10 is good)
  ✓ Each serves specific query pattern

General rule:
  - 3-5 indexes per table is typical
  - 10+ indexes = too many (unless huge table)
```

### Monitoring Index Usage

```sql
-- See which indexes are actually used
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan AS index_scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- If index_scans = 0 after months → Remove unused index
```

---

## Testing Your Design

### Test 1: Can You Store Your Data?

**Sample data from your inventory:**
```sql
-- Category
INSERT INTO categories (name) VALUES ('Ear Rings');

-- Item
INSERT INTO inventory_items
(category_id, item_name, cost_price, selling_price, quantity, barcode)
VALUES (1, 'Ear Rings XCNR', 110.00, 250.00, 4, '84 0110');

-- Verify
SELECT * FROM inventory_items;
```

### Test 2: Can You Query Efficiently?

**Common queries:**
```sql
-- 1. Total inventory value
SELECT SUM(selling_price * quantity) FROM inventory_items;

-- 2. Items by category
SELECT c.name, COUNT(i.id)
FROM categories c
LEFT JOIN inventory_items i ON c.id = i.category_id
GROUP BY c.name;

-- 3. Low stock
SELECT * FROM v_low_stock;

-- 4. Profit margins
SELECT item_name, profit_margin_percent FROM v_inventory_full;
```

### Test 3: Can You Handle Edge Cases?

**Test constraints:**
```sql
-- Try negative price (should fail)
INSERT INTO inventory_items (category_id, item_name, cost_price, selling_price, quantity)
VALUES (1, 'Test', -100, 200, 1);
-- ERROR: CHECK constraint violation

-- Try duplicate barcode (should fail)
INSERT INTO inventory_items (category_id, item_name, cost_price, selling_price, quantity, barcode)
VALUES (1, 'Test', 100, 200, 1, '84 0110');
-- ERROR: UNIQUE constraint violation

-- Try invalid category (should fail)
INSERT INTO inventory_items (category_id, item_name, cost_price, selling_price, quantity)
VALUES (999, 'Test', 100, 200, 1);
-- ERROR: FOREIGN KEY constraint violation

All good! Constraints working ✓
```

### Test 4: Performance Test

```sql
-- Explain query plan (see if indexes used)
EXPLAIN ANALYZE
SELECT * FROM inventory_items WHERE category_id = 1;

-- Look for:
-- "Index Scan using idx_inventory_category" ✓ Good!
-- "Seq Scan on inventory_items" ✗ Bad (full table scan)
```

---

## Migration Considerations

### From Google Sheets to PostgreSQL

**What changes:**
```
Google Sheets:
  - Formulas: =C2*D2
  - Calculated columns stored

PostgreSQL:
  - Views: SELECT cost_price * quantity
  - Calculated on-the-fly (not stored)
  - Always accurate (no stale data)
```

**Mapping:**
```
Google Sheets Column → PostgreSQL Column

A (Type)                 → categories.name + inventory_items.category_id
B (Name)                 → inventory_items.item_name
C (Cost Price)           → inventory_items.cost_price
D (Quantity)             → inventory_items.quantity
E (Selling Price)        → inventory_items.selling_price
F (Total Cost)           → CALCULATED: cost_price * quantity
G (Total Selling)        → CALCULATED: selling_price * quantity
H (Barcode)              → inventory_items.barcode
I (Already Present)      → inventory_items.already_in_mybillbook
J (Inventory Barcode)    → inventory_items.mybillbook_sku
```

### Data Normalization

**Before (Denormalized - Google Sheets):**
```
Type       | Name           | Cost | Qty | Price
-----------|----------------|------|-----|------
Ear Rings  | Ear Rings XCNR | 110  | 4   | 250
Ear Rings  | Ear Rings HXXL | 110  | 4   | 250
Ear Rings  | Ear Rings GL   | 45   | 2   | 199

"Ear Rings" repeated 3 times (wastes space)
```

**After (Normalized - PostgreSQL):**
```
categories:
id | name
---|----------
1  | Ear Rings

inventory_items:
id | category_id | name           | cost | qty | price
---|-------------|----------------|------|-----|------
1  | 1           | Ear Rings XCNR | 110  | 4   | 250
2  | 1           | Ear Rings HXXL | 110  | 4   | 250
3  | 1           | Ear Rings GL   | 45   | 2   | 199

"Ear Rings" stored ONCE
Items reference it by id
```

**Benefits:**
```
✓ Less storage space
✓ Update category name once, affects all items
✓ No typos ("Ear Rings" vs "Ear Ring" vs "EarRings")
✓ Faster queries (smaller tables)
```

---

## Views for Dashboards

### Why Use Views?

**Instead of:**
```sql
-- Writing this query every time:
SELECT
    c.name,
    i.item_name,
    (i.selling_price - i.cost_price) AS profit,
    ((i.selling_price - i.cost_price) / i.cost_price * 100) AS margin
FROM inventory_items i
JOIN categories c ON i.category_id = c.id;
```

**Use view:**
```sql
-- Create once:
CREATE VIEW v_inventory_full AS ...

-- Use everywhere:
SELECT * FROM v_inventory_full;
SELECT * FROM v_inventory_full WHERE profit > 100;
SELECT category, AVG(margin) FROM v_inventory_full GROUP BY category;
```

**Benefits:**
```
✓ Simpler queries
✓ Consistent calculations
✓ Easier for Metabase (just select from view)
✓ Centralized logic
```

### Views We Created

**1. v_inventory_full**
```sql
Purpose: Main view for dashboards
Contains: All inventory + calculations
Use for: Most dashboard charts

Example queries:
  - SELECT * FROM v_inventory_full
  - SELECT category, SUM(total_profit_potential) FROM v_inventory_full GROUP BY category
  - SELECT * FROM v_inventory_full WHERE quantity < 5
```

**2. v_low_stock**
```sql
Purpose: Quick alert for low stock items
Pre-filtered: quantity < 5
Use for: Stock management dashboard

Example:
  - SELECT * FROM v_low_stock ORDER BY quantity
```

**3. v_category_summary**
```sql
Purpose: Category-level statistics
Pre-aggregated: Counts, sums, totals
Use for: Category comparison charts

Example:
  - SELECT * FROM v_category_summary ORDER BY total_selling_value DESC
```

---

## Advanced Features

### Triggers (Auto-Update Timestamps)

**What they do:**
```sql
-- When you update a row:
UPDATE inventory_items SET quantity = 10 WHERE id = 1;

-- Trigger automatically runs:
updated_at = CURRENT_TIMESTAMP

-- You don't have to remember to update timestamp!
```

**How it works:**
```sql
-- 1. Create function
CREATE FUNCTION update_updated_at_column() ...

-- 2. Attach to table
CREATE TRIGGER trigger_inventory_updated_at
    BEFORE UPDATE ON inventory_items
    ...

-- 3. Profit!
-- Timestamps always accurate, automatically
```

### Constraints (Data Validation)

**CHECK Constraints:**
```sql
cost_price DECIMAL(10,2) CHECK (cost_price >= 0)

Prevents:
  - Negative prices
  - Invalid data entry
  - Bugs in application code

If you try:
  INSERT INTO inventory_items (cost_price) VALUES (-100);

PostgreSQL says:
  ERROR: CHECK constraint violated
```

**NOT NULL Constraints:**
```sql
item_name VARCHAR(200) NOT NULL

Prevents:
  - Forgetting to enter item name
  - Empty/null products

If you try:
  INSERT INTO inventory_items (item_name) VALUES (NULL);

PostgreSQL says:
  ERROR: NOT NULL constraint violated
```

---

## Schema Evolution

### Future Additions

**When you need more features:**

```sql
-- Add customer table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

-- Link sales to customers
ALTER TABLE sales
ADD COLUMN customer_id INTEGER REFERENCES customers(id);

-- Add supplier table
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20)
);

-- Track which supplier provides which item
CREATE TABLE item_suppliers (
    item_id INTEGER REFERENCES inventory_items(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    cost_from_supplier DECIMAL(10,2),
    PRIMARY KEY (item_id, supplier_id)
);
```

**Schema is flexible:**
```
Start simple (4 tables)
Add as you grow (customers, suppliers, etc.)
Database adapts to your business
```

---

## Comparison: Sheets vs Database

| Feature | Google Sheets | PostgreSQL |
|---------|---------------|------------|
| **Data Size** | ~5,000 rows max (slow after) | Millions of rows (fast!) |
| **Concurrent Users** | Limited (conflicts) | 100s simultaneously |
| **Queries** | Basic filters | Complex SQL |
| **Calculations** | Manual formulas | Automatic views |
| **Backups** | Manual exports | Automatic daily |
| **Performance** | Slow with 1000+ rows | Fast with millions |
| **Data Integrity** | Manual checking | Automatic constraints |
| **Relationships** | Manual (VLOOKUP) | Automatic (FOREIGN KEY) |
| **Access Control** | Share entire sheet | Per-table permissions |
| **Cost** | Free | $0 (Free Tier), then ~$14/month |

**When to use each:**
```
Google Sheets:
  ✓ Quick data entry
  ✓ Team collaboration on input
  ✓ Visual exploration
  ✓ Small datasets (< 1000 rows)

PostgreSQL:
  ✓ Large datasets
  ✓ Complex queries
  ✓ Multiple applications
  ✓ Production systems
  ✓ Dashboards (Metabase)
```

**Our approach:**
```
Google Sheets: Data entry (Phase 1)
      ↓
PostgreSQL: Storage & analysis (Phase 2)
      ↓
Metabase: Visualization (Phase 2)

Best of all worlds!
```

---

## Summary & Next Steps

### What You Learned

```
✓ Database design fundamentals
✓ Analyzing data requirements
✓ Creating tables with proper data types
✓ Defining relationships (foreign keys)
✓ Indexing for performance
✓ Using views for dashboards
✓ Data constraints for integrity
✓ Migration planning
```

### Your Schema is Ready!

**You now have:**
```
✓ Complete SQL schema (copy-paste ready)
✓ 4 tables designed
✓ 3 views for dashboards
✓ Proper indexes for performance
✓ Constraints for data integrity
✓ Auto-updating timestamps
✓ Sample data for testing
```

### What to Do Next

**Option 1: Test Locally (Recommended)**
```
1. Install PostgreSQL on your computer
2. Create database: inventory_test
3. Run the schema SQL (entire script above)
4. Insert sample data
5. Try queries
6. Experiment!

Time: 2-3 hours
Benefit: Confident before AWS
```

**Option 2: Wait for AWS**
```
1. Save schema SQL to file: database_schema.sql
2. When AWS RDS ready, run schema
3. Create tables in cloud

Time: 5 minutes on AWS day
```

**Option 3: Continue Learning**
```
1. Move to Lesson 5: Writing migration script
2. Prepare Python code
3. Ready to execute when AWS is live

Time: Ongoing preparation
```

---

## Practice Exercises

### Exercise 1: Modify Schema

**Task:** Add "color" field to inventory items

```sql
-- Solution:
ALTER TABLE inventory_items
ADD COLUMN color VARCHAR(50);

-- Add sample colors:
UPDATE inventory_items SET color = 'Gold' WHERE id = 1;
UPDATE inventory_items SET color = 'Silver' WHERE id = 2;
```

### Exercise 2: Write Queries

**Task:** Find total value by category

```sql
-- Solution:
SELECT
    c.name AS category,
    SUM(i.selling_price * i.quantity) AS total_value
FROM categories c
JOIN inventory_items i ON c.id = i.category_id
GROUP BY c.name
ORDER BY total_value DESC;
```

### Exercise 3: Create New View

**Task:** View showing only new items (not in MyBillBook)

```sql
-- Solution:
CREATE VIEW v_new_items AS
SELECT
    c.name AS category,
    i.item_name,
    i.selling_price,
    i.quantity
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE i.already_in_mybillbook = FALSE
ORDER BY i.selling_price DESC;

-- Use it:
SELECT * FROM v_new_items;
```

---

## Troubleshooting

**Problem: Can't create table**
```sql
-- Error: "relation already exists"
-- Solution: Table already created, drop it first
DROP TABLE IF EXISTS inventory_items CASCADE;
-- Then create again
```

**Problem: Foreign key error**
```sql
-- Error: "violates foreign key constraint"
-- Solution: Create categories first, then inventory_items
-- Order matters!

-- Correct order:
1. CREATE categories
2. CREATE inventory_items (references categories)
3. CREATE sales (references inventory_items)
```

**Problem: Index not used**
```sql
-- Check query plan:
EXPLAIN ANALYZE SELECT * FROM inventory_items WHERE selling_price > 200;

-- If seeing "Seq Scan" instead of "Index Scan":
-- 1. Table too small (< 1000 rows) - index not worth it
-- 2. Index missing - create it
-- 3. Statistics outdated - run ANALYZE
ANALYZE inventory_items;
```

---

## Resources & References

**Official Documentation:**
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)

**Best Practices (2025):**
- [PostgreSQL Best Practices 2025](https://www.instaclustr.com/education/postgresql/top-10-postgresql-best-practices-for-2025/)
- [Database Schema Design Guide](https://www.bytebase.com/blog/top-database-schema-design-best-practices/)
- [PostgreSQL Indexing Guide](https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide)

**Learning Resources:**
- SQLBolt: https://sqlbolt.com/
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/
- DB Fiddle (Online Practice): https://www.db-fiddle.com/

---

## Files to Save

**Create these files in your project:**

**1. `phase2/database_schema.sql`**
- Complete schema from this lesson
- Ready to run on AWS RDS

**2. `phase2/sample_queries.sql`**
- Practice queries
- Dashboard query templates

**3. `phase2/schema_notes.md`**
- Your notes about the design
- Why you made certain choices
- Future modifications planned

---

**Congratulations!** Your database is designed and ready. When AWS is live, you'll just run one SQL script and your entire database structure is created in seconds!

**Next Lesson:** Writing the Python migration script to move data from Google Sheets to PostgreSQL.

Ready when you are!
