# How Swadha Automation Works
## Simple Guide for Everyone 👥

---

## 🎯 What Does This Do?

**In Simple Words:**
This system takes your raw inventory data and automatically:
1. ✅ Organizes it (removes duplicates)
2. ✅ Matches it with what's already in MyBillBook
3. ✅ Separates NEW items from EXISTING items
4. ✅ Creates printable labels

**Why?** So you don't have to manually check which items are new vs old, and you can quickly import everything to MyBillBook!

---

## 📋 The 4 Simple Steps

```
Step 0: Get Latest Data from MyBillBook
   ↓
Step 1: Organize & Match Your Inventory
   ↓
Step 2: Create Import Files for MyBillBook
   ↓
Step 3: Create Labels for Printing
```

---

## 🔄 Complete Workflow (Visual)

### STEP 0: Download Current MyBillBook Data
**What happens:** The system downloads all your current MyBillBook inventory

```
    🌐 MyBillBook Website
         │
         │ (Downloads 352 items)
         ▼
    📊 Google Sheet: "myBillBook Inventory"

    ✓ Now we know what items you already have
```

**You do:** Just click Menu Option 0

---

### STEP 1: Organize & Smart Match

#### What You Start With:
```
📝 Your Manual Entry ("Inventory RAW" sheet):

+========================================+
| Type     Name   Cost   Qty   Sell      |
| ------   ----   ----   ---   ----      |
| Ear              110    2     250      | <- Row 1
| Ear              110    2     250      | <- Row 2 (duplicate!)
| Ear      SL      45     3     199      | <- Row 3
| ...                                    |
+========================================+
    Total: 78 rows (with duplicates)
```

#### What The System Does:

**Part A: Combine Duplicates**
```
Row 1: Ear | (blank) | 110 | 2 | 250
Row 2: Ear | (blank) | 110 | 2 | 250
          ↓ ↓ ↓ COMBINES ↓ ↓ ↓
Result:    Ear | (blank) | 110 | 4 | 250  ← Quantity added (2+2=4)
```

**Part B: Smart Matching**

For each item, the system asks 4 questions:

```
+----------------------------------------------+
| 🔍 Does this item already exist in MyBillBook? |
+----------------------------------------------+
|                                              |
| Question 1: Same category? (Ear Rings)       |
| Question 2: Same cost price? (110)           |
| Question 3: Same selling price? (250)        |
| Question 4: Same name variant? (blank/SL/GL) |
|                                              |
+----------------------------------------------+
            |
    +-------+--------+
    v                v
+---------+      +---------+
| ALL 4   |      | NOT ALL |
| MATCH!  |      | MATCH   |
|   ✓     |      |    ✗    |
+---------+      +---------+
    |                |
    v                v
EXISTING         NEW ITEM
 ITEM

Use old name     Create new name
& barcode        & barcode

Example:         Example:
"Ear Rings XCNR" "Ear Rings HXXL"
84 0110          24 0118
```

**Result:**
```
    📊 "Inventory" Sheet (Final Organized List)

    71 total items:
    ├─ 2 items marked "Yes" (already in MyBillBook)
    └─ 69 items marked "No" (new items to add)

    New Columns Added:
    • Column I: "Already Present" = Yes/No
    • Column J: "Inventory Item Barcode" = Actual barcode to use
```

---

### STEP 2: Create Import Files

**What happens:** The system creates 2 separate files for MyBillBook

```
    📊 Inventory Sheet (71 items)
         |
         | The system reads Column I ("Already Present")
         |
    +----+----+
    v         v
+--------+  +--------+
|Column I|  |Column I|
|= "Yes" |  |= "No"  |
+--------+  +--------+
    |         |
    v         v
+==========+  +==========+
| UPDATE   |  |   ADD    |
|  SHEET   |  |  SHEET   |
+==========+  +==========+
| 2 items  |  | 69 items |
|          |  |          |
| These    |  | These    |
| already  |  | are NEW  |
| exist in |  | items to |
| MyBill   |  | add      |
| Book     |  |          |
+==========+  +==========+
```

**Real Example:**

**UPDATE Sheet** (2 items):
```
+-----------------+----------+--------+-------+
| Name            | Category | Barcode| Price |
+-----------------+----------+--------+-------+
| Ear Rings XCNR  | Ear Rings| 84 0110| 250   | <- Already exists
| Bracelets R AXPZ| Bracelets| 78 0611| 250   | <- Already exists
+-----------------+----------+--------+-------+
```

**ADD Sheet** (69 items):
```
+-----------------+----------+--------+-------+
| Name            | Category | Barcode| Price |
+-----------------+----------+--------+-------+
| Ear Rings HXXL  | Ear Rings| 24 0118| 250   | <- New item
| Ear Rings GL... | Ear Rings| 67 5432| 199   | <- New item
| ... (67 more)   |          |        |       |
+-----------------+----------+--------+-------+
```

