# Phase 2 - Lesson 2: AWS Free Tier 2025 - The Real Deal
## Updated Information Based on July 15, 2025 Changes

---

## CRITICAL: What Changed on July 15, 2025

**⚠️ IMPORTANT:** AWS completely restructured their Free Tier on July 15, 2025. Old tutorials and guides are now **OUTDATED**.

### Old Free Tier (Before July 15, 2025) - LEGACY

```
❌ NO LONGER AVAILABLE FOR NEW ACCOUNTS

Duration: 12 months
RDS PostgreSQL: 750 hours/month FREE
EC2: 750 hours/month FREE
Storage: 20 GB FREE
Cost: $0 for 12 months

If you created account BEFORE July 15, 2025:
  You keep these benefits!
```

### New Free Tier (After July 15, 2025) - CURRENT

```
✓ WHAT YOU GET AS A NEW USER

Duration: 6 months (not 12!)
Credits: $200 total ($100 instant + $100 from tasks)
After 6 months: MUST upgrade to Paid Plan or account deleted
Cost: $0 for 6 months, then ~$27/month

You'll use CREDITS instead of "free hours"
```

---

## How the New Credit-Based System Works

### The $200 Credits Breakdown

**1. Instant $100 Credits**
```
When you sign up:
  → Immediately receive $100 in AWS credits
  → Valid for 6 months
  → Can use on any eligible AWS service
```

**2. Earn Additional $100 Credits**
```
Complete 5 onboarding tasks ($20 each):

Task 1: Launch & terminate an EC2 instance        → $20
Task 2: Launch an RDS database                     → $20
Task 3: Create Lambda function with Function URL   → $20
Task 4: Use Amazon Bedrock text prompt             → $20
Task 5: Set a cost budget in AWS Budgets           → $20

Total: $100 more credits
```

**3. Credit Expiration**
```
Your Free Plan ends when:
  Option A: 6 months pass (whichever comes first)
  Option B: You use all $200 credits

After expiration:
  → 90-day grace period to upgrade
  → If no upgrade: Account and resources DELETED
```

---

## Can We Still Build Our Project? YES!

### Cost Calculation for Our Inventory System

**What We Need to Run:**
- 1× RDS PostgreSQL database (db.t3.micro)
- 1× EC2 instance for Metabase (t3.micro)
- Storage for database and server

**Mumbai Region Pricing (ap-south-1):**

| Service | Instance Type | Cost/Hour | Hours/Month | Monthly Cost |
|---------|--------------|-----------|-------------|--------------|
| **RDS PostgreSQL** | db.t3.micro | $0.020 | 720 | $14.40 |
| **EC2 (Metabase)** | t3.micro | $0.0104 | 720 | $7.49 |
| **RDS Storage** | 20 GB gp2 | - | - | $2.30 |
| **EC2 Storage** | 30 GB | - | - | $3.00 |
| **Data Transfer** | - | - | - | $0.50 |
| **TOTAL/MONTH** | | | | **$27.69** |

**6 Months Calculation:**
```
Month 1: $27.69
Month 2: $27.69
Month 3: $27.69
Month 4: $27.69
Month 5: $27.69
Month 6: $27.69

Total 6 months: $166.14

Your credits: $200
Remaining: $33.86

✓ YES, $200 will cover 6 months with room to spare!
```

---

## What Happens After 6 Months?

### Timeline

```
Day 1: Create AWS account
  ↓
  → Get $100 credits instantly
  → Complete 5 tasks → Get $100 more
  → Total: $200 credits
  ↓
Month 1-6: Build and run project
  ↓
  → Spend ~$27/month
  → Watch credits decrease
  ↓
Month 6 (End of Free Plan):
  ↓
  → AWS sends warning email
  → 90-day grace period begins
  ↓
3 Options Available:

  Option 1: Upgrade to Paid Plan
    → Keep everything running
    → Start paying $27/month
    → Recommended if business is growing

  Option 2: Export data & shut down
    → Download all dashboard designs
    → Export database to CSV
    → Delete all AWS resources
    → Cost: $0

  Option 3: Do nothing
    → After 90 days: Account DELETED
    → All data LOST
    → Cost: $0 (but lose everything!)
```

---

## Free Plan vs. Paid Plan

### Free Plan (First 6 Months)

**Pros:**
- $200 in credits
- No charges unless you upgrade
- Access to most AWS services
- Perfect for learning

**Cons:**
- 6 months maximum
- Some enterprise services restricted
- Must complete tasks to get full $200
- Account deleted if not upgraded

**Best For:**
- Learning cloud computing
- Testing business ideas
- Building prototypes
- Our inventory dashboard project ✓

### Paid Plan (After 6 Months)

