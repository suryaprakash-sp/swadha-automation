# Phase 2 - Pre-AWS Preparation Checklist
## Everything You Can Do BEFORE Creating AWS Account

---

## Why This Matters

```
Your 6-month Free Tier timer starts when you create AWS account.
Every day counts!

If you prepare first:
  Day 1 of AWS: Hit the ground running
  Week 1: Database live, data migrated
  Week 2: Dashboards built and in use
  Remaining time: Using, learning, iterating

If you DON'T prepare:
  Day 1-7: Learning PostgreSQL basics
  Day 8-14: Designing database schema
  Day 15-21: Writing migration scripts
  Day 22+: Finally starting...
  Result: Wasted 3 weeks of your 6 months!
```

**Goal:** Be 100% ready so on Day 1 of AWS, you just execute.

---

## Complete Pre-AWS Preparation Timeline

### Phase A: Learning Fundamentals (1-2 weeks)
Do this before AWS account creation

### Phase B: Design & Planning (3-5 days)
Complete database and dashboard design

### Phase C: Code Preparation (3-5 days)
Write all scripts (just add AWS connection details later)

### Phase D: Local Testing (2-3 days)
Test everything locally with PostgreSQL

### Phase E: Final Readiness (1 day)
Checklist verification

**Total Preparation Time: 2-3 weeks**
**AWS Time Saved: 2-3 weeks out of 6 months = 10-12% saved!**

---

## Phase A: Learning Fundamentals

### 1. Learn PostgreSQL Basics

**Why:** You'll be working with PostgreSQL database daily.

**What to learn:**

```sql
Basic Concepts:
  ✓ What is SQL?
  ✓ What is a relational database?
  ✓ Tables, rows, columns
  ✓ Primary keys, foreign keys
  ✓ Data types (INTEGER, VARCHAR, DECIMAL, TIMESTAMP)

Basic SQL Commands:
  ✓ SELECT - Query data
  ✓ INSERT - Add data
  ✓ UPDATE - Modify data
  ✓ DELETE - Remove data
  ✓ WHERE - Filter results
  ✓ JOIN - Combine tables
  ✓ GROUP BY - Aggregate data
  ✓ ORDER BY - Sort results
```

**Free Resources (No AWS needed):**

1. **Interactive Learning (Recommended):**
   - SQLBolt: https://sqlbolt.com/
   - W3Schools SQL: https://www.w3schools.com/sql/
   - Khan Academy SQL: https://www.khanacademy.org/computing/computer-programming/sql
   - Time: 3-4 hours total

2. **Video Tutorials:**
   - freeCodeCamp PostgreSQL Course (YouTube)
   - Programming with Mosh - PostgreSQL Tutorial
   - Time: 2-3 hours

3. **Practice Playground:**
   - https://www.db-fiddle.com/ (online SQL playground)
   - Try PostgreSQL queries without installing anything!

**Hands-on Exercise:**
```sql
-- Try these queries on db-fiddle.com
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    quantity INTEGER
);

INSERT INTO products (name, price, quantity) VALUES
    ('Ear Rings', 250.00, 4),
    ('Bracelets', 250.00, 5);

SELECT * FROM products;
SELECT * FROM products WHERE price > 200;
SELECT SUM(quantity) FROM products;
```

**Time Investment:** 5-8 hours
**Benefit:** You'll understand every SQL command we use

---

### 2. Install PostgreSQL Locally (Optional but Recommended)

**Why:** Practice on your computer before AWS. No time wasted learning when AWS is running.

**How to Install:**

**Windows:**
```
1. Download: https://www.postgresql.org/download/windows/
2. Choose: PostgreSQL 16 (latest stable)
3. Download installer
4. Run installer:
   - Password: (create strong password, write it down)
   - Port: 5432 (default)
   - Install pgAdmin (graphical tool)
5. Complete installation (takes 5 minutes)
```

