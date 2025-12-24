# Phase 2 - Lesson 3: Creating Your AWS Account
## Complete Step-by-Step Guide for Absolute Beginners

---

## Table of Contents
1. [Pre-Flight Checklist](#pre-flight-checklist)
2. [Step-by-Step Account Creation](#step-by-step-account-creation)
3. [Understanding Verification](#understanding-verification)
4. [Credit Card Setup (Why It Won't Charge You)](#credit-card-setup)
5. [CRITICAL: Setting Up Billing Alerts](#critical-setting-up-billing-alerts)
6. [Completing the 5 Tasks for $100 Extra Credits](#completing-the-5-tasks)
7. [Verifying Your Free Plan Status](#verifying-your-free-plan-status)
8. [Setting Default Region to Mumbai](#setting-default-region-to-mumbai)
9. [Understanding the AWS Console](#understanding-the-aws-console)
10. [Security Best Practices](#security-best-practices)

---

## Pre-Flight Checklist

Before we start, gather these items. You'll need them during the signup process:

### Required Items

```
✓ Email Address
  - Gmail, Yahoo, Outlook all work
  - Don't use temporary/disposable emails
  - You'll need access to this email NOW
  - Example: yourname@gmail.com

✓ Strong Password
  - At least 8 characters
  - Include: uppercase, lowercase, numbers, symbols
  - Example: MyAWS2025!Secure
  - Write it down somewhere safe!

✓ Credit or Debit Card
  - Visa, Mastercard, American Express, or RuPay
  - Must have international transactions enabled
  - Will charge ₹2 (~$0.02) for verification, refunded immediately
  - NO OTHER CHARGES if you stay in free tier

✓ Phone Number
  - Mobile phone that can receive SMS
  - Or voice call (if SMS doesn't work)
  - Format: +91-XXXXXXXXXX (India)

✓ Address Details
  - Full address with PIN code
  - Billing address (same as credit card)
  - Be accurate - needed for verification
```

### Optional (May Be Required)

```
? Government ID
  - Aadhar Card, PAN Card, Passport, or Driver's License
  - Sometimes AWS asks for verification
  - Have a photo ready on your phone/computer
  - Most users don't need this, but keep handy
```

### Time Required

```
Account Creation:      15-20 minutes
Verification:          5-10 minutes
Billing Alerts Setup:  5 minutes
5 Onboarding Tasks:    15-20 minutes
Total:                 40-55 minutes

☕ Grab a coffee - we're going to do this carefully!
```

---

## Step-by-Step Account Creation

### Step 1: Go to AWS Free Tier Signup Page

**Action:**
1. Open your web browser (Chrome, Firefox, Edge)
2. Go to: https://aws.amazon.com/free/
3. Look for a button that says **"Create a Free Account"** or **"Get started for free"**
4. Click it

**What you'll see:**
- AWS homepage with information about Free Tier
- Big orange or blue button to start signup
- Don't click other buttons like "Sign In" (that's for existing accounts)

**Tip:** Keep this browser tab open throughout the process. Don't close it until you're done!

---

### Step 2: Enter Your Email and Choose Account Name

**What you'll see:**
```
Sign up for AWS
====================
Root user email address: [____________]
AWS account name:        [____________]

[ Continue ]
```

**What to enter:**

**Root user email address:**
- Your email (e.g., yourname@gmail.com)
- This becomes your AWS account username
- You'll receive important notifications here
- **Cannot be changed later** - choose wisely!

**AWS account name:**
- Name for this account (e.g., "Swadha Inventory Project")
- Can be changed later
- Just helps you identify the account
- Keep it simple and descriptive

**Example:**
```
Root user email address: ramesh.kumar@gmail.com
AWS account name:        Swadha-Inventory-Dashboard
```

**Click:** The "Continue" button

---

### Step 3: Verify Your Email

**What happens next:**
AWS sends a verification code to your email.

**What you'll see:**
```
Verify email address
====================
We sent a verification message to: ramesh.kumar@gmail.com

Verification code: [___________]

Didn't receive it? [ Resend code ]

[ Verify ]
```

**What to do:**
1. Open your email inbox (new tab, keep AWS tab open)
2. Look for email from: **no-reply@signin.aws**
3. Subject: **"Your AWS verification code"**
4. Open the email
5. Copy the 6-digit code (e.g., 123456)
6. Go back to AWS tab
7. Paste code in the box
8. Click "Verify"

**Troubleshooting:**
```
Problem: Email doesn't arrive
Solution:
  1. Check spam/junk folder
  2. Wait 2-3 minutes
  3. Click "Resend code"
  4. Check email again

Problem: Code expired
Solution:
  1. Click "Resend code"
  2. Enter new code quickly (within 10 minutes)
```

---

### Step 4: Create Password

**What you'll see:**
```
Set your password
====================
Password:         [____________]
Confirm password: [____________]

Password requirements:
- Minimum 8 characters
- Uppercase letter (A-Z)
- Lowercase letter (a-z)
- Number (0-9)
- Non-alphanumeric character (!@#$%^&*)

[ Continue ]
```

**Create a strong password:**

**Bad passwords:**
```
✗ password123      (too common)
✗ Swadha2025       (no special character)
✗ admin@123        (too simple)
```

**Good passwords:**
```
✓ Swadha@2025!AWS    (has everything)
✓ MyInventory#2025   (has everything)
✓ AWS$ecure2025!     (has everything)
```

**Important:**
- **Write this password down** in a notebook
- Or use a password manager (LastPass, 1Password)
- You'll need this EVERY time you log in
- Forgot password = long recovery process

**Enter password twice:**
1. Type password in first box
2. Type EXACT same password in second box
3. Make sure they match!
4. Click "Continue"

---

### Step 5: Choose Plan Type - CRITICAL STEP!

**What you'll see:**
```
Choose your support plan
====================

[ ] Free Plan
    - Up to $200 in credits (complete tasks to unlock more credits)
    - 6 months or until credits run out
    - No charges unless you upgrade

[ ] Paid Plan
    - All services available
    - Pay as you go
    - Charges start immediately

Select one and continue
```

**⚠️ CRITICAL: Select "Free Plan"**

**Why this matters:**
```
If you choose Free Plan:
  ✓ Get $200 credits
  ✓ No charges for 6 months
  ✓ Our project works perfectly
  ✓ Can upgrade later if needed

If you choose Paid Plan:
  ✗ No free credits
  ✗ Charges start immediately
  ✗ Pay ~$27/month from day 1
  ✗ Not what we want!
```

**Action:**
1. Click the **"Free Plan"** radio button
2. Make sure it's selected (filled circle)
3. Click "Continue" button

**Double-check:** Look for confirmation text saying "Free Plan selected" or similar.

---

### Step 6: Enter Contact Information

**What you'll see:**
```
Contact Information
====================

How do you plan to use AWS?
( ) Personal
( ) Business
( ) For education/learning

Full Name:        [___________________]
Phone Number:     [+91] [__________]
Country/Region:   [India ▼]
Address:          [___________________]
City:             [___________________]
State/Province:   [___________________]
Postal code:      [___________________]

[ ] I have read and agree to AWS Customer Agreement
    and AWS Service Terms

[ Continue ]
```

**How to fill this out:**

**How do you plan to use AWS?**
- Choose **"Business"** (even if small business)
- Why? You're using it for your jewelry business
- Gives you access to business support options

**Full Name:**
- Your real name (as on credit card)
- Example: Ramesh Kumar

**Phone Number:**
- Your mobile number
- Format: +91 and then 10 digits
- Example: +91 9876543210
- Make sure you can receive SMS on this number!

**Country/Region:**
- Select "India" from dropdown

**Address:**
- Your complete address
- Should match credit card billing address
- Example: "123, MG Road, Gandhi Nagar"

**City:**
- Your city name
- Example: "Mumbai"

**State/Province:**
- Your state
- Example: "Maharashtra"

**Postal Code:**
- Your PIN code
- Example: "400001"

**Terms Agreement:**
- Check the box: "I have read and agree..."
- **What you're agreeing to:**
  - AWS Customer Agreement (standard legal terms)
  - AWS Service Terms (how to use services)
  - These are standard, same for everyone

**Click:** "Continue"

---

### Step 7: Payment Information (Credit Card)

**What you'll see:**
```
Payment Information
====================

( ) Credit or Debit Card
( ) Checking Account (Not available in India)

Card number:      [________________]
Expiration date:  [MM/YY]
Cardholder name:  [________________]
CVV:              [___]

Billing address:
( ) Same as contact information
( ) Use different billing address

[ Verify and Add ]
```

**Understanding why AWS needs your card:**

```
AWS needs card for:
  1. Identity verification (prove you're real person)
  2. Prevent abuse (one account per card)
  3. Backup payment (if you exceed free tier)

AWS will charge:
  1. ₹2 (about $0.02) for verification
  2. Refunded within 3-5 days
  3. NO other charges if you stay in free tier

Your card must:
  1. Have international transactions enabled
  2. Have at least ₹2 balance
  3. Be in your name
```

**How to fill this out:**

**Card number:**
- 16-digit number on front of card
- Example: 4532 1234 5678 9010
- Type carefully! No spaces needed (AWS adds them)

**Expiration date:**
- MM/YY format
- Example: If card expires December 2027, enter: 12/27
- Find on front of card

**Cardholder name:**
- Name exactly as printed on card
- Example: "RAMESH KUMAR"
- Usually in CAPITAL LETTERS on card

**CVV (Card Verification Value):**
- 3 digits on back of card (Visa/Mastercard)
- 4 digits on front (American Express)
- Example: 123

**Billing address:**
- Select "Same as contact information" (if it matches)
- Or enter card's billing address if different

**Click:** "Verify and Add"

**What happens next:**
```
Step 1: AWS processes your card
  → Shows "Verifying..." message
  → Takes 10-30 seconds

Step 2: ₹2 charge for verification
  → Shows on card as "AMAZON WEB SERVICES"
  → Immediately refunded

Step 3: Verification complete
  → Green checkmark appears
  → "Payment method verified" message
  → Proceeds to next step
```

**Troubleshooting:**

```
Problem: "Card declined"
Solutions:
  1. Check card has international transactions enabled
     - Call your bank
     - Ask to enable international/online transactions
  2. Try different card
  3. Check card has balance
  4. Check card is not expired

Problem: "Invalid card number"
Solutions:
  1. Re-enter number carefully
  2. Make sure it's 16 digits
  3. No spaces (AWS adds them automatically)

Problem: "CVV incorrect"
Solutions:
  1. Check back of card (3 digits)
  2. American Express: front of card (4 digits)
  3. Sometimes front and back confused
```

---

### Step 8: Confirm Your Identity (Phone Verification)

**What you'll see:**
```
Confirm your identity
====================

We'll send a verification code to: +91 9876543210

How would you like to verify?
( ) Text message (SMS)
( ) Voice call

Enter the security check (CAPTCHA):
[Type the characters you see]
[fuzzy image: 7aH2kP]

[ Send SMS ] or [ Call me now ]
```

**Choose verification method:**

**Text message (SMS) - Recommended:**
- Faster (arrives in 10-30 seconds)
- Easy to copy code
- Doesn't require answering phone

**Voice call:**
- Good if SMS doesn't work
- Robot voice reads 4-digit code
- Repeat 3 times slowly

**Steps:**

1. **Choose** "Text message (SMS)"

2. **Enter CAPTCHA:**
   - Look at fuzzy image
   - Type characters exactly as shown
   - Case matters! (A ≠ a)
   - Example image shows: 7aH2kP → Type: 7aH2kP
   - Hard to read? Click "Get a new puzzle"

3. **Click** "Send SMS" button

4. **Wait for SMS:**
   - Should arrive in 10-30 seconds
   - From: AMAZON or AWS
   - Contains 4-digit code
   - Example: "Your AWS verification code is 1234"

5. **Enter code:**
   ```
   Enter the PIN you received
   ====================

   [_] [_] [_] [_]

   Didn't receive it?
   [ Send new code ]

   [ Verify ]
   ```

6. **Type the 4-digit code**
   - Example: 1234
   - Click "Verify"

**Troubleshooting:**

```
Problem: SMS doesn't arrive
Solutions:
  1. Wait 2 minutes (sometimes delayed)
  2. Check phone has signal
  3. Check phone can receive SMS from international numbers
  4. Try "Voice call" instead
  5. Click "Send new code"

Problem: Code not working
Solutions:
  1. Make sure you typed it correctly
  2. Code expires in 10 minutes
  3. Request new code if expired
```

---

### Step 9: Select Support Plan

**What you'll see:**
```
Select a Support Plan
====================

Basic Support - Free
  ✓ AWS Trusted Advisor
  ✓ AWS Personal Health Dashboard
  ✓ Customer service for account and billing
  ✓ Documentation, whitepapers, support forums

  [Select] ← Choose this one

Developer Support - $29/month
  ✓ Everything in Basic
  ✓ Technical support via email
  ✓ Response time: 12-24 hours

  [Select]

Business Support - $100/month
  ✓ Everything in Developer
  ✓ 24/7 phone and chat support
  ✓ Response time: < 1 hour

  [Select]

Enterprise Support - $15,000/month
  ✓ Everything in Business
  ✓ Dedicated Technical Account Manager
  ✓ Response time: < 15 minutes

  [Select]
```

**⚠️ IMPORTANT: Choose "Basic Support - Free"**

**Why:**
```
For our project:
  ✓ Basic Support is enough
  ✓ We don't need phone/chat support
  ✓ Documentation is available
  ✓ Community forums help with issues
  ✓ Saves $29-$15,000 per month!

When you might need paid support:
  ✗ Running production business (not us yet)
  ✗ Need 24/7 help (we're learning)
  ✗ Have critical downtime issues (not applicable)
```

**Action:**
1. Scroll to **"Basic Support - Free"**
2. Click **"Select"** button under it
3. Ignore all other options

**What happens next:**
- Confirmation message appears
- Account creation is processing
- Takes 20-60 seconds

---

### Step 10: Welcome to AWS!

**What you'll see:**
```
Congratulations!
====================

Your AWS account is being set up.

You'll receive an email when your account is ready.
This usually takes a few minutes.

Current status: [Processing...]

[ Go to AWS Management Console ]
```

**Understanding the wait:**

```
What AWS is doing:
  1. Creating your account
  2. Allocating $100 credits
  3. Setting up billing
  4. Preparing services
  5. Sending welcome email

Time: 1-5 minutes (usually)
Sometimes: Up to 24 hours (rare)
```

**Options:**

**Option A: Wait on this page**
- Page automatically updates
- When ready: "Go to AWS Management Console" button activates
- Click it to enter your account

**Option B: Check email**
- Subject: "Welcome to Amazon Web Services"
- Contains confirmation
- Link to sign in

**Option C: Try signing in**
- Go to: https://console.aws.amazon.com/
- Enter your email
- Click "Next"
- If account ready: You'll proceed to password
- If not ready: Error message (wait longer)

---

### Step 11: First Sign-In to AWS Console

**Go to:** https://console.aws.amazon.com/

**What you'll see:**
```
Sign in
====================

Root user email address: [___________________]

[ Next ]

Don't have an account? [ Sign up ]
```

**Steps:**

1. **Enter your email**
   - The email you used to create account
   - Example: ramesh.kumar@gmail.com

2. **Click "Next"**

3. **Enter password:**
   ```
   Sign in as Root user
   ====================

   Email: ramesh.kumar@gmail.com

   Password: [___________________]

   [ ] Keep me signed in

   [ Sign in ]
   ```

4. **Type your password**
   - The one you created in Step 4
   - Case-sensitive!

5. **"Keep me signed in" checkbox:**
   - Check it if using your own computer
   - Don't check if using shared/public computer

6. **Click "Sign in"**

**What happens:**
- AWS verifies credentials
- Loads AWS Management Console
- Shows dashboard

**Congratulations! You're in! 🎉**

---

## Understanding Verification

### Why AWS Verifies You

**AWS needs to verify:**

1. **You're a real person** (not a bot)
2. **One account per person** (prevent abuse)
3. **Valid payment method** (backup if you exceed limits)
4. **Reachable contact info** (send important alerts)

### What Gets Verified

```
✓ Email          → Can they send you notifications?
✓ Phone          → Can they reach you in emergency?
✓ Credit Card    → Is it valid? (charges ₹2, refunds it)
✓ Address        → Is it real?
```

### Normal vs. Additional Verification

**Normal verification (90% of users):**
- Email verification code
- Phone SMS/call
- Credit card ₹2 charge
- **Done in 10 minutes**

**Additional verification (10% of users):**
- Sometimes AWS asks for ID proof
- Why? Fraud prevention, unusual patterns
- What to send: Photo of Aadhar/PAN/Passport
- Upload via AWS console
- **Done in 24-48 hours**

**If asked for additional verification:**
```
Don't panic! It's normal.

Steps:
  1. AWS sends email with instructions
  2. Open email, click link
  3. Upload photo of ID (clear, readable)
  4. Wait for approval (1-2 days usually)
  5. Get confirmation email
  6. Account activated
```

---

## Credit Card Setup

### Why AWS Needs Your Card

**Let me explain exactly why AWS requires a credit card, even though the Free Plan is free:**

**Reason 1: Identity Verification**
```
Without card requirement:
  → One person could create 100 accounts
  → Get $20,000 in credits ($200 × 100)
  → Mine cryptocurrency for free
  → Massive abuse of system

With card requirement:
  → One card = One account
  → Cannot abuse
  → Fair for everyone
```

**Reason 2: Safety Net**
```
Scenario: You accidentally launch expensive service

Without card:
  → AWS blocks your account immediately
  → Lose all data
  → No warning

With card:
  → Service keeps running
  → You get billing alert
  → Chance to fix mistake
  → Only charged for what you use
```

**Reason 3: Global Standard**
```
All major cloud providers require card:
  ✓ AWS
  ✓ Google Cloud (GCP)
  ✓ Microsoft Azure
  ✓ DigitalOcean
  ✓ Linode

It's industry standard, not just AWS.
```

### What AWS Charges

**During signup:**
```
₹2 (approximately $0.02)
  → Temporary authorization hold
  → Verifies card is valid
  → Refunded within 3-5 business days
  → Shows as "AMAZON WEB SERVICES" on statement
```

**During Free Plan (6 months):**
```
$0 - As long as you:
  ✓ Stay within $200 credits
  ✓ Don't launch non-free services
  ✓ Follow our setup guide
  ✓ Set up billing alerts
```

**If you exceed free tier:**
```
Only then charges begin
  → You get email alert first
  → Card charged for excess usage
  → Example: Use $205 worth → Charged $5
```

### Card Requirements

**Your card must:**
- Be Visa, Mastercard, American Express, or RuPay
- Have **international transactions enabled** (very important!)
- Be in your name (matches account name)
- Have at least ₹2 available balance
- Not be a prepaid/virtual card (most banks reject these)

**To enable international transactions:**
```
For most Indian banks:

Option 1: Banking App
  1. Open your bank's mobile app
  2. Go to Cards section
  3. Find your card
  4. Look for "International Usage" or "Online Transactions"
  5. Enable it
  6. May need to set limit (₹10,000 is enough)

Option 2: Call Bank
  1. Call customer service
  2. Ask: "Please enable international transactions on my card"
  3. They may ask: Purpose? → "For cloud services"
  4. Takes 5 minutes

Option 3: NetBanking
  1. Login to net banking
  2. Cards section
  3. Enable international transactions
```

### What Shows on Your Statement

**After signup:**
```
Transaction: AMAZON WEB SERVICES
Amount: ₹2
Status: Pending

After 3-5 days:
Transaction: AMAZON WEB SERVICES REFUND
Amount: ₹2
Status: Completed
```

**If you actually use paid services:**
```
Transaction: AWS SERVICES
Amount: (varies)
Description: Invoice #1234567890
Date: End of month
```

### Card Safety

**Is it safe to give AWS your card?**

**Yes, because:**
1. AWS is owned by Amazon (trillion-dollar company)
2. PCI-DSS compliant (highest security standard)
3. Same security as Amazon shopping
4. Used by millions worldwide
5. Card info encrypted, not stored by AWS directly

**Extra protection:**
- Most cards have zero-liability protection
- If fraud occurs, bank refunds you
- AWS fraud protection monitors unusual activity

**Pro tip:** Use a card with low limit (₹10,000-50,000) for extra peace of mind.

---

## CRITICAL: Setting Up Billing Alerts

**⚠️ DO THIS IMMEDIATELY AFTER ACCOUNT CREATION**

This is the MOST IMPORTANT safety step. Set this up before doing anything else!

### Why Billing Alerts Matter

**Without billing alerts:**
```
Day 1: Accidentally launch large instance
Day 15: Using services, don't notice
Month end: $500 bill!
Result: Surprise bill, no warning
```

**With billing alerts:**
```
Day 1: Accidentally launch large instance
Day 1 (2 hours later): Email: "You've spent $1!"
Day 1 (3 hours later): You fix the mistake
Month end: $1 bill (instead of $500)
```

### Step-by-Step: Create Billing Alerts

**Step 1: Open Billing Dashboard**

1. You're signed into AWS Console: https://console.aws.amazon.com/
2. Top-right corner: Click your **account name** (e.g., "Ramesh Kumar")
3. Dropdown menu appears
4. Click **"Billing and Cost Management"**

**Alternative method:**
- Type "Billing" in search bar (top of AWS Console)
- Click "Billing and Cost Management" in results

**What you'll see:**
```
Billing Dashboard
====================

Month-to-date spend:    $0.00
Forecasted spend:       $0.00
Free tier usage:        [View details]

Quick links:
  • Bills
  • Budgets
  • Cost Explorer
  • Free Tier
```

---

**Step 2: Create Your First Budget**

1. Left sidebar: Click **"Budgets"**
2. Click button: **"Create budget"**

**What you'll see:**
```
Create budget
====================

Use a template or customize
( ) Use a template (simplified)
( ) Customize (advanced)

[Select one to continue]
```

3. Choose **"Use a template (simplified)"**
4. Click **"Continue"** or it auto-expands

---

**Step 3: Configure Budget #1 - $1 Alert**

**Template options:**
```
Templates available:
( ) Zero spend budget
( ) Monthly cost budget  ← Select this
( ) Daily savings plans coverage budget
```

1. Select **"Monthly cost budget"**

**Fill in the form:**

```
Budget name: [________________]
  → Enter: Alert-1-Dollar

Budgeted amount ($): [_____]
  → Enter: 1

Email recipients: [________________]
  → Enter: yourname@gmail.com (your email)

[ Create budget ]
```

**Example:**
```
Budget name: Alert-1-Dollar
Budgeted amount: $1
Email: ramesh.kumar@gmail.com
```

2. Click **"Create budget"**

**What happens:**
- Budget created successfully
- Shows in budget list
- You'll get email when spend reaches:
  - 80% of $1 (at $0.80)
  - 100% of $1 (at $1.00)
  - Over budget (at $1.01+)

---

**Step 4: Create Budget #2 - $5 Alert**

**Repeat the process for more safety levels:**

1. Click **"Create budget"** again
2. Select **"Use a template"**
3. Select **"Monthly cost budget"**
4. Fill in:
   ```
   Budget name: Alert-5-Dollars
   Budgeted amount: 5
   Email: yourname@gmail.com
   ```
5. Click **"Create budget"**

---

**Step 5: Create Budget #3 - $10 Alert**

Repeat once more:

1. Click **"Create budget"** again
2. Template: Monthly cost budget
3. Fill in:
   ```
   Budget name: Alert-10-Dollars
   Budgeted amount: 10
   Email: yourname@gmail.com
   ```
4. Click **"Create budget"**

---

**Step 6: Create Budget #4 - $25 Alert (Half Credits)**

One more (this is half of your $200 credits - important checkpoint):

1. Click **"Create budget"** again
2. Template: Monthly cost budget
3. Fill in:
   ```
   Budget name: Alert-25-Dollars-Half-Credits
   Budgeted amount: 25
   Email: yourname@gmail.com
   ```
4. Click **"Create budget"**

---

**Step 7: Verify All Budgets Are Active**

**Check your budget list:**
```
Your budgets (4 total)
====================

Name                          Amount    Status
Alert-1-Dollar                $1        Active ✓
Alert-5-Dollars               $5        Active ✓
Alert-10-Dollars              $10       Active ✓
Alert-25-Dollars-Half-Credits $25       Active ✓
```

**Test email notification:**
1. Check your email inbox
2. Subject: "AWS Budgets: You created a new budget"
3. Open email, verify it arrived
4. If no email: Check spam folder

---

### Understanding Budget Alerts

**What happens when you hit a budget:**

```
Example: You hit $1 spending

Email 1 (at $0.80 - 80%):
  Subject: "AWS Budgets: Alert-1-Dollar has exceeded 80%"
  Body: "Your AWS costs are $0.80 (80% of $1 budget)"
  Action: Log in and check what's running

Email 2 (at $1.00 - 100%):
  Subject: "AWS Budgets: Alert-1-Dollar has exceeded your budget"
  Body: "Your AWS costs are $1.00 (100% of $1 budget)"
  Action: Investigate immediately!

Email 3 (at $1.01+ - Over budget):
  Subject: "AWS Budgets: Alert-1-Dollar is over budget"
  Body: "Your AWS costs are $1.05 (105% of $1 budget)"
  Action: Stop services causing charges!
```

**What budgets DON'T do:**
```
✗ Don't automatically stop services
✗ Don't prevent charges
✗ Don't limit spending

They only:
✓ Send email alerts
✓ Let you know what's happening
✓ Give you chance to react
```

**To actually stop charges:**
- You must manually stop/delete services
- Or set up AWS Cost Anomaly Detection (advanced)

---

### Monitoring Your Spending

**Daily check (30 seconds):**

1. Go to Billing Dashboard
2. Look at "Month-to-date spend"
3. Should be ~$0.90/day ($27/month ÷ 30 days)
4. If higher → investigate what's running

**Weekly check (2 minutes):**

1. Go to Billing → Bills
2. Review "By Service" breakdown:
   ```
   Service          Charges
   RDS              $3.50
   EC2              $1.75
   Data Transfer    $0.12
   Total:           $5.37
   ```
3. Verify expected services only
4. Look for unexpected services

**Monthly check (5 minutes):**

1. Go to Billing → Bills
2. Download full invoice (PDF)
3. Review all charges
4. Verify against expected $27/month

---

## Completing the 5 Tasks for $100 Extra Credits

Now let's earn that extra $100! These tasks are designed to introduce you to AWS services.

**Current credits:** $100
**After completing tasks:** $200
**Time required:** 15-20 minutes

---

### Task 1: Launch & Terminate EC2 Instance ($20)

**What is EC2?**
- Elastic Compute Cloud (virtual server)
- The most popular AWS service
- We'll use this for Metabase later

**Steps:**

1. **Go to EC2 Dashboard:**
   - AWS Console search bar → Type "EC2"
   - Click "EC2" in results
   - Or go to: https://console.aws.amazon.com/ec2/

2. **Launch Instance:**
   - Big orange button: **"Launch Instance"**
   - Click it

3. **Configure Instance (Quick Setup):**
   ```
   Name: test-task1

   Application and OS Images:
   → Select: Amazon Linux 2023

   Instance type:
   → Select: t2.micro (Free tier eligible)

   Key pair:
   → Select: "Proceed without a key pair"

   (Leave everything else default)
   ```

4. **Click "Launch instance"** (orange button, bottom-right)

5. **Wait 2 minutes** for instance to start
   - Status changes: Pending → Running
   - Refresh page if needed

6. **Terminate Instance (Important!):**
   - Check the box next to "test-task1"
   - Top-right: **Instance state** dropdown
   - Click **"Terminate instance"**
   - Confirm termination
   - Status changes to: Terminated

**Why terminate?**
- We don't need it running
- Saves credits
- Task only requires launching, not keeping it running

**Verification:**
- Check email: "AWS Task Completion: $20 credit earned"
- Or check AWS Console → Billing → Credits

**Task 1 Complete! ✓** ($20 earned)

---

### Task 2: Launch RDS Database ($20)

**What is RDS?**
- Relational Database Service
- This is what we'll use for PostgreSQL!
- Perfect task since we need it anyway

**Steps:**

1. **Go to RDS Dashboard:**
   - Search bar → Type "RDS"
   - Click "RDS" in results

2. **Create Database:**
   - Button: **"Create database"**
   - Click it

3. **Choose Creation Method:**
   ```
   ( ) Standard create
   ( ) Easy create  ← Select this
   ```

4. **Configuration:**
   ```
   Engine type:
   ( ) MySQL
   ( ) MariaDB
   (•) PostgreSQL  ← Select this
   ( ) SQL Server

   DB instance size:
   (•) Free tier  ← Important! Select this

   DB instance identifier: test-database-task2

   Master username: postgres (default, keep it)

   Master password: [Auto-generate] ← Use this option
   ```

5. **Click "Create database"** (orange button, bottom)

6. **Wait for creation:**
   - Status: Creating...
   - Takes 3-5 minutes
   - You can move to Task 3 while waiting!

**Note:** We'll delete this test database later. In a future lesson, we'll create our real production database.

**Task 2 Complete! ✓** ($20 earned)

---

### Task 3: Create Lambda Function ($20)

**What is Lambda?**
- Serverless computing
- Run code without managing servers
- Not needed for our project, but easy task!

**Steps:**

1. **Go to Lambda Dashboard:**
   - Search bar → "Lambda"
   - Click "Lambda"

2. **Create Function:**
   - Button: **"Create function"**
   - Click it

3. **Basic Information:**
   ```
   ( ) Use a blueprint
   (•) Author from scratch  ← Select
   ( ) Container image

   Function name: test-function-task3

   Runtime: Python 3.12 (or latest)
   ```

4. **Click "Create function"** (bottom-right)

5. **Add Function URL** (Required for task credit):
   - Function page loads
   - Top-right: Click **"Create function URL"**
   - Dialog appears:
     ```
     Auth type:
     ( ) AWS_IAM
     (•) NONE  ← Select this

     [ ] Configure cross-origin resource sharing (CORS)
     Leave unchecked

     [Save]
     ```
   - Click **"Save"**

6. **Function URL created:**
   - Shows URL like: https://abc123.lambda-url.ap-south-1.on.aws/
   - Copy it if you want, or ignore it
   - We won't use it

**Task 3 Complete! ✓** ($20 earned)

---

### Task 4: Use Amazon Bedrock ($20)

**What is Bedrock?**
- AI service (like ChatGPT)
- Run AI models
- Easiest task!

**Steps:**

1. **Go to Bedrock:**
   - Search bar → "Bedrock"
   - Click "Amazon Bedrock"

2. **First-time setup:**
   - Might see: "Get started with Amazon Bedrock"
   - Click any "Get started" or "Enable" buttons
   - Accept default settings

3. **Open Playgrounds:**
   - Left sidebar → **"Playgrounds"**
   - Or click **"Text"** under Playgrounds

4. **Select Model:**
   ```
   Model:
   - Look for "Claude" or "Titan Text" or any available model
   - Some models may need to be enabled first
   - Click "Enable" if needed
   ```

5. **Test the Model:**
   ```
   Text input box:
   Type: Hello, what is AWS?

   Click: [Run]
   ```

6. **See Response:**
   - AI responds with answer about AWS
   - That's it! Task complete!

**If model access needed:**
- Some regions require requesting access
- Click "Request model access"
- Select any free model (Claude Instant, Titan, etc.)
- Submit request
- Usually approved instantly
- Then run the playground

**Task 4 Complete! ✓** ($20 earned)

---

### Task 5: Set Cost Budget ($20)

**Good news:** We already did this!

In the "Setting Up Billing Alerts" section, when we created budgets, that counted as Task 5.

**If you haven't done it yet:**
- Scroll up to "CRITICAL: Setting Up Billing Alerts"
- Follow Step 2-3 to create ONE budget
- That completes this task

**Task 5 Complete! ✓** ($20 earned)

---

### Verify All Tasks Complete

**Check your credits:**

1. **Go to Billing Dashboard**
   - Top-right → Your name → Billing and Cost Management

2. **Click "Credits"** (left sidebar)

3. **What you should see:**
   ```
   AWS Credits Summary
   ====================

   Available credits: $200.00

   Credit breakdown:
   - Sign-up bonus:              $100.00
   - EC2 task completion:         $20.00
   - RDS task completion:         $20.00
   - Lambda task completion:      $20.00
   - Bedrock task completion:     $20.00
   - Budget task completion:      $20.00

   Total: $200.00
   Expires: [6 months from signup]
   ```

**If you don't see all $200:**
- Check email for task completion notifications
- Sometimes takes 24 hours to reflect
- As long as you completed tasks, credits will appear
- Refresh page, wait a bit

---

### Clean Up Test Resources

**Important:** Delete the test resources we created, so they don't use credits!

**Delete Test EC2 Instance:**
- Already terminated in Task 1 ✓

**Delete Test RDS Database:**
1. Go to RDS Dashboard
2. Find "test-database-task2"
3. Select it (checkbox)
4. Actions dropdown → **Delete**
5. Dialog appears:
   ```
   Create final snapshot?
   ( ) Yes
   (•) No  ← Select this (it's just a test)

   [ ] I acknowledge that upon instance deletion, automated backups...
   ✓ Check this box

   Type "delete me" to confirm: [delete me]
   ```
6. Type "delete me"
7. Click **"Delete"**
8. Takes 5-10 minutes to delete

**Delete Test Lambda Function:**
1. Go to Lambda Dashboard
2. Find "test-function-task3"
3. Select it (checkbox)
4. Actions → **Delete**
5. Confirm deletion

**Bedrock:**
- Nothing to delete, playground doesn't create persistent resources

**Budgets:**
- Keep these! They're protecting you

---

## Verifying Your Free Plan Status

Let's make sure you're on the Free Plan and have $200 credits.

### Step 1: Check Plan Type

1. **Go to Billing Dashboard**
   - Top-right → Account name → Billing and Cost Management

2. **Look for Plan Information**
   - Should say: **"Free Plan"** or **"Free Tier"**
   - If says "Paid Plan" → You selected wrong option during signup!

**If you accidentally chose Paid Plan:**
```
Don't panic! You can switch.

Steps:
  1. Go to Billing Dashboard
  2. Click "Payment methods"
  3. Look for "Change plan" or contact AWS Support
  4. Or create new account (if less than 24 hours old)

Better: Complete this lesson on Free Plan to be sure
```

---

### Step 2: Verify $200 Credits

1. **Billing Dashboard → Credits** (left sidebar)

2. **Check amount:**
   ```
   Total available: $200.00

   If less:
   - $100 → Only got sign-up bonus, tasks not complete
   - $120-$180 → Some tasks complete, finish remaining
   - $200 → Perfect! All done ✓
   ```

---

### Step 3: Check Expiration Date

**In Credits page, look for:**
```
Expires: July 22, 2026
(or 6 months from your signup date)
```

**Mark this date in your calendar:**
- Set reminder for 1 month before (to decide: upgrade or export)
- Example: If expires July 22, set reminder for June 22

---

### Step 4: Verify Free Tier Tracking

1. **Billing Dashboard → Free Tier** (left sidebar)

2. **What you'll see:**
   ```
   AWS Free Tier Usage
   ====================

   Service          Usage           Limit           % Used
   EC2              0 hrs           750 hrs/month   0%
   RDS              0 hrs           750 hrs/month   0%
   S3               0 GB            5 GB            0%
   Data Transfer    0 GB            15 GB           0%
   ```

3. **This is informational only**
   - With new credit-based system, these limits don't apply
   - Your $200 credits are what matter
   - Still useful to track usage patterns

---

## Setting Default Region to Mumbai

**Why this matters:**
- AWS has data centers worldwide (regions)
- You'll use Mumbai region (fastest for India)
- Must set it as default or you'll accidentally use wrong region
- Different regions = different costs!

### Understanding Regions

**AWS Regions worldwide:**
```
US East (Virginia)     us-east-1
US West (Oregon)       us-west-2
Europe (Ireland)       eu-west-1
Europe (Frankfurt)     eu-central-1
Asia (Mumbai)          ap-south-1     ← We'll use this
Asia (Singapore)       ap-southeast-1
Asia (Tokyo)           ap-northeast-1
... and 30+ more
```

**Why Mumbai (ap-south-1)?**
```
✓ Closest to India → Fastest speed
✓ Lowest latency (ping time)
✓ Cheaper data transfer within India
✓ Supports all services we need (RDS, EC2, etc.)
✓ Prices in USD but optimized for region
```

### How to Set Default Region

**Step 1: Find Current Region**

Look at top-right of AWS Console:
```
[Your Name ▼] [ap-south-1 ▼]  [Support ▼]
               ↑
          Current region
```

**It might show:**
- US East (N. Virginia) - Default for many users
- Asia Pacific (Singapore)
- Europe (Ireland)
- Or something else

**Step 2: Change to Mumbai**

1. Click the **region dropdown** (top-right)

2. **List of regions appears:**
   ```
   [Search regions...]

   US East (Ohio)
   US East (N. Virginia)
   US West (N. California)
   ...
   Asia Pacific (Mumbai)     ← Find this
   Asia Pacific (Seoul)
   Asia Pacific (Singapore)
   ...
   ```

3. **Scroll down** to find **"Asia Pacific (Mumbai)"**

4. **Click it**

5. **Region changes:**
   - Top-right now shows: **ap-south-1**
   - Page reloads
   - All services now in Mumbai region

**Step 3: Verify**

Check region indicator:
```
Should show: ap-south-1
Or: Asia Pacific (Mumbai)
```

**Important:** **Every time you log in**, verify you're in Mumbai region!

### Region Gotchas

**Problem 1: Services in wrong region**
```
You create RDS database in Singapore
Later, create EC2 in Mumbai
Result: They can't talk to each other easily!
         Higher data transfer costs

Solution: ALWAYS check region before creating anything
```

**Problem 2: "Service not available"**
```
Some newer services aren't in all regions
If you see "Not available in this region"
→ The service doesn't exist in Mumbai yet
→ Use alternative service or different region
```

**Problem 3: Accidentally switching regions**
```
You're working on project
Click region dropdown by accident
Suddenly "Where are my resources?"
→ They're still there, just in other region!
→ Switch back to Mumbai
```

**Pro Tip:** Some people put sticky note on monitor: "CHECK REGION: ap-south-1" 😄

---

## Understanding the AWS Console

Let's tour the AWS Management Console so you know where everything is.

### Main Console Dashboard

**What you see when logged in:**

```
+----------------------------------------------------------+
| AWS  [Search]                     [ap-south-1▼] [Name▼]  | ← Top bar
+----------------------------------------------------------+
|                                                           |
| Recently visited                                          |
| [EC2] [RDS] [S3] [Lambda]                                |
|                                                           |
| Favorites                                                 |
| [Add service shortcuts here]                              |
|                                                           |
| Build a solution                                          |
| [Launch a virtual machine]                                |
| [Deploy a web app]                                        |
| [Create a database]                                       |
|                                                           |
| Explore AWS                                               |
| [What's new] [Documentation] [Tutorials]                  |
|                                                           |
+----------------------------------------------------------+
```

### Key Components

**1. Top Bar:**
```
[AWS Logo] - Click to return to homepage

[Search bar] - Type service name
  Examples: "EC2", "RDS", "billing"
  Fastest way to find anything

[ap-south-1 ▼] - Region selector
  ALWAYS verify this before doing anything!

[Your Name ▼] - Account menu
  → Billing and Cost Management
  → Account settings
  → Security credentials
  → Sign out
```

**2. Services Menu:**
```
Top-left: Click [Services] or [☰] hamburger menu

Categories:
  → Compute (EC2, Lambda, etc.)
  → Storage (S3, EBS, etc.)
  → Database (RDS, DynamoDB, etc.)
  → Networking (VPC, Route 53, etc.)
  → Security (IAM, etc.)
  → ... and 200+ more services
```

**3. Recently Visited:**
- Services you used recently
- Quick access
- Updates automatically

**4. Favorites:**
- Pin services you use often
- Click star icon to favorite
- Customize your dashboard

### Services We'll Use

**For our project, you'll mainly use:**

```
1. RDS (Database)
   → Create PostgreSQL database
   → Manage database settings
   → View connections

2. EC2 (Virtual Server)
   → Create server for Metabase
   → Start/stop instances
   → Manage security groups

3. VPC (Networking)
   → Set up private network
   → Configure security
   → (AWS creates default VPC automatically)

4. Billing Dashboard
   → Check spending
   → View credits
   → Manage budgets

5. IAM (Security)
   → Create users
   → Manage permissions
   → (We'll set this up for security)
```

**200+ other services:** We won't use them. Ignore them!

### Navigation Tips

**Tip 1: Use Search (Fastest)**
```
Instead of: Services menu → Database → RDS
Just do: Search "RDS" → Enter
Saves clicks!
```

**Tip 2: Breadcrumb Navigation**
```
Top of page shows where you are:
Services > RDS > Databases > my-database

Click any part to go back:
Click "Databases" → See all databases
Click "RDS" → RDS home
```

**Tip 3: Service Homepage vs. Dashboard**
```
Each service has:
  - Homepage (overview, getting started)
  - Dashboard (your actual resources)

If lost, click service name in breadcrumb
```

**Tip 4: Resource Lists**
```
Each service shows your resources:
EC2 → Instances
RDS → Databases
S3 → Buckets

If empty: "No resources found"
Normal when starting!
```

---

## Security Best Practices

**Critical:** AWS security is VERY important. Follow these practices from day one.

### Practice 1: Protect Your Root Account

**What is Root Account?**
- The account you just created (with your email)
- Has UNLIMITED power (can do anything)
- Can delete everything, spend millions
- Like "Administrator" on Windows, but more powerful

**Security Rules:**

**Rule 1: Enable MFA (Multi-Factor Authentication)**

**What is MFA?**
```
Login requires TWO things:
  1. Password (something you know)
  2. Code from phone (something you have)

Even if someone steals password, can't log in without your phone!
```

**How to enable MFA:**

1. **Top-right → Your name → Security credentials**

2. **Find "Multi-factor authentication (MFA)"**

3. **Click "Assign MFA device"**

4. **Choose MFA type:**
   ```
   ( ) Virtual MFA device (app on phone) ← Recommended
   ( ) Hardware MFA device (physical key)
   ( ) FIDO security key
   ```

5. **Select "Virtual MFA device"** → Continue

6. **Install authenticator app on phone:**
   - Google Authenticator (Android/iOS)
   - Microsoft Authenticator (Android/iOS)
   - Authy (Android/iOS)

   All free, download from app store

7. **Scan QR code:**
   - AWS shows QR code
   - Open authenticator app
   - Click "Add account" or "+"
   - Scan QR code with phone camera
   - App shows 6-digit code (changes every 30 seconds)

8. **Enter TWO consecutive codes:**
   ```
   MFA code 1: [______]  ← Enter current code

   (Wait 30 seconds for code to change)

   MFA code 2: [______]  ← Enter new code
   ```

9. **Click "Assign MFA"**

10. **MFA enabled! ✓**

**From now on, when you log in:**
```
Step 1: Enter email
Step 2: Enter password
Step 3: Enter 6-digit code from authenticator app
→ Then you're in!
```

**IMPORTANT: Write down backup codes!**
- AWS gives emergency backup codes
- Save them in safe place
- If you lose phone, you can still log in

---

**Rule 2: Don't Use Root Account for Daily Work**

**Why not?**
```
Root account has unlimited power.
If hacked: Attacker can delete everything.

Better approach:
  Use root only for:
    - Billing changes
    - Account settings
    - Emergency situations

  Create IAM user for daily work:
    - Limited permissions
    - If hacked: Limited damage
    - Easy to revoke
```

**We'll create IAM user in next lesson.**

---

### Practice 2: Strong Password

**Requirements:**
```
✓ At least 12 characters (longer = better)
✓ Mix of uppercase, lowercase, numbers, symbols
✓ Not a dictionary word
✓ Not related to personal info (birthday, name, etc.)
✓ Unique (don't reuse from other sites)
```

**Good password examples:**
```
✓ CloudDB$2025!Swadha
✓ MyInv3nt0ry#AWS@2025
✓ SecureP@ssw0rd!AWS
```

**Bad password examples:**
```
✗ password123
✗ Swadha2025  (too simple)
✗ your birthday
```

**Password management:**
- Use password manager (LastPass, 1Password, Bitwarden)
- Or write in notebook (keep it safe!)
- Change password every 6 months

---

### Practice 3: Monitor Your Account

**Daily:**
- Check Billing Dashboard
- Verify charges are expected
- Look for unfamiliar services

**Weekly:**
- Review running resources (EC2, RDS)
- Check CloudTrail logs (who did what)
- Verify no unexpected users

**Monthly:**
- Download and review invoice
- Check for unused resources
- Clean up test resources

---

### Practice 4: Never Share Credentials

**NEVER share:**
```
✗ AWS password
✗ MFA device
✗ Access keys (we'll create these later)
✗ Console login link
```

**Instead, for team members:**
- Create separate IAM user for each person
- Give minimum permissions needed
- Revoke access when person leaves

---

### Practice 5: Set Up CloudTrail (Audit Log)

**What is CloudTrail?**
```
Records every action in your AWS account:
  - Who logged in
  - What they did
  - When they did it
  - From which IP address

Like CCTV camera for your AWS account!
```

**Enable CloudTrail:**

1. Search → "CloudTrail"
2. Click "Create trail"
3. Name: audit-log
4. Storage: Create new S3 bucket (default)
5. Click "Create trail"

**Free tier:** First trail is FREE!

---

### Practice 6: Recognize Phishing

**AWS will NEVER:**
```
✗ Email asking for password
✗ Email asking for credit card details
✗ Call asking for account verification
✗ Send suspicious links to "verify account"
```

**Legitimate AWS emails:**
```
✓ Billing notifications (from aws.amazon.com)
✓ Service updates (from amazonaws.com)
✓ Security alerts (from aws.amazon.com)

Always check sender email address!
```

**If suspicious email:**
1. Don't click links
2. Go to console.aws.amazon.com directly
3. Check notifications there
4. Report phishing to: abuse@amazonaws.com

---

## Summary & Next Steps

### What You Accomplished Today! 🎉

```
✓ Created AWS Free Tier account
✓ Verified email and phone
✓ Added payment method (card)
✓ Set up billing alerts ($1, $5, $10, $25)
✓ Completed 5 onboarding tasks
✓ Earned $200 in credits
✓ Selected Free Plan (not Paid)
✓ Set default region to Mumbai (ap-south-1)
✓ Learned AWS Console navigation
✓ Enabled MFA for security
✓ Cleaned up test resources
```

**Current Status:**
```
Account: Active ✓
Credits: $200
Charges: $0
Region: ap-south-1 (Mumbai)
Security: MFA enabled
Budgets: 4 alerts set
Expires: 6 months from today
```

You're ready to build!

---

### Pre-Flight Checklist for Next Lesson

Before Lesson 4, verify:

```
Account Setup:
  ✓ Can log in to AWS Console
  ✓ MFA working (have phone with authenticator app)
  ✓ Region set to ap-south-1 (Mumbai)
  ✓ Billing alerts receiving emails
  ✓ $200 credits showing in Billing Dashboard

Local Computer Setup:
  ✓ Python installed (you have this from Phase 1)
  ✓ Google Sheets access working (from Phase 1)
  ✓ Comfortable with command line basics

Knowledge:
  ✓ Understand credits vs. charges
  ✓ Know how to check billing
  ✓ Comfortable navigating AWS Console
  ✓ Know your password and MFA device location
```

---

### What's Next: Lesson 4 Preview

**Lesson 4: Designing Your Database Schema**

We'll cover:
- Understanding database design principles
- Analyzing your inventory data structure
- Creating tables for:
  - Inventory items
  - MyBillBook sync history
  - Sales transactions (future)
  - Categories
- Understanding relationships (foreign keys)
- Choosing data types (VARCHAR, INTEGER, DECIMAL, etc.)
- Indexing for performance
- Documenting the schema

**Why design first?**
```
Good database design = Fast queries, easy to use
Bad database design = Slow, confusing, hard to fix later

We'll spend time designing BEFORE creating database.
Saves time and headaches!
```

**Time needed:** 30-45 minutes (reading + planning)

---

### Troubleshooting Common Issues

**Issue: Can't log in**
```
Solutions:
  1. Verify email (check spelling)
  2. Try password reset
  3. Check MFA app has correct time
  4. Clear browser cache
  5. Try different browser
```

**Issue: Credit card declined**
```
Solutions:
  1. Enable international transactions
  2. Call bank, explain it's for AWS
  3. Try different card
  4. Verify card not expired
```

**Issue: Tasks not showing $20 credit**
```
Solutions:
  1. Wait 24 hours (sometimes delayed)
  2. Check email for completion notification
  3. Redo task if no notification
  4. Contact AWS Support if still missing after 48 hours
```

**Issue: Accidentally deleted something important**
```
Solutions:
  At this stage: Nothing critical exists yet!
  Later: We'll set up backups
  For now: Just recreate if needed
```

**Issue: Charges appearing**
```
Solutions:
  1. Check it's not the ₹2 verification (gets refunded)
  2. Review what services are running
  3. Delete/stop unnecessary resources
  4. Contact AWS Support if unexpected
```

---

### Important Reminders

**Remember:**

1. **Always check region:** ap-south-1 before creating anything
2. **Monitor spending weekly:** Billing Dashboard
3. **Keep MFA device safe:** Can't log in without it
4. **Don't create random resources:** Everything costs credits
5. **Delete test resources:** Don't let them run
6. **Mark calendar:** 6-month expiration date

**Emergency Contact:**
- AWS Support: https://console.aws.amazon.com/support/
- Billing Issues: Open support case from Billing Dashboard

---

## Congratulations! 🎉

You've successfully created your AWS account and set up proper security and billing protection!

This was the longest and most detailed lesson because setting up correctly from the start prevents problems later.

**You are now ready to:**
- Design your database schema (Lesson 4)
- Launch your PostgreSQL database (Lesson 5)
- Migrate data from Google Sheets (Lesson 6)
- Build beautiful dashboards (Lessons 7-8)

**Take a break, then let me know when you're ready for Lesson 4!**

---

**Documentation saved:** `docs/PHASE2_LESSON3_CREATE_AWS_ACCOUNT.md`