**Pros:**
- No time limit
- All AWS services available
- Professional features
- Data never deleted (as long as you pay)

**Cons:**
- Costs money (~$27/month for our project)
- Credit card charged automatically
- Must monitor spending

**Best For:**
- Production businesses
- Long-term projects
- When dashboard proves valuable

---

## The 5 Onboarding Tasks (How to Get $100 Extra)

### Task 1: Launch & Terminate EC2 Instance

**What you'll do:**
```
1. Go to EC2 Dashboard
2. Click "Launch Instance"
3. Choose t3.micro (free tier)
4. Launch it
5. Wait 2 minutes
6. Terminate it

Time: 5 minutes
Reward: $20 in credits
```

**Why it's easy:** We need to launch EC2 anyway for Metabase, so this is automatic!

### Task 2: Launch RDS Database

**What you'll do:**
```
1. Go to RDS Dashboard
2. Click "Create database"
3. Choose PostgreSQL
4. Select db.t3.micro
5. Create it

Time: 3 minutes
Reward: $20 in credits
```

**Why it's easy:** This is EXACTLY what we need for our project!

### Task 3: Create Lambda Function

**What you'll do:**
```
1. Go to Lambda Dashboard
2. Click "Create function"
3. Choose "Author from scratch"
4. Name it "test-function"
5. Add Function URL
6. Save

Time: 3 minutes
Reward: $20 in credits
```

**Why it's easy:** Just clicking buttons, no coding required.

### Task 4: Use Amazon Bedrock

**What you'll do:**
```
1. Go to Bedrock Dashboard
2. Open "Text playground"
3. Type any question
4. Click "Run"

Time: 2 minutes
Reward: $20 in credits
```

**Why it's easy:** Just type "Hello" and click a button!

### Task 5: Set Cost Budget

**What you'll do:**
```
1. Go to AWS Budgets
2. Click "Create budget"
3. Set amount: $10
4. Add your email for alerts
5. Save

Time: 3 minutes
Reward: $20 in credits
```

**Why it's easy:** This is ESSENTIAL for safety anyway!

**Total Time: ~16 minutes**
**Total Reward: $100 in credits**

---

## Our Recommended Strategy

### Phase 2A: First 6 Months (FREE)

```
Month 1: Setup
  ├─ Create AWS account → Get $100 credits
  ├─ Complete 5 tasks → Get $100 more
  ├─ Launch RDS PostgreSQL
  ├─ Launch EC2 for Metabase
  ├─ Migrate data from Google Sheets
  └─ Build dashboards

Month 2-6: Use & Learn
  ├─ Use dashboards daily
  ├─ Monitor spending ($27/month)
  ├─ Evaluate business value
  └─ Decide if worth $27/month

Total Cost: $0 (covered by $200 credits)
```

### Phase 2B: After 6 Months (Decision Time)

```
If dashboards are valuable:
  → Upgrade to Paid Plan
  → Pay $27/month
  → Keep using professional tools
  → Scale as business grows

If NOT worth it:
  → Export all data before Month 6 ends
  → Download Metabase dashboard designs
  → Save database as CSV
  → Delete AWS resources
  → Total spent: $0
```

---

## Alternative Free Options

If you don't want to pay $27/month after 6 months:

### Option 1: Railway.app

```
Free Tier:
  ✓ PostgreSQL database
  ✓ 512 MB RAM
  ✓ 1 GB disk
  ✓ Forever free (with limits)

Limitations:
  ✗ Smaller database
  ✗ Less powerful
  ✗ Must stay active (deploy once/month)

Cost: $0/month forever
```

### Option 2: Supabase

```
Free Tier:
  ✓ PostgreSQL database
  ✓ 500 MB storage
  ✓ API access
  ✓ Forever free

Limitations:
  ✗ Paused after 7 days inactivity
  ✗ Limited to 500 MB
  ✗ Must unpause manually

Cost: $0/month forever
```

### Option 3: Render.com

```
Free Tier:
  ✓ PostgreSQL database
  ✓ Web services
  ✓ 90 days free for databases

Limitations:
  ✗ Only 90 days free
  ✗ Slower performance
  ✗ Limited to 1 GB storage

Cost: $0 for 3 months, then $7/month
```

### Our Recommendation

**Start with AWS Free Tier because:**
1. Best learning experience (industry standard)
2. Most powerful (handles any data size)
3. 6 months to decide if worth paying
4. Professional-grade tools
5. Great for resume/portfolio

**After 6 months:**
- If business value proven → Pay $27/month (worth it!)
- If just learning → Migrate to Railway or Supabase (free forever)

---

## Critical Safety Rules

### Rule 1: Set Billing Alerts IMMEDIATELY