**After Installation:**
```
1. Open pgAdmin 4 (installed with PostgreSQL)
2. Connect to local server (localhost)
3. Password: (the one you set during install)
4. Create test database:
   - Right-click "Databases"
   - Create → Database
   - Name: inventory_test
   - Save
5. Now you can practice SQL!
```

**Practice Tasks:**
```
1. Create tables matching your inventory structure
2. Insert sample data from your Google Sheets
3. Try queries:
   - Find items with price > 200
   - Calculate total inventory value
   - Group by category
   - Practice JOIN operations
4. Get comfortable with pgAdmin interface
```

**Time Investment:** 2 hours (installation + practice)
**Benefit:** Confident with PostgreSQL before AWS

---

### 3. Learn Metabase Basics

**Why:** You'll build dashboards with Metabase. Learn interface before AWS.

**What to learn:**

```
Metabase Concepts:
  ✓ What is Metabase?
  ✓ Questions (queries)
  ✓ Dashboards (collections of charts)
  ✓ Filters
  ✓ Chart types (bar, line, pie, table, etc.)
  ✓ Sharing dashboards
```

**Free Resources:**

1. **Official Demo:**
   - Go to: https://www.metabase.com/demo/
   - Play with sample data
   - Click around, explore
   - Try creating questions
   - No signup needed!

2. **Video Tutorials:**
   - Metabase Official YouTube Channel
   - "Getting Started with Metabase" series
   - Time: 1-2 hours

3. **Documentation:**
   - https://www.metabase.com/docs/latest/
   - Read "Getting Started" section
   - Bookmark for reference

**Hands-on Exercise:**
```
1. Open Metabase demo
2. Create a simple question:
   - "Show me all orders"
   - Group by product
   - Show as bar chart
3. Create a dashboard:
   - Add 3-4 questions
   - Arrange layout
   - Add filters
4. Explore different chart types
5. Take screenshots of dashboard ideas
```

**Time Investment:** 2-3 hours
**Benefit:** Know what you want to build before starting

---

### 4. Understand AWS Concepts (Theory Only)

**Why:** So you're not confused when navigating AWS Console.

**What to learn:**

```
Core Concepts:
  ✓ What is RDS? (managed database)
  ✓ What is EC2? (virtual server)
  ✓ What is VPC? (private network)
  ✓ What are security groups? (firewall rules)
  ✓ What is IAM? (user management)
  ✓ Regions vs Availability Zones
```

**Free Resources:**

1. **AWS Training (Free):**
   - AWS Skill Builder: https://skillbuilder.aws/
   - Create free account (NOT AWS account, just training)
   - Take courses:
     - "AWS Cloud Practitioner Essentials" (free)
     - "Getting Started with Databases" (free)
   - Time: 4-6 hours

2. **YouTube:**
   - "AWS Explained in 10 Minutes"
   - "What is Amazon RDS?"
   - "What is Amazon EC2?"

**Time Investment:** 3-4 hours
**Benefit:** Confident navigating AWS Console from day 1

---

## Phase B: Design & Planning

### 5. Design Your Database Schema

**Why:** Know EXACTLY what tables you need before creating database.

**What you have (from Phase 1):**

```
Your inventory data columns:
  A: Type (Category)
  B: Name
  C: Per Item (Cost Price)
  D: Quantity
  E: Per Item (Selling Price)
  F: Total Cost Price
  G: Total Selling Price
  H: Barcode (generated)
  I: Already Present (Yes/No)
  J: Inventory Item Barcode (actual)
```

**Database Design Task:**

**Table 1: Categories**
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Examples:
-- 1, "Ear Rings", 2025-12-22 10:30:00
-- 2, "Bracelets", 2025-12-22 10:30:00
```

**Table 2: Inventory Items**
```sql
CREATE TABLE inventory_items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    item_name VARCHAR(200) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    barcode VARCHAR(50) UNIQUE,
    already_in_mybillbook BOOLEAN DEFAULT FALSE,
    mybillbook_sku VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example:
-- 1, 1, "Ear Rings XCNR", 110.00, 250.00, 4, "84 0110", TRUE, "84 0110", ...
```

**Table 3: Sync History** (track when data was updated)
```sql
CREATE TABLE sync_history (
    id SERIAL PRIMARY KEY,
    sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    items_synced INTEGER,
    source VARCHAR(50),
    status VARCHAR(20)
);

-- Track every time you update from Google Sheets
```

**Table 4: Sales** (future - when you track sales)
```sql
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES inventory_items(id),
    quantity_sold INTEGER NOT NULL,
    sale_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR(100),
    notes TEXT
);

-- For future use
```

**Your Task:**
1. Copy these schemas to a text file
2. Modify if needed for your business
3. Add any additional columns you want
4. Understand what each column means
5. Save as: `database_schema.sql`

**Time Investment:** 2-3 hours (design + document)
**Benefit:** Clear plan, no guesswork on AWS

---

### 6. Design Your Dashboards

**Why:** Know what metrics matter BEFORE building.

**Dashboard Ideas for Jewelry Business:**

**Dashboard 1: Inventory Overview**
```
Metrics:
  ┌─────────────────┬─────────────────┐
  │ Total Items: 71 │ Total Value:    │
  │                 │ ₹45,000         │
  ├─────────────────┼─────────────────┤
  │ Low Stock: 5    │ New Items: 69   │
  └─────────────────┴─────────────────┘

Charts:
  ┌─────────────────────────────────────┐
  │ Inventory by Category (Pie Chart)   │
  │ • Ear Rings: 40%                    │
  │ • Bracelets: 30%                    │
  │ • Necklaces: 20%                    │
  │ • Others: 10%                       │
  └─────────────────────────────────────┘

  ┌─────────────────────────────────────┐
  │ Items by Price Range (Bar Chart)    │
  │ < ₹100:    ████████ 20              │
  │ ₹100-200:  ████████████ 30          │
  │ ₹200-500:  ████████ 15              │
  │ > ₹500:    ████ 6                   │
  └─────────────────────────────────────┘
```

**Dashboard 2: Profit Analysis**
```
Metrics:
  ┌─────────────────────────────────────┐
  │ Average Profit Margin: 127%         │
  │ Total Potential Profit: ₹32,000     │
  └─────────────────────────────────────┘

Charts:
  ┌─────────────────────────────────────┐
  │ Top 10 Most Profitable Items        │
  │ (Table sorted by profit margin)     │
  └─────────────────────────────────────┘

  ┌─────────────────────────────────────┐
  │ Cost vs Selling Price Comparison    │
  │ (Scatter plot)                      │
  └─────────────────────────────────────┘
```

**Dashboard 3: Stock Management**
```
Charts:
  ┌─────────────────────────────────────┐
  │ Low Stock Alert (Items with qty < 5)│
  │ Table with reorder suggestions      │
  └─────────────────────────────────────┘

  ┌─────────────────────────────────────┐
  │ MyBillBook Integration Status       │
  │ Pie: Already in MyBillBook vs New   │
  └─────────────────────────────────────┘
```

**Your Task:**
1. Sketch dashboards on paper or in Excel
2. List metrics that matter to your business
3. Choose chart types
4. Prioritize: Which dashboards to build first?
5. Save sketches/notes

**Time Investment:** 2-3 hours
**Benefit:** Clear vision of end goal

---

## Phase C: Code Preparation

### 7. Write Data Migration Script (90% Complete)

**Why:** Have script ready, just plug in AWS connection details later.

**File to create:** `migrate_to_postgres.py`

```python
"""
Data Migration Script: Google Sheets → PostgreSQL
Preparation version - add AWS connection details later
"""

import psycopg2
from utils.sheets import SheetsManager
from config import SHEET_INVENTORY

