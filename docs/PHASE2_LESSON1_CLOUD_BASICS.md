# Phase 2 - Lesson 1: Cloud Computing & AWS Fundamentals
## Complete Beginner's Guide

---

## Table of Contents
1. [What is Cloud Computing?](#what-is-cloud-computing)
2. [Why Do We Need the Cloud?](#why-do-we-need-the-cloud)
3. [What is AWS?](#what-is-aws)
4. [AWS Free Tier Explained](#aws-free-tier-explained)
5. [Key AWS Services We'll Use](#key-aws-services-well-use)
6. [What is a Database?](#what-is-a-database)
7. [What is PostgreSQL?](#what-is-postgresql)
8. [What is Metabase?](#what-is-metabase)
9. [Our Complete Architecture](#our-complete-architecture)
10. [Cost Breakdown & Safety](#cost-breakdown-and-safety)

---

## What is Cloud Computing?

### The Simple Analogy

**Think of electricity in your home:**

**OLD WAY (Before electricity grids):**
- Every house had its own generator
- You had to maintain it, fuel it, repair it
- If it broke, you had no power
- Expensive and inefficient

**NEW WAY (With electricity grid):**
- You just plug into the wall
- Electricity company handles generation, maintenance
- You only pay for what you use
- Always available, reliable

**Cloud computing is the EXACT same concept, but for computers!**

### The Technical Definition

**Before Cloud (Traditional Way):**
```
Your Business Needs a Website/Database
         ↓
You Buy Physical Server ($5,000+)
         ↓
You Install It in Your Office
         ↓
You Pay for:
  • Server hardware
  • Electricity (24/7)
  • Internet connection
  • Air conditioning (servers get hot!)
  • IT person to maintain it
  • Backup systems
  • Security systems
         ↓
Total Cost: $10,000+ per year
```

**With Cloud (Modern Way):**
```
Your Business Needs a Website/Database
         ↓
You Rent a Virtual Server from AWS
         ↓
You Pay for:
  • Only the computing power you use
  • Only the storage you use
  • Only when it's running
         ↓
Total Cost: $0 - $50 per month (or FREE with free tier!)
```

### What "Cloud" Actually Means

The "cloud" is just **someone else's computer** that you rent over the internet.

**Physical Reality:**
```
You (In India)
      |
      | Internet
      |
      ↓
AWS Data Center (Mumbai/Singapore)
      |
      ├─ Building full of thousands of computers
      ├─ Massive air conditioning
      ├─ Backup power generators
      ├─ Security guards
      ├─ IT teams 24/7
      └─ Fire suppression systems
```

You get to **use** these computers without **owning** them!

---

## Why Do We Need the Cloud?

### For Your Jewelry Business

**Current Setup (Phase 1):**
```
Google Sheets on Your Computer
  ↓
Problems:
  ✗ Only accessible from your computer
  ✗ No automated backups
  ✗ Can't handle lots of data (slow with 10,000+ rows)
  ✗ No real-time analytics
  ✗ Team members can't access simultaneously
  ✗ If Google Sheets goes down, you're stuck
```

**With Cloud (Phase 2):**
```
Data in AWS PostgreSQL Database
  ↓
Benefits:
  ✓ Access from anywhere (home, shop, phone)
  ✓ Automatic backups every day
  ✓ Handles millions of rows (fast!)
  ✓ Real-time dashboards
  ✓ Entire team can access at once
  ✓ 99.99% uptime (almost never goes down)
  ✓ Professional-grade security
```

### Real-World Example

**Scenario:** You're at your jewelry shop, a customer asks about an earring.

**Without Cloud:**
1. You need to go home to check Google Sheets
2. Or call someone to check for you
3. Customer waits or leaves

**With Cloud:**
1. You pull out your phone
2. Open dashboard
3. See inventory in 2 seconds
4. Customer buys immediately

---

## What is AWS?

### Full Name
**AWS = Amazon Web Services**

### What It Is

AWS is Amazon's **cloud computing platform**. Yes, the same Amazon that sells products online!

**Fun Fact:** Amazon built huge computer infrastructure to run their online shopping site. They realized "Hey, we have all these extra computers, let's rent them out!" Now AWS makes MORE money than Amazon's retail business!

### Why AWS is Popular

**Market Share:**
```
Cloud Computing Market (2024):
  AWS (Amazon)         32%  ████████████
  Azure (Microsoft)    23%  ████████
  GCP (Google)         10%  ████
  Others               35%  ████████
```

**Why We Choose AWS:**
1. **Most popular** = Most tutorials, help available
2. **Free tier** = Perfect for learning and small businesses
3. **Reliable** = Used by Netflix, Airbnb, NASA
4. **Complete** = Has every service we need

### AWS Global Infrastructure

AWS has data centers around the world:

```
AWS Regions (Some Examples):
  • US East (Virginia)      - Oldest, most services
  • US West (Oregon)
  • EU (Ireland)
  • EU (Frankfurt)
  • Asia Pacific (Mumbai)   ← We'll likely use this
  • Asia Pacific (Singapore)
  • Middle East (Bahrain)
  • South America (São Paulo)
```

**Region:** A geographical location with multiple data centers

**Why Multiple Regions?**
- Faster access (closer = faster)
- Legal requirements (data must stay in country)
- Disaster recovery (if one region fails, others work)

---

## AWS Free Tier Explained

### Three Types of Free Tier

AWS offers three different types of "free":

```
+----------------------------------------------------------+
|  1. ALWAYS FREE                                          |
|  Services that are free forever (with limits)            |
|  Examples:                                               |
|  • Lambda: 1 million requests/month                      |
|  • DynamoDB: 25 GB storage                               |
|  We won't use these for our project                      |
+----------------------------------------------------------+

+----------------------------------------------------------+
|  2. 12 MONTHS FREE                                       |
|  Free for first 12 months after account creation         |
|  Examples:                                               |
|  • EC2: 750 hours/month (virtual servers)                |
|  • RDS: 750 hours/month (databases) ← WE'LL USE THIS     |
|  • S3: 5 GB storage                                      |
+----------------------------------------------------------+

+----------------------------------------------------------+
|  3. TRIAL PERIODS                                        |
|  Free for short periods (30-60 days)                     |
|  Examples:                                               |
|  • SageMaker: 2 months free                              |
|  We won't use these                                      |
+----------------------------------------------------------+
```

### What "750 Hours/Month" Means

**Confused about 750 hours?** Let me explain:

**1 Month = 30 days × 24 hours = 720 hours**

So 750 hours = **You can run ONE server 24/7 for the entire month FREE**

**Math:**
```
Option 1: Run 1 server for 750 hours = FREE
Option 2: Run 2 servers for 375 hours each = FREE
Option 3: Run 1 server 24/7 (720 hours) = FREE (with 30 hours extra!)

Our Plan: Run 2 servers 24/7:
  • 1 Database server (RDS)    = 720 hours
  • 1 Metabase server (EC2)    = 720 hours
  Both covered under free tier = $0
```

### Free Tier Limits for Our Project

**What We'll Use:**

| Service | What It's For | Free Tier Limit | Our Usage | Cost |
|---------|---------------|-----------------|-----------|------|
| RDS PostgreSQL | Database | 750 hrs/month | 720 hrs/month | $0 |
| | | 20 GB storage | ~1 GB | $0 |
| EC2 t2.micro | Metabase server | 750 hrs/month | 720 hrs/month | $0 |
| | | 30 GB storage | ~10 GB | $0 |
| Data Transfer | Internet | 15 GB out/month | ~1 GB | $0 |
| **TOTAL** | | | | **$0/month** |

### Safety Mechanisms We'll Set Up

Don't worry! We'll configure **billing alerts**:

```
Step 1: Set Billing Alert at $1
  ↓
Step 2: Set Billing Alert at $5
  ↓
Step 3: Set Billing Alert at $10

If you EVER spend $1, you get email warning!
We can fix it before spending more.
```

---

## Key AWS Services We'll Use

### 1. RDS (Relational Database Service)

**What It Is:** Managed database hosting

**Simple Analogy:**
```
Without RDS:
  You buy a fish tank, maintain water, feed fish, clean tank

With RDS:
  You pay aquarium, they handle everything, you just visit fish
```

**What RDS Does:**
- Installs PostgreSQL for you
- Handles backups automatically
- Applies security updates
- Monitors health 24/7
- Handles crashes/recovery

**What You Do:**
- Just use the database
- Write queries
- Store/retrieve data

### 2. EC2 (Elastic Compute Cloud)

**What It Is:** Virtual server (computer in the cloud)

**Simple Analogy:**
```
Physical Server:
  You buy a computer, put it in your office

EC2 Instance:
  You rent a computer in AWS data center
  Access it remotely from anywhere
```

**What We'll Use It For:**
- Running Metabase (dashboard software)
- Accessible via web browser
- No physical hardware needed

**Instance Types:**
```
t2.nano    $0.0058/hour   512 MB RAM    (Too small)
t2.micro   $0.0116/hour   1 GB RAM      ← FREE TIER (We'll use this)
t2.small   $0.023/hour    2 GB RAM      (Not free)
t2.medium  $0.046/hour    4 GB RAM      (Not free)
```

### 3. VPC (Virtual Private Cloud)

**What It Is:** Your own private network in AWS

**Simple Analogy:**
```
Your Home Network:
  • Your WiFi router creates private network
  • Devices (laptop, phone) can talk to each other
  • Internet comes in through one point

VPC:
  • AWS creates virtual network for you
  • Your services (database, server) can talk
  • Internet access controlled by you
```

**Why We Need It:**
- Security (keep database private)
- Isolation (your stuff separate from others)
- Control (decide what's accessible from internet)

---

## What is a Database?

### The Simple Explanation

**A database is an organized collection of data.**

### Real-World Analogy

**Filing Cabinet System:**
```
Filing Cabinet (Database)
  ├─ Drawer 1: Customers (Table)
  │    ├─ Folder: Customer #001 (Row)
  │    │    ├─ Name: Raj Kumar
  │    │    ├─ Phone: 98765-43210
  │    │    └─ Email: raj@example.com
  │    ├─ Folder: Customer #002 (Row)
  │    └─ Folder: Customer #003 (Row)
  │
  ├─ Drawer 2: Products (Table)
  │    ├─ Folder: Product #001 (Row)
  │    │    ├─ Name: Ear Rings XCNR
  │    │    ├─ Price: 250.00
  │    │    └─ Stock: 4
  │
  └─ Drawer 3: Sales (Table)
       └─ ...
```

### Google Sheets vs Database

**Google Sheets (What You Use Now):**
```
Strengths:
  ✓ Easy to use (like Excel)
  ✓ Visual (can see all data)
  ✓ Good for small data (< 10,000 rows)
  ✓ Simple formulas

Weaknesses:
  ✗ Slow with lots of data
  ✗ No complex queries
  ✗ No automatic relationships
  ✗ Not designed for applications
  ✗ Limited security
```

**PostgreSQL Database:**
```
Strengths:
  ✓ Handles millions of rows (fast!)
  ✓ Complex queries (find, filter, calculate)
  ✓ Relationships between tables
  ✓ Used by applications (Python can talk to it)
  ✓ Advanced security
  ✓ Automatic data integrity

Weaknesses:
  ✗ Not visual (need tools to see data)
  ✗ Requires SQL knowledge
  ✗ More setup needed
```

### Example: Your Inventory Data

**In Google Sheets:**
```
Type          | Name           | Cost  | Qty | Price
------------- | -------------- | ----- | --- | -----
Ear Rings     | Ear Rings XCNR | 110   | 4   | 250
Bracelets     | Bracelets R... | 110   | 5   | 250
```

**In PostgreSQL:**
```sql
-- Same data, but now you can query it:
SELECT * FROM inventory WHERE cost < 100;
SELECT SUM(qty) FROM inventory WHERE type = 'Ear Rings';
SELECT * FROM inventory WHERE price > cost * 2;
```

### Types of Databases

```
+----------------------------------------------------------+
|  SQL DATABASES (Relational)                              |
|  Data in tables with relationships                       |
|  Examples:                                               |
|  • PostgreSQL    ← We'll use this                        |
|  • MySQL                                                 |
|  • SQL Server                                            |
+----------------------------------------------------------+

+----------------------------------------------------------+
|  NoSQL DATABASES (Non-relational)                        |
|  Flexible data structure                                 |
|  Examples:                                               |
|  • MongoDB (documents)                                   |
|  • Redis (key-value)                                     |
|  We won't use these (overkill for our needs)             |
+----------------------------------------------------------+
```

---

## What is PostgreSQL?

### Basic Info

**Name:** PostgreSQL (often called "Postgres")
**Pronunciation:** "post-gress-Q-L" or "post-gres"
**Type:** Relational Database
**Cost:** FREE (open source)
**Age:** 35+ years old (very mature, stable)

### Why PostgreSQL?

**Comparison:**

| Feature | PostgreSQL | MySQL | SQL Server |
|---------|-----------|-------|------------|
| **Cost** | FREE | FREE | $$$$ |
| **Performance** | Excellent | Good | Excellent |
| **Features** | Most advanced | Basic | Advanced |
| **AWS Support** | Yes (RDS) | Yes (RDS) | Yes (RDS) |
| **Learning Curve** | Medium | Easy | Medium |
| **Popularity** | High | Very High | Medium |

**Why We Choose PostgreSQL:**
1. **FREE** and open source
2. **Advanced features** (we may need later)
3. **Excellent** AWS support
4. **Industry standard** (good for your resume!)
5. **Great** for analytics and dashboards

### What PostgreSQL Can Do

**Example Queries:**
```sql
-- Find all items with low stock (quantity < 5)
SELECT name, quantity
FROM inventory
WHERE quantity < 5;

-- Calculate total inventory value
SELECT SUM(quantity * price) as total_value
FROM inventory;

-- Find which category has most items
SELECT type, COUNT(*) as item_count
FROM inventory
GROUP BY type
ORDER BY item_count DESC;

-- Find items with high profit margin (>100%)
SELECT name, cost, price,
       ((price - cost) / cost * 100) as profit_margin
FROM inventory
WHERE price > cost * 2;
```

---

## What is Metabase?

### Basic Info

**Name:** Metabase
**Type:** Business Intelligence (BI) Tool / Dashboard Software
**Cost:** FREE (open source version)
**Purpose:** Turn data into visual dashboards

### The Simple Analogy

**Metabase is like a translator between you and your database:**

```
You: "Show me total sales this month"
  ↓
Metabase: Converts to SQL query
  ↓
Database: Returns numbers
  ↓
Metabase: Creates beautiful chart
  ↓
You: See visual chart on screen
```

### What Metabase Does

**Without Metabase:**
```
You want to know: "What's selling well?"
  ↓
You write SQL: SELECT type, SUM(qty) FROM sales GROUP BY type
  ↓
You see text result: Ear Rings: 45, Bracelets: 30
  ↓
You manually create chart in Excel
```

**With Metabase:**
```
You click: "Create Question"
  ↓
You select: Table = Sales, Group by = Type
  ↓
Metabase automatically creates beautiful chart
  ↓
You can share link with your team
```

### Dashboard Example

**What You'll Be Able to Build:**
```
+----------------------------------------------------------+
|  SWADHA INVENTORY DASHBOARD                              |
+----------------------------------------------------------+
|                                                          |
|  Total Items: 71        Total Value: ₹45,000            |
|  Low Stock: 5          New Items: 69                     |
|                                                          |
|  +--------------------+  +--------------------+          |
|  | Sales by Category  |  | Profit Margin      |          |
|  |                    |  |                    |          |
|  | [Bar Chart]        |  | [Pie Chart]        |          |
|  |                    |  |                    |          |
|  +--------------------+  +--------------------+          |
|                                                          |
|  +--------------------+  +--------------------+          |
|  | Stock Levels       |  | Top Selling Items  |          |
|  |                    |  |                    |          |
|  | [Line Chart]       |  | [Table]            |          |
|  |                    |  |                    |          |
|  +--------------------+  +--------------------+          |
|                                                          |
+----------------------------------------------------------+
```

### Why Metabase?

**Alternatives Comparison:**

| Tool | Cost | Ease of Use | Features | Our Choice |
|------|------|-------------|----------|------------|
| **Metabase** | FREE | Easy | Good | ✓ YES |
| Tableau | $$$$ | Medium | Excellent | ✗ Too expensive |
| Power BI | $ | Medium | Excellent | ✗ Costs money |
| Grafana | FREE | Hard | Excellent | ✗ Too complex |
| Superset | FREE | Medium | Good | ✗ Harder setup |

**Why Metabase:**
1. **Completely FREE**
2. **Easy** to learn (no SQL needed for basic use)
3. **Beautiful** dashboards
4. **Self-hosted** (we control our data)
5. **Active** community (lots of help available)

---

## Our Complete Architecture

### The Big Picture

```
+----------------------------------------------------------+
|  PHASE 2: COMPLETE SYSTEM ARCHITECTURE                   |
+----------------------------------------------------------+

  YOUR COMPUTER (Windows)
         |
         | 1. Run Python script
         |
         v
  +------------------+
  | Google Sheets    |
  | (Current Data)   |
  +------------------+
         |
         | 2. Python reads data
         |
         v

    INTERNET
         |
         v

+----------------------------------------------------------+
|  AWS CLOUD (Mumbai/Singapore Region)                     |
|                                                          |
|  +-------------------+        +--------------------+     |
|  | RDS PostgreSQL    |        | EC2 Instance       |     |
|  | (Database)        |<------>| (Metabase)         |     |
|  |                   |        |                    |     |
|  | • Stores inventory|        | • Creates          |     |
|  | • 20 GB storage   |        |   dashboards       |     |
|  | • Auto backups    |        | • Web interface    |     |
|  | • 24/7 running    |        | • 24/7 running     |     |
|  +-------------------+        +--------------------+     |
|         ^                              |                 |
|         |                              v                 |
|         | 3. Python                    |                 |
|         |    uploads                   |                 |
|         |    data                      |                 |
|         |                              |                 |
+---------|------------------------------|------------------+
          |                              |
          |                              | 4. You access via
          |                              |    web browser
          v                              v

    YOUR COMPUTER (Windows)

    Open browser → http://your-metabase-url
                     ↓
              View Dashboards!
```

### Data Flow

**Step-by-Step Process:**

```
STEP 1: Initial Setup (One-time)
  ├─ Create AWS account
  ├─ Launch PostgreSQL database
  ├─ Launch EC2 server
  ├─ Install Metabase on EC2
  └─ Connect Metabase to database

STEP 2: Data Migration (One-time)
  ├─ Design database tables
  ├─ Write Python script
  ├─ Read data from Google Sheets
  ├─ Transform data
  └─ Upload to PostgreSQL

STEP 3: Dashboard Creation (One-time)
  ├─ Design dashboard layout
  ├─ Create charts
  ├─ Add filters
  └─ Share with team

STEP 4: Daily Usage (Ongoing)
  ├─ Add new inventory to Google Sheets
  ├─ Run Python script to sync
  ├─ View updated dashboards
  └─ Make business decisions!
```

### What Each Component Does

**1. Google Sheets (Data Entry)**
```
Role: Where you enter new inventory
Why: Easy for your team to use
When: Every time you get new stock
```

**2. Python Script (Data Pipeline)**
```
Role: Moves data from Sheets to Database
Why: Automates the boring work
When: Run daily/weekly (or on-demand)
```

**3. PostgreSQL (Data Storage)**
```
Role: Stores all your inventory history
Why: Fast, reliable, can handle millions of rows
When: Always running, 24/7
```

**4. Metabase (Visualization)**
```
Role: Shows data as charts and dashboards
Why: Easier to understand than raw numbers
When: Access anytime you need insights
```

---

## Cost Breakdown & Safety

### Month-by-Month Costs

**Months 1-12 (First Year):**
```
RDS PostgreSQL (db.t2.micro):
  • 750 hours/month = FREE ✓
  • 20 GB storage = FREE ✓

EC2 Instance (t2.micro):
  • 750 hours/month = FREE ✓
  • 30 GB storage = FREE ✓

Data Transfer:
  • 15 GB outbound/month = FREE ✓
  • Inbound = FREE (always) ✓

TOTAL: $0/month for first 12 months
```

**After Month 12 (Without Free Tier):**
```
RDS PostgreSQL (db.t2.micro):
  • $0.017/hour × 720 hours = $12.24/month
  • 20 GB storage × $0.115/GB = $2.30/month

EC2 Instance (t2.micro):
  • $0.0116/hour × 720 hours = $8.35/month
  • 30 GB storage × $0.10/GB = $3.00/month

Data Transfer:
  • First 1 GB/month = FREE
  • $0.09/GB after that = ~$0.50/month

SUBTOTAL: $26.39/month
AWS often has promotions: ~$20-25/month realistic
```

### What Happens After 12 Months?

**Option 1: Keep Running (Recommended)**
```
Cost: ~$25/month ($300/year)

Is it worth it?
  • Professional dashboard
  • Unlimited data storage
  • 24/7 access from anywhere
  • Automatic backups

Compare to:
  • Hiring data analyst: $30,000/year
  • Other BI tools: $50-100/month

Verdict: Great value for money!
```

**Option 2: Migrate to Free Alternative**
```
Options:
  • Heroku (has free tier for small apps)
  • Google Cloud (also has free tier)
  • Railway.app (free tier available)

Downside: Need to move everything
```

**Option 3: Stop Services**
```
You can:
  • Export all data before month 12
  • Download Metabase dashboards
  • Delete AWS resources
  • No charges after deletion
```

### Safety Mechanisms

**1. Billing Alerts (We'll Set Up)**
```
Alert 1: $1 spent
  ↓
Email: "You've spent $1"
  ↓
Check what caused it
  ↓
Fix before it grows

Alert 2: $5 spent
  ↓
Email: "WARNING: $5 spent"
  ↓
Immediate action needed

Alert 3: $10 spent
  ↓
Email: "URGENT: $10 spent"
  ↓
Stop all services
```

**2. Budget Limits**
```
Set Budget: $10/month
  ↓
AWS sends alerts at:
  • 50% of budget ($5)
  • 80% of budget ($8)
  • 100% of budget ($10)

Cannot exceed without upgrading plan
```

**3. Daily Monitoring**
```
Check AWS Console:
  • Current month charges
  • Service-by-service breakdown
  • Projected month-end total

Takes 30 seconds/day
```

**4. Resource Tags**
```
We'll tag all resources:
  Tag: "Project = Swadha Phase 2"

Then view costs by project:
  Easy to see if something's wrong
```

### Common Mistakes to Avoid

**❌ MISTAKE 1: Leaving Services Running**
```
Bad:
  Launch 5 EC2 instances
  Forget about them
  = $40/month charge

Good:
  Launch only what we need (1 database + 1 server)
  Monitor weekly
  = $0/month (free tier)
```

**❌ MISTAKE 2: Wrong Instance Type**
```
Bad:
  Choose t2.large (not free)
  = $67/month charge

Good:
  Choose t2.micro (free tier)
  = $0/month
```

**❌ MISTAKE 3: Wrong Region**
```
Bad:
  Launch in US region
  You're in India
  = High data transfer costs

Good:
  Launch in Mumbai region
  = Faster + cheaper
```

**❌ MISTAKE 4: No Billing Alerts**
```
Bad:
  Don't set alerts
  Surprise bill at month end

Good:
  Set alerts immediately
  Know within hours if something's wrong
```

---

## Summary & Next Steps

### What You Learned Today

```
✓ What cloud computing is (rent vs. buy)
✓ What AWS is (Amazon's cloud platform)
✓ AWS Free Tier (12 months free!)
✓ RDS (managed database service)
✓ EC2 (virtual servers)
✓ What a database is (organized data)
✓ What PostgreSQL is (powerful free database)
✓ What Metabase is (dashboard tool)
✓ Complete architecture (how everything fits)
✓ Cost breakdown ($0 for first year!)
✓ Safety mechanisms (billing alerts)
```

### Key Concepts to Remember

**1. Cloud = Renting Computers**
- Don't buy hardware
- Pay only for what you use
- Access from anywhere

**2. AWS = Biggest Cloud Provider**
- Reliable
- Free tier for learning
- Complete set of services

**3. Free Tier = 12 Months Free**
- 750 hours/month per service
- Enough for 24/7 operation
- Must monitor usage

**4. Our Stack:**
```
PostgreSQL = Database (stores data)
Metabase = Dashboard (visualizes data)
Python = Connector (moves data)
```

### Ready for Next Lesson?

**Lesson 2 Preview: Creating Your AWS Account**

We'll cover:
- Step-by-step account creation
- Email verification
- Credit card setup (why it's safe)
- Setting up billing alerts
- Choosing the right region
- Verifying free tier activation

**Time needed:** 30-45 minutes

**What you'll need:**
- Email address
- Credit/debit card (for verification)
- Phone number (for SMS verification)
- Government ID (for some countries)

---

## Quick Reference

### Terms Glossary

| Term | Simple Definition |
|------|------------------|
| **Cloud** | Using someone else's computers over internet |
| **AWS** | Amazon's cloud computing service |
| **RDS** | Managed database service (we don't maintain) |
| **EC2** | Virtual server in the cloud |
| **PostgreSQL** | Free, powerful database software |
| **Metabase** | Turns data into dashboards |
| **Free Tier** | AWS services free for 12 months |
| **Instance** | A virtual server/computer |
| **Region** | Geographic location of AWS data centers |
| **SQL** | Language to talk to databases |

### Important Numbers

```
750 hours/month = 24/7 operation
720 hours/month = actual hours in 30-day month
20 GB = Database storage limit (free tier)
30 GB = Server storage limit (free tier)
12 months = Free tier duration
$0 = Our target monthly cost
```

---

**Ready to continue to Lesson 2?** Let me know and I'll guide you through creating your AWS account step-by-step!