```
Alert 1: $1 spent
Alert 2: $5 spent
Alert 3: $10 spent
Alert 4: $25 spent

Why: Know INSTANTLY if something goes wrong
```

### Rule 2: Only Launch What We Need

```
✓ 1 RDS database (db.t3.micro)
✓ 1 EC2 instance (t3.micro)
✗ NO extra instances
✗ NO experiments with other services
✗ NO larger instance types
```

### Rule 3: Choose Mumbai Region

```
Region: ap-south-1 (Asia Pacific Mumbai)

Why Mumbai:
  ✓ Closest to India (faster)
  ✓ Cheaper than US regions
  ✓ Lower data transfer costs
```

### Rule 4: Monitor Weekly

```
Every Monday:
  1. Check AWS Billing Dashboard
  2. Verify charges are ~$27/month pace
  3. Check credit balance remaining
  4. Look for unexpected charges

Takes: 2 minutes/week
Saves: Surprise bills!
```

### Rule 5: Export Before Month 6

```
Month 5, Day 15:
  → Export all database data to CSV
  → Download Metabase dashboard configs
  → Save Python scripts
  → Backup everything locally

Why: Insurance if you forget to upgrade
```

---

## Comparison: 2025 vs Legacy Free Tier

| Feature | Legacy (Before July 15) | New (After July 15) |
|---------|------------------------|---------------------|
| **Duration** | 12 months | 6 months |
| **RDS Free** | 750 hrs/month | Credits-based |
| **EC2 Free** | 750 hrs/month | Credits-based |
| **Total Value** | ~$330 | $200 |
| **After Expiry** | Services just start charging | Account DELETED (90 days) |
| **Eligibility** | Existing accounts only | New accounts only |
| **Complexity** | Service limits | Credit management |

**Bottom Line:** New system gives less ($200 vs $330) for shorter time (6 months vs 12 months), BUT still enough for our project!

---

## Real-World Example: Your 6-Month Journey

### Month 1: January 2026

```
Jan 1: Create AWS account
  → Instant: $100 credits
  → Balance: $100

Jan 2-3: Complete 5 onboarding tasks (16 minutes)
  → Earned: $100 more
  → Balance: $200

Jan 4-7: Setup (using our Phase 2 lessons)
  → Launch RDS PostgreSQL
  → Launch EC2 for Metabase
  → Migrate data
  → Build dashboards

Jan 8-31: Use dashboards daily
  → Charges: $27.69
  → Balance: $172.31
```

### Month 2-6: February-June 2026

```
Each month:
  → Use dashboards for business
  → Charges: $27.69/month
  → Track inventory, sales, profits

June 30 Balance: $33.86 remaining
```

### End of Month 6: June 30, 2026

```
Email from AWS:
  "Your Free Plan expires in 30 days.
   You have $33.86 in credits remaining.
   Please upgrade to Paid Plan to keep your resources."

Your Decision:
  Option A: Upgrade (dashboards worth $27/month? → YES)
  Option B: Export & shut down (not worth it → NO)
```

### Month 7: July 2026

```
If you upgraded:
  → Everything keeps running
  → Credit card charged $27.69
  → Business continues

If you didn't upgrade:
  → 90-day grace period starts
  → Countdown to account deletion
  → Need to export data NOW
```

---

## Frequently Asked Questions

### Q1: Is the new Free Tier worse than the old one?

**A:** Yes and no.

**Worse:**
- Only 6 months instead of 12
- Only $200 instead of ~$330 value
- Account gets deleted if not upgraded

**Better:**
- Simpler to understand (credits vs. service limits)
- $200 is enough for our small project
- Clear decision point at 6 months

### Q2: Can I create multiple AWS accounts to get more free credits?

**A:** Technically possible but **NOT RECOMMENDED**.

**Why:**
- Against AWS Terms of Service
- Requires different credit cards
- Requires different email addresses
- Can get all accounts banned
- Considered fraud

**Better approach:** Use the 6 months wisely, then decide if worth paying.

### Q3: What if I accidentally spend all $200 before 6 months?

**A:** Your Free Plan ends immediately.

**What happens:**
1. AWS sends email warning
2. 90-day grace period starts
3. Must upgrade to Paid Plan or lose everything

**How to prevent:**
- Set billing alerts at $25, $50, $75, $100, $150, $175
- Check billing dashboard weekly
- Don't launch extra services

### Q4: Can I pause my Free Plan to make it last longer?

**A:** NO. The 6-month timer starts on account creation and cannot be paused.

**Workaround:**
- Don't create account until you're ready to start
- Have everything planned beforehand
- Maximize your 6 months

### Q5: What happens to my data if I don't upgrade?

**A:**