# TODO: Fill these in after AWS RDS is created
DB_CONFIG = {
    'host': 'YOUR_AWS_RDS_ENDPOINT_HERE',  # Will get from AWS
    'port': 5432,
    'database': 'inventory_db',
    'user': 'postgres',
    'password': 'YOUR_DB_PASSWORD_HERE'  # Set during RDS creation
}

def connect_to_database():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Connected to database")
        return conn
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return None

def create_tables(conn):
    """Create database tables if they don't exist"""
    cursor = conn.cursor()

    # Create categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Create inventory_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_items (
            id SERIAL PRIMARY KEY,
            category_id INTEGER REFERENCES categories(id),
            item_name VARCHAR(200) NOT NULL,
            cost_price DECIMAL(10,2) NOT NULL,
            selling_price DECIMAL(10,2) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            barcode VARCHAR(50) UNIQUE,
            already_in_mybillbook BOOLEAN DEFAULT FALSE,
            mybillbook_sku VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Create sync_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_history (
            id SERIAL PRIMARY KEY,
            sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            items_synced INTEGER,
            source VARCHAR(50),
            status VARCHAR(20)
        );
    """)

    conn.commit()
    print("✓ Tables created successfully")

def get_or_create_category(cursor, category_name):
    """Get category ID, create if doesn't exist"""
    cursor.execute(
        "SELECT id FROM categories WHERE name = %s",
        (category_name,)
    )
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO categories (name) VALUES (%s) RETURNING id",
            (category_name,)
        )
        return cursor.fetchone()[0]

def migrate_inventory_data(conn):
    """Read from Google Sheets and migrate to PostgreSQL"""
    sheets = SheetsManager()

    # Read inventory data
    print("Reading data from Google Sheets...")
    data = sheets.read_sheet(SHEET_INVENTORY)

    if not data or len(data) < 2:
        print("✗ No data found in Inventory sheet")
        return

    rows = data[1:]  # Skip header
    print(f"Found {len(rows)} items to migrate")

    cursor = conn.cursor()
    migrated_count = 0

    for row in rows:
        # Ensure row has enough columns
        while len(row) < 10:
            row.append("")

        # Extract data
        category_name = row[0]  # Column A: Type
        item_name = row[1]      # Column B: Name
        cost_price = float(row[2].replace(',', '')) if row[2] else 0
        quantity = int(float(row[3].replace(',', ''))) if row[3] else 0
        selling_price = float(row[4].replace(',', '')) if row[4] else 0
        barcode = row[7]        # Column H: Barcode
        already_present = row[8].lower() == 'yes' if row[8] else False
        mybillbook_sku = row[9]  # Column J: Inventory Item Barcode

        # Get or create category
        category_id = get_or_create_category(cursor, category_name)

        # Insert inventory item
        cursor.execute("""
            INSERT INTO inventory_items
            (category_id, item_name, cost_price, selling_price, quantity,
             barcode, already_in_mybillbook, mybillbook_sku)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (barcode) DO UPDATE SET
                quantity = EXCLUDED.quantity,
                cost_price = EXCLUDED.cost_price,
                selling_price = EXCLUDED.selling_price,
                updated_at = CURRENT_TIMESTAMP
        """, (category_id, item_name, cost_price, selling_price, quantity,
              barcode, already_present, mybillbook_sku))

        migrated_count += 1

    # Record sync history
    cursor.execute("""
        INSERT INTO sync_history (items_synced, source, status)
        VALUES (%s, %s, %s)
    """, (migrated_count, 'Google Sheets', 'SUCCESS'))

    conn.commit()
    print(f"✓ Successfully migrated {migrated_count} items")