**What You Do Next:**
1. Download both sheets as CSV files
2. Go to MyBillBook website
3. Upload "ADD" sheet → Add 69 new products
4. Upload "UPDATE" sheet → Update 2 existing products

---

### STEP 3: Create Printable Labels

**What happens:** The system creates one row per label

```
    📊 Inventory Sheet (71 items)
         │
         │ Each item has a quantity
         │
         ▼
    🏷️ WePrint Sheet

    One row = One physical label

    Example:
    Item "Ear Rings XCNR" has Qty = 4
         ↓
    Creates 4 identical label rows:

    Row 1: Ear Rings XCNR | 84 0110 | 250.00
    Row 2: Ear Rings XCNR | 84 0110 | 250.00
    Row 3: Ear Rings XCNR | 84 0110 | 250.00
    Row 4: Ear Rings XCNR | 84 0110 | 250.00

    Total: 299 labels ready to print
```

**What You Do Next:**
1. Download WePrint sheet as CSV/Excel
2. Import to your label printer software
3. Print all labels at once

---

## 🎨 Visual Summary

```
+-------------------------------------------------------------+
|                     START TO FINISH                         |
+-------------------------------------------------------------+

📝 Manual Entry           🌐 Download MyBillBook
   (78 rows)      +          (352 items)
       |                          |
       +----------+---------------+
                  v
         🔄 STEP 1: Organize
         ---------------------
         • Combines duplicates (78 -> 71)
         • Checks each item
         • Marks as "Yes" or "No"
                  |
        +---------+---------+
        v                   v
    2 items              69 items
   "Already              "New
    Present"              Items"
        |                   |
        +---------+---------+
                  v
         📋 STEP 2: Split Files
         ----------------------
         • UPDATE sheet (2)
         • ADD sheet (69)
                  |
                  v
         🏷️ STEP 3: Labels
         ------------------
         • 299 labels total
         • Ready to print

+-------------------------------------------------------------+
|                       ✅ DONE!                              |
|                                                             |
| • MyBillBook ready to import                                |
| • Labels ready to print                                     |
| • Everything organized                                      |
+-------------------------------------------------------------+
```

---

## 🤔 Simple Q&A

### Q: Why do we need to sync MyBillBook first?
**A:** So the system knows which items you already have. Without this, it would treat everything as new!

### Q: What does "smart matching" mean?
**A:** The system automatically checks if an item already exists in MyBillBook by comparing category, prices, and name. You don't have to manually check!

### Q: What's the difference between ADD and UPDATE sheets?
- **ADD:** Brand new items to add to MyBillBook (69 items)
- **UPDATE:** Items you already have, just updating quantity/price (2 items)

### Q: Why 299 labels when we only have 71 items?
**A:** Because if one item has quantity 4, you need 4 labels! The system automatically duplicates labels based on quantity.

### Q: What if I don't want to print labels?
**A:** No problem! Just skip Step 3. Steps 1 and 2 are still useful for organizing and importing to MyBillBook.

---

## 📊 The Magic Numbers

```
+------------------------------------------+
|         WHAT GOES IN VS OUT              |
+------------------------------------------+
| YOU ENTER:    78 rows (with duplicates)  |
|               v                          |
| SYSTEM GIVES: 71 organized items         |
|               +- 2 existing items        |
|               +- 69 new items            |
|               v                          |
| FINAL OUTPUT: • 2 rows in UPDATE sheet   |
|               • 69 rows in ADD sheet     |
|               • 299 labels to print      |
+------------------------------------------+
```

---

## 🎯 Key Takeaways

1. **You only enter data once** (in "Inventory RAW")
2. **The system does the hard work** (matching, organizing, splitting)
3. **You get 3 ready-to-use outputs**:
   - ✅ UPDATE file for MyBillBook (existing items)
   - ✅ ADD file for MyBillBook (new items)
   - ✅ Label file for printing
4. **Total time: About 20 seconds** ⚡

---

## 💡 Tips for Your Team

✅ **Always run in order:** Step 0 → 1 → 2 → 3

✅ **Menu Option 4 runs everything automatically** (recommended!)

✅ **Check the "Already Present" column** to verify matches

✅ **The barcode in Column J is the REAL barcode** to use everywhere

✅ **Don't edit Inventory sheet manually** - it's auto-generated

---

## 🎬 Quick Start Guide

```
1. Open Google Sheets
2. Enter your data in "Inventory RAW" sheet
3. Run the program (python main.py)
4. Select Option 4: "Run All Operations"
5. Wait 20 seconds ☕
6. Done! ✅

   Download and use:
   • myBillBook add.csv
   • myBillBook update.csv
   • WePrint.csv
```

**That's it! No complicated steps, no manual checking, no errors!** 🎉