```
Month 6 (Free Plan ends):
  → 90-day grace period starts
  → Data still accessible
  → No charges yet

Month 9 (End of grace period):
  → Account DELETED
  → All data LOST FOREVER
  → No recovery possible

⚠️ EXPORT YOUR DATA BEFORE MONTH 6!
```

### Q6: Is $27/month worth it after the free period?

**A:** Depends on your business value.

**It's worth it if:**
- Dashboards help make better business decisions
- Time saved > $27/month value
- Inventory tracking prevents losses
- Sales insights increase profits

**It's NOT worth it if:**
- Rarely use the dashboards
- Google Sheets is enough
- Business too small to justify
- Just learning (not production)

**Our advice:** Use the 6 months to evaluate!

### Q7: Can I switch to a cheaper instance to save money?

**A:** db.t3.micro and t3.micro are ALREADY the cheapest options.

**Next level down:** db.t4g.nano (~$7/month)
**Problem:** Too slow for Metabase, poor experience

**Better approach:** If cost is issue, migrate to free alternative (Railway, Supabase) after 6 months.

### Q8: Will AWS charge my credit card during the Free Plan?

**A:** NO, as long as you stay within $200 credits.

**When charges occur:**
- If you use > $200 in services
- If you launch non-free-tier services
- If you exceed free tier limits

**Safety:** Set billing alerts to know before charges happen!

---

## Summary & Next Steps

### What You Learned

```
✓ AWS changed Free Tier on July 15, 2025
✓ New accounts get $200 credits for 6 months (not 12)
✓ Our project costs ~$27/month ($166 total for 6 months)
✓ $200 credits will cover our project with $34 left over
✓ After 6 months: Upgrade ($27/month) or migrate (free)
✓ Must complete 5 tasks to get full $200 ($100 base + $100 tasks)
✓ Account gets deleted if not upgraded (90-day warning)
✓ Mumbai region is best (fastest + cheapest)
```

### Your Decision

**Before we proceed, you need to decide:**

```
Option 1: Proceed with AWS Free Tier
  ✓ 6 months completely free
  ✓ Professional-grade tools
  ✓ Learn industry-standard platform
  ✓ Decision point at Month 6 (upgrade or export)
  ✗ Requires credit card (won't be charged)
  ✗ Must complete within 6 months
  ✗ $27/month after if you keep using

Option 2: Start with Free Alternative (Railway/Supabase)
  ✓ Free forever (with limits)
  ✓ No credit card needed
  ✓ No time pressure
  ✗ Less powerful
  ✗ Not industry standard
  ✗ May need to upgrade eventually anyway

Option 3: Postpone Phase 2
  ✓ Keep using Google Sheets
  ✓ Zero cost
  ✗ No dashboards
  ✗ No cloud benefits
```

**Our Recommendation:** **Option 1 (AWS)** for best learning + business value.

6 months is plenty of time to build, test, and decide if worth paying $27/month.

---

## Ready for Lesson 3?

**Lesson 3 Preview: Creating Your AWS Account (Step-by-Step)**

We'll cover:
- Exact steps to create account (with screenshots description)
- How to verify your identity
- Setting up billing alerts BEFORE launching anything
- Completing the 5 tasks to get $100 extra credits
- Verifying you're on the FREE Plan (not Paid)
- Choosing Mumbai region
- Understanding the AWS Console

**Time needed:** 45-60 minutes

**What to prepare:**
- Email address (Gmail works)
- Credit/debit card (for verification - won't be charged)
- Phone number (for SMS verification)
- ID proof (may be needed for verification)

---

## Sources & References

All information verified from official sources (December 2025):

- [AWS Free Tier Official Page](https://aws.amazon.com/free/)
- [AWS Free Tier Legacy Page](https://aws.amazon.com/free/legacy/)
- [AWS Free Tier 2025 Changes (DEV Community)](https://dev.to/ricky_rios/aws-free-tier-2025-what-changed-whats-included-and-how-to-use-it-7a6)
- [What's New in AWS Free Tier 2025](https://dev.to/aws-builders/whats-new-in-aws-free-tier-2025-2ba5)
- [AWS Free Tier Changes July 2025](https://freetier.co/articles/aws-free-tier-changes-july-15-2025)
- [AWS RDS Free Tier Details](https://aws.amazon.com/rds/free/)
- [RDS Pricing](https://aws.amazon.com/rds/pricing/)
- [EC2 Pricing Mumbai Region](https://instances.vantage.sh/aws/ec2/t3.micro?region=ap-south-1)
- [db.t3.micro Pricing](https://instances.vantage.sh/aws/rds/db.t3.micro)

---

**Next:** Ready to create your AWS account? Let me know and we'll proceed to Lesson 3!