def verify_migration(conn):
    """Verify data was migrated correctly"""
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inventory_items")
    item_count = cursor.fetchone()[0]

    print(f"\nMigration Summary:")
    print(f"  Categories: {category_count}")
    print(f"  Inventory Items: {item_count}")

    # Show sample data
    cursor.execute("""
        SELECT c.name, i.item_name, i.cost_price, i.selling_price, i.quantity
        FROM inventory_items i
        JOIN categories c ON i.category_id = c.id
        LIMIT 5
    """)

    print(f"\nSample Items:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} - Cost: ₹{row[2]}, Sell: ₹{row[3]}, Qty: {row[4]}")

def main():
    """Main migration function"""
    print("=== PostgreSQL Migration Script ===\n")

    # Connect to database
    conn = connect_to_database()
    if not conn:
        return

    try:
        # Create tables
        create_tables(conn)

        # Migrate data
        migrate_inventory_data(conn)

        # Verify
        verify_migration(conn)

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("\n✓ Database connection closed")

if __name__ == "__main__":
    main()
```

**Your Task:**
1. Create this file in your project: `migrate_to_postgres.py`
2. Review the code, understand what it does
3. Test the logic (everything except actual DB connection)
4. Later: Just fill in AWS RDS endpoint and password

**Time Investment:** 2-3 hours (write + understand)
**Benefit:** Ready to migrate data on AWS Day 1

---

### 8. Install Required Python Packages

**Why:** Have everything ready before AWS.

**Packages needed:**

```bash
# PostgreSQL adapter for Python
pip install psycopg2-binary

# Or if that doesn't work:
pip install psycopg2

# Already have from Phase 1:
# - google-auth
# - google-auth-oauthlib
# - google-auth-httplib2
# - google-api-python-client
```

**Test installation:**
```python
# test_imports.py
try:
    import psycopg2
    print("✓ psycopg2 installed correctly")
except ImportError:
    print("✗ psycopg2 not found - install it!")

try:
    from utils.sheets import SheetsManager
    print("✓ Google Sheets integration working")
except ImportError:
    print("✗ Google Sheets utils missing")
```

**Time Investment:** 15 minutes
**Benefit:** No surprises on AWS day

---

### 9. Create SQL Query Templates

**Why:** Have queries ready for Metabase dashboards.

**File to create:** `dashboard_queries.sql`

```sql
-- Dashboard Queries for Metabase
-- Copy-paste these when creating Metabase questions

-- === INVENTORY OVERVIEW ===

-- Total Items
SELECT COUNT(*) as total_items FROM inventory_items;

-- Total Inventory Value (Cost)
SELECT SUM(cost_price * quantity) as total_cost_value FROM inventory_items;

-- Total Inventory Value (Selling)
SELECT SUM(selling_price * quantity) as total_selling_value FROM inventory_items;

-- Potential Profit
SELECT
    SUM((selling_price - cost_price) * quantity) as potential_profit
FROM inventory_items;

-- Average Profit Margin
SELECT
    AVG(((selling_price - cost_price) / cost_price * 100)) as avg_profit_margin_percent
FROM inventory_items
WHERE cost_price > 0;


-- === CATEGORY ANALYSIS ===

-- Items by Category
SELECT
    c.name as category,
    COUNT(*) as item_count,
    SUM(i.quantity) as total_quantity
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
GROUP BY c.name
ORDER BY item_count DESC;

-- Value by Category
SELECT
    c.name as category,
    SUM(i.selling_price * i.quantity) as total_value
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
GROUP BY c.name
ORDER BY total_value DESC;


-- === STOCK MANAGEMENT ===

-- Low Stock Items (quantity < 5)
SELECT
    c.name as category,
    i.item_name,
    i.quantity,
    i.selling_price
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE i.quantity < 5
ORDER BY i.quantity ASC;

-- Out of Stock Items
SELECT
    c.name as category,
    i.item_name,
    i.cost_price
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE i.quantity = 0;


-- === PROFIT ANALYSIS ===

-- Top 10 Most Profitable Items (by margin)
SELECT
    c.name as category,
    i.item_name,
    i.cost_price,
    i.selling_price,
    ((i.selling_price - i.cost_price) / i.cost_price * 100) as profit_margin_percent,
    ((i.selling_price - i.cost_price) * i.quantity) as total_profit_potential
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE i.cost_price > 0
ORDER BY profit_margin_percent DESC
LIMIT 10;

-- Items by Price Range
SELECT
    CASE
        WHEN selling_price < 100 THEN '< ₹100'
        WHEN selling_price BETWEEN 100 AND 200 THEN '₹100-200'
        WHEN selling_price BETWEEN 200 AND 500 THEN '₹200-500'
        ELSE '> ₹500'
    END as price_range,
    COUNT(*) as item_count
FROM inventory_items
GROUP BY price_range
ORDER BY MIN(selling_price);


-- === MYBILLBOOK INTEGRATION ===

-- MyBillBook Status
SELECT
    CASE
        WHEN already_in_mybillbook THEN 'Already in MyBillBook'
        ELSE 'New Items'
    END as status,
    COUNT(*) as count
FROM inventory_items
GROUP BY already_in_mybillbook;

-- New Items to Add to MyBillBook
SELECT
    c.name as category,
    i.item_name,
    i.selling_price,
    i.quantity
FROM inventory_items i
JOIN categories c ON i.category_id = c.id
WHERE i.already_in_mybillbook = FALSE
ORDER BY i.selling_price DESC;


-- === SYNC HISTORY ===

-- Recent Syncs
SELECT
    sync_date,
    items_synced,
    source,
    status
FROM sync_history
ORDER BY sync_date DESC
LIMIT 10;
```

**Your Task:**
1. Create this file
2. Understand each query
3. Test queries if you have local PostgreSQL
4. Later: Use these in Metabase

**Time Investment:** 1 hour
**Benefit:** Instant dashboard creation on AWS

---

## Phase D: Local Testing

### 10. Test Everything Locally

**Why:** Fix bugs before AWS timer starts.

**If you installed PostgreSQL locally:**

**Test 1: Create Test Database**
```sql
-- In pgAdmin or command line
CREATE DATABASE inventory_test;
```

**Test 2: Run Migration Script**
```bash
# Update DB_CONFIG in migrate_to_postgres.py to local:
# host: 'localhost'
# database: 'inventory_test'
# user: 'postgres'
# password: 'your_local_password'

python migrate_to_postgres.py
```

**Test 3: Verify Data**
```sql
-- In pgAdmin, run queries:
SELECT COUNT(*) FROM inventory_items;
SELECT * FROM inventory_items LIMIT 10;
```

**Test 4: Test All Dashboard Queries**
```sql
-- Copy queries from dashboard_queries.sql
-- Run each one
-- Verify results make sense
```

**Test 5: Practice Modifications**
```sql
-- Try updating data
UPDATE inventory_items
SET quantity = quantity + 10
WHERE id = 1;

-- Try adding new item
INSERT INTO inventory_items (category_id, item_name, cost_price, selling_price, quantity)
VALUES (1, 'Test Item', 100.00, 200.00, 5);

-- Delete test item
DELETE FROM inventory_items WHERE item_name = 'Test Item';
```

**Time Investment:** 3-4 hours
**Benefit:** Zero learning curve on AWS

---

**If you DIDN'T install PostgreSQL locally:**

Use online SQL playground:

1. Go to: https://www.db-fiddle.com/
2. Select "PostgreSQL 16"
3. Copy table creation SQL from your schema
4. Add sample data manually
5. Test queries

Limited but better than nothing!

---

## Phase E: Final Readiness

### 11. Create Project Checklist

**File to create:** `aws_day1_checklist.md`

```markdown
# AWS Day 1 Execution Checklist

## Hour 1: Account Setup
- [ ] Create AWS account
- [ ] Complete email verification
- [ ] Complete phone verification
- [ ] Add payment method (credit card)
- [ ] Choose FREE PLAN (not Paid!)
- [ ] Verify region set to ap-south-1 (Mumbai)

## Hour 2: Security & Billing
- [ ] Enable MFA on root account
- [ ] Create billing alert: $1
- [ ] Create billing alert: $5
- [ ] Create billing alert: $10
- [ ] Create billing alert: $25
- [ ] Verify $100 credits received

## Hour 3: Onboarding Tasks ($100 extra credits)
- [ ] Task 1: Launch EC2 instance ($20)
- [ ] Task 2: Create RDS database ($20)
- [ ] Task 3: Create Lambda function ($20)
- [ ] Task 4: Use Bedrock playground ($20)
- [ ] Task 5: Create budget ($20) - already done!
- [ ] Verify total credits: $200

## Hour 4-5: RDS Database Setup
- [ ] Create RDS PostgreSQL database (db.t3.micro)
- [ ] Note down endpoint URL
- [ ] Note down password
- [ ] Configure security group (allow connections)
- [ ] Test connection from local computer

## Hour 6-7: Data Migration
- [ ] Update migrate_to_postgres.py with RDS endpoint
- [ ] Run migration script
- [ ] Verify data migrated correctly
- [ ] Check categories table
- [ ] Check inventory_items table
- [ ] Run sample queries

## Day 2: EC2 & Metabase
- [ ] Launch EC2 instance (t3.micro)
- [ ] Install Metabase
- [ ] Connect Metabase to RDS
- [ ] Create first dashboard

## Day 3-4: Dashboard Building
- [ ] Dashboard 1: Inventory Overview
- [ ] Dashboard 2: Profit Analysis
- [ ] Dashboard 3: Stock Management
- [ ] Test all filters and charts

## Day 5: Documentation & Training
- [ ] Document RDS connection details
- [ ] Document Metabase URL
- [ ] Create user guide for team
- [ ] Backup dashboard configs

## Week 2+: Use & Iterate
- [ ] Use dashboards daily
- [ ] Collect feedback
- [ ] Add new metrics as needed
- [ ] Monitor AWS costs weekly
```

**Time Investment:** 30 minutes
**Benefit:** Clear execution plan

---

### 12. Prepare All Files

**Create project structure:**

```
C:\swadha-automation\
  ├─ phase2/                          ← New folder
  │   ├─ migrate_to_postgres.py       ← Migration script
  │   ├─ database_schema.sql          ← Table definitions
  │   ├─ dashboard_queries.sql        ← Metabase queries
  │   ├─ aws_day1_checklist.md       ← Execution plan
  │   ├─ connection_details.txt       ← Fill after AWS setup
  │   └─ notes.md                     ← Your notes/learnings
  │
  ├─ docs/                            ← Existing
  │   ├─ PHASE2_LESSON1_CLOUD_BASICS.md
  │   ├─ PHASE2_LESSON2_AWS_FREE_TIER_2025_REALITY.md
  │   └─ PHASE2_LESSON3_CREATE_AWS_ACCOUNT.md
  │
  └─ [existing Phase 1 files...]
```

**Create folders:**
```bash
mkdir phase2
cd phase2
```

**Time Investment:** 15 minutes
**Benefit:** Organized and ready

---

### 13. Final Knowledge Check

**Before creating AWS account, can you answer:**

```
PostgreSQL:
  ✓ What is a PRIMARY KEY?
  ✓ What is a FOREIGN KEY?
  ✓ What does SELECT * FROM table WHERE price > 100 do?
  ✓ How do you add a new row? (INSERT)
  ✓ How do you join two tables?

AWS:
  ✓ What is RDS?
  ✓ What is EC2?
  ✓ What region will you use? (ap-south-1)
  ✓ How much do credits cost? ($200)
  ✓ How long is Free Plan valid? (6 months)

Metabase:
  ✓ What is a "Question"?
  ✓ What is a "Dashboard"?
  ✓ How do you create a chart?
  ✓ Can you filter data?

Your Project:
  ✓ What tables will your database have?
  ✓ What dashboards will you build first?
  ✓ What metrics matter to your business?
```

**If you can answer all of these → You're ready! ✓**

**If not → Review the sections above**

---

## Complete Pre-AWS Timeline Summary

### Week 1: Learning (10-15 hours)
```
Day 1-2: PostgreSQL basics (5-8 hours)
Day 3-4: Metabase & AWS concepts (5-7 hours)
```

### Week 2: Planning & Coding (15-20 hours)
```
Day 1: Database schema design (2-3 hours)
Day 2: Dashboard design (2-3 hours)
Day 3-4: Write migration script (4-6 hours)
Day 5: Create SQL queries (2 hours)
Day 6-7: Local testing (4-6 hours)
```

### Week 3: Final Prep (2-3 hours)
```
Day 1: Install packages (30 min)
Day 2: Create checklists (1 hour)
Day 3: Organize files (30 min)
Day 4: Final review (1 hour)
```

**Total Preparation: 25-40 hours over 3 weeks**

**AWS Time Saved: 2-3 weeks minimum!**

---

## The Payoff

### Without Preparation:
```
AWS Day 1: "What is PostgreSQL?"
AWS Week 1: Learning SQL basics
AWS Week 2: Designing database
AWS Week 3: Writing migration script
AWS Week 4: Finally getting started
AWS Month 2-6: Actually using the system

Result: Wasted 1 month of 6-month free period (17%!)
```

### With Preparation:
```
AWS Day 1: Execute checklist, setup complete
AWS Day 2: Data migrated, database live
AWS Day 3-4: Dashboards built
AWS Week 2: Using system, gathering insights
AWS Month 2-6: Business value, iteration, learning

Result: Used full 6 months productively!
```

---

## What You CAN'T Do Before AWS

**These require AWS account (do AFTER creation):**

```
✗ Create RDS database
✗ Launch EC2 instance
✗ Actually run Metabase in cloud
✗ Test AWS-to-local connections
✗ Set up AWS IAM users
✗ Configure VPC settings
```

**But everything else? DO IT NOW!**

---

## Action Plan

### This Week:
1. Complete PostgreSQL tutorial (SQLBolt)
2. Install PostgreSQL locally (optional but recommended)
3. Play with Metabase demo
4. Watch AWS intro videos

### Next Week:
1. Design database schema
2. Sketch dashboards on paper
3. Write migration script
4. Create SQL query templates

### Week 3:
1. Test everything locally
2. Create execution checklist
3. Organize all files
4. Final review

### Week 4:
**CREATE AWS ACCOUNT → EXECUTE! 🚀**

---

## Checklist Before Creating AWS Account

```
Learning:
  ✓ Completed PostgreSQL basics
  ✓ Understand SQL SELECT, INSERT, UPDATE
  ✓ Know what RDS and EC2 are
  ✓ Familiar with Metabase interface

Planning:
  ✓ Database schema designed
  ✓ Dashboards sketched
  ✓ Know what metrics matter

Code:
  ✓ Migration script written
  ✓ SQL queries prepared
  ✓ Python packages installed
  ✓ Tested locally (if possible)

Organization:
  ✓ Files organized in phase2/ folder
  ✓ Execution checklist ready
  ✓ Connection details template ready

Readiness:
  ✓ Credit card ready
  ✓ Email accessible
  ✓ Phone for SMS verification
  ✓ 4-5 hours free for AWS Day 1
```

**All checked? → CREATE AWS ACCOUNT!**
**Not all checked? → Keep preparing!**

---

## Remember

**6 months seems long, but:**
- Month 1: Setup, learning, building
- Month 2-4: Using, iterating, improving
- Month 5: Evaluate: Keep paying or migrate?
- Month 6: Decision time

**Every day of preparation = More days actually using the system!**

---

Ready to start your preparation journey? Let me know what you want to tackle first!
