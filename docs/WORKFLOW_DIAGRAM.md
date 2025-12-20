# Swadha Automation - Complete Workflow Diagram

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SWADHA AUTOMATION PIPELINE                          │
│                                                                             │
│  Manual Entry → Sync API → Smart Match → Split ADD/UPDATE → Generate Labels │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Step-by-Step Flow

```
+===========================================================================+
|                       START: MANUAL DATA ENTRY                            |
+===========================================================================+
                                    |
                                    v
        +-------------------------------------------------------+
        |  Google Sheets: "Inventory RAW"                       |
        |  -------------------------------------------          |
        |  Type  | Name | Cost | Qty | Sell                     |
        |  ------|------|------|-----|------                    |
        |  Ear   |      | 110  |  2  | 250                      |
        |  Ear   |      | 110  |  2  | 250                      |
        |  Ear   | SL   |  45  |  3  | 199                      |
        |  ...                                                  |
        |                                                       |
        |  Total: 78 rows (manual entry)                        |
        +-------------------------------------------------------+
                                    |
                                    v
+===========================================================================+
|                    STEP 0: SYNC MYBILLBOOK INVENTORY                      |
|                         (Menu Option 0)                                   |
+===========================================================================+
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
        +---------------------+       +----------------------------+
        |  MyBillBook API     |       |  Fetch Current Inventory   |
        |  -----------------  |       |  -----------------------   |
        |  • Login with token |       |  • 352 existing items      |
        |  • Company ID       |       |  • 24 columns of data      |
        |  • Bearer auth      |       |  • SKU codes, prices, etc  |
        +---------------------+       +----------------------------+
                                                    |
                                                    v
                        +-------------------------------------------+
                        |  Google Sheets: "myBillBook Inventory"    |
                        |  ---------------------------------------  |
                        |  ID    | Name          | SKU    | Cat ... |
                        |  ------|---------------|--------|-----    |
                        |  e170  | Ear Rings XCNR| 84 0110| Ear...  |
                        |  a234  | Bracelets R...| 78 0611| Bra...  |
                        |  ...                                      |
                        |                                           |
                        |  Total: 352 items synced                  |
                        +-------------------------------------------+
                                                    |
                                                    v
+===========================================================================+
|              STEP 1: TRANSFORM 1 - CONSOLIDATE + SMART MATCH              |
|                         (Menu Option 1)                                   |
+===========================================================================+
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
        +----------------------+       +--------------------------+
        |  Read RAW Sheet      |       |  Read MyBillBook Sync    |
        |  78 rows             |       |  352 items               |
        +----------------------+       +--------------------------+
                    |                               |
                    +---------------+---------------+
                                    v
                        +------------------------+
                        |  CONSOLIDATION         |
                        |  -------------------   |
                        |  Group by:             |
                        |  • Type                |
                        |  • Name                |
                        |  • Cost Price          |
                        |  • Selling Price       |
                        |                        |
                        |  Sum quantities        |
                        |  78 rows -> 71 items   |
                        +------------------------+
                                    |
                                    v
                +-------------------------------------------+
                |  FOR EACH CONSOLIDATED ITEM (71 items)    |
                |  --------------------------------------   |
                |  Check if exists in MyBillBook:           |
                |                                           |
                |  ✓ Category matches?                      |
                |  ✓ Cost Price matches?                    |
                |  ✓ Selling Price matches?                 |
                |  ✓ Name variant matches?                  |
                +-------------------------------------------+
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
        +-----------------------+       +-------------------------+
        |  MATCH FOUND! ✓       |       |  NO MATCH FOUND ✗       |
        |  (2 items)            |       |  (69 items)             |
        |  -----------------    |       |  ------------------     |
        |                       |       |                         |
        |  Use existing:        |       |  Generate new:          |
        |  • MyBillBook name    |       |  • Type + Name + XXXX   |
        |  • MyBillBook SKU     |       |  • Random barcode       |
        |                       |       |                         |
        |  Example:             |       |  Example:               |
        |  "Ear Rings XCNR"     |       |  "Ear Rings HXXL"       |
        |  SKU: 84 0110         |       |  Barcode: 24 0118       |
        |                       |       |                         |
        |  Column I: "Yes"      |       |  Column I: "No"         |
        |  Column J: 84 0110    |       |  Column J: 24 0118      |
        +-----------------------+       +-------------------------+
                    |                               |
                    +---------------+---------------+
                                    v
                +-------------------------------------------------+
                |  Google Sheets: "Inventory" (71 items)          |
                |  ---------------------------------------------- |
                |  Type|Name      |Cost|Qty|Sell|...|Present|SKU  |
                |  ----|----------|----|---|----|---|-------|---  |
                |  Ear |Ear...XCNR|110 | 4 |250 |...| Yes   |84.. | <- Matched
                |  Bra |Bra...AXPZ|110 | 5 |250 |...| Yes   |78.. | <- Matched
                |  Ear |Ear...HXXL|110 | 4 |250 |...| No    |24.. | <- New
                |  Ear |Ear...GL..|45  | 2 |199 |...| No    |67.. | <- New
                |  ...                                            |
                |                                                 |
                |  10 Columns: A-J                                |
                |  Column I: Already Present (Yes/No)             |
                |  Column J: Inventory Item Barcode (actual SKU)  |
                +-------------------------------------------------+
                                    |
                                    v
+===========================================================================+
|             STEP 2: TRANSFORM 2 - MYBILLBOOK ADD/UPDATE                   |
|                         (Menu Option 2)                                   |
+===========================================================================+
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
        +-----------------------+       +-------------------------+
        |  CHECK COLUMN I       |       |  CHECK COLUMN I         |
        |  "Already Present"    |       |  "Already Present"      |
        |                       |       |                         |
        |  IF "Yes" ----------> |       |  IF "No" -------------->|
        +-----------------------+       +-------------------------+
                    |                               |
                    v                               v
    +------------------------------+  +-------------------------------+
    |  UPDATE SHEET                |  |  ADD SHEET                    |
    |  ---------------             |  |  ----------                   |
    |  For existing items (2)      |  |  For new items (69)           |
    |                              |  |                               |
    |  Name | Cat | SKU   | Price  |  |  Name | Cat | SKU   | Price   |
    |  -----|-----|-------|-----   |  |  -----|-----|-------|-----    |
    |  Ear  | Ear |84 0110| 250    |  |  Ear  | Ear |24 0118| 250     |
    |  XCNR |     |       |        |  |  HXXL |     |       |         |
    |  -----|-----|-------|-----   |  |  -----|-----|-------|-----    |
    |  Bra  | Bra |78 0611| 250    |  |  Ear  | Ear |67 5432| 199     |
    |  R    |     |       |        |  |  GL.. |     |       |         |
    |  AXPZ |     |       |        |  |  ...                          |
    |                              |  |                               |
    |  14 columns total            |  |  18 columns total             |
    |  Uses MyBillBook SKU codes   |  |  Uses generated barcodes      |
    +------------------------------+  +-------------------------------+
                    |                               |
                    +---------------+---------------+
                                    v
                        +------------------------+
                        |  DOWNLOAD AS CSV       |
                        |  -----------------     |
                        |  • myBillBook add.csv  |
                        |  • myBillBook update...|
                        +------------------------+
                                    |
                                    v
                        +------------------------+
                        |  IMPORT TO MYBILLBOOK  |
                        |  ------------------    |
                        |  • Add 69 new items    |
                        |  • Update 2 existing   |
                        +------------------------+
                                    |
                                    v
+===========================================================================+
|              STEP 3: TRANSFORM 3 - WEPRINT LABEL EXPORT                   |
|                         (Menu Option 3)                                   |
+===========================================================================+
                                    |
                                    v
                +-----------------------------------------+
                |  READ ALL 71 ITEMS FROM INVENTORY       |
                |  -------------------------------------- |
                |  • Use Column J (actual barcode)        |
                |  • Duplicate by quantity                |
                +-----------------------------------------+
                                    |
                    +---------------+---------------+
                    v                               v
        +-----------------------+       +-------------------------+
        |  MATCHED ITEMS        |       |  NEW ITEMS              |
        |  -------------        |       |  ---------              |
        |  Ear Rings XCNR       |       |  Ear Rings HXXL         |
        |  84 0110 (MyBillBook) |       |  24 0118 (Generated)    |
        |  250.00               |       |  250.00                 |
        |                       |       |                         |
        |  Qty: 4               |       |  Qty: 4                 |
        |  -> 4 label rows      |       |  -> 4 label rows        |
        +-----------------------+       +-------------------------+
                    |                               |
                    +---------------+---------------+
                                    v
                +-----------------------------------------+
                |  Google Sheets: "WePrint"               |
                |  -------------------------------------- |
                |  Product         | Barcode  | Price     |
                |  ----------------|----------|-----      |
                |  Ear Rings XCNR  | 84 0110  | 250.00    | <- Label 1
                |  Ear Rings XCNR  | 84 0110  | 250.00    | <- Label 2
                |  Ear Rings XCNR  | 84 0110  | 250.00    | <- Label 3
                |  Ear Rings XCNR  | 84 0110  | 250.00    | <- Label 4
                |  Bracelets R AXPZ| 78 0611  | 250.00    | <- Label 1
                |  Bracelets R AXPZ| 78 0611  | 250.00    | <- Label 2
                |  ...                                    |
                |  Ear Rings HXXL  | 24 0118  | 250.00    |
                |  Ear Rings HXXL  | 24 0118  | 250.00    |
                |  ...                                    |
                |                                         |
                |  Total: 299 label rows                  |
                +-----------------------------------------+
                                    |
                                    v
                        +------------------------+
                        |  DOWNLOAD & PRINT      |
                        |  -----------------     |
                        |  • Export as CSV/Excel |
                        |  • Import to WePrint   |
                        |  • Print 299 labels    |
                        +------------------------+
                                    |
                                    v
+===========================================================================+
|                              COMPLETE! ✓                                  |
|                                                                           |
|  ✓ MyBillBook updated (69 new + 2 updated)                                |
|  ✓ Labels ready to print (299 labels)                                     |
|  ✓ Inventory consolidated and tracked                                     |
+===========================================================================+
```

## Key Decision Points

### 🔍 Smart Matching (Transform 1)

```
For each RAW item, check MyBillBook inventory:

+---------------------------------------------+
|  MATCHING CRITERIA (ALL 4 MUST MATCH)       |
+---------------------------------------------+
|  1. Category (Type)          ✓              |
|  2. Purchase Price (Cost)    ✓              |
|  3. Selling Price            ✓              |
|  4. Name Variant             ✓              |
+---------------------------------------------+
            |
    +-------+-------+
    |               |
    v               v
 +-----+         +-----+
 |MATCH|         | NEW |
 | Yes |         | No  |
 +-----+         +-----+
    |               |
    v               v
Use existing   Generate new
MyBillBook      name & code
name & SKU
```

### 📊 ADD vs UPDATE (Transform 2)

```
Read Column I from Inventory:

+------------------+
| Already Present? |
+------------------+
        |
    +---+---+
    v       v
  "Yes"    "No"
    |       |
    v       v
+------+ +-----+
|UPDATE| | ADD |
|Sheet | |Sheet|
+------+ +-----+
 2 items  69 items
```

## Summary Statistics

```
+--------------------------------------------------------+
|                    PIPELINE SUMMARY                    |
+--------------------------------------------------------+
|  Input (RAW):              78 rows                     |
|  MyBillBook Sync:          352 items                   |
|  Consolidated:             71 unique items             |
|    +- Matched:             2 items (existing)          |
|    +- New:                 69 items (to add)           |
|  Output Sheets:            4 sheets                    |
|    +- Inventory            71 items (10 columns)       |
|    +- myBillBook add       69 items (18 columns)       |
|    +- myBillBook update    2 items (14 columns)        |
|    +- WePrint              299 labels (3 columns)      |
|  Total Processing Time:    ~15-20 seconds              |
+--------------------------------------------------------+
```

## Quick Reference: Column Usage

```
+---------------------------------------------------------------------+
|  COLUMN I: "Already Present"                                        |
|  ----------------------------                                       |
|  • Set by Transform 1 during matching                               |
|  • "Yes" = Item exists in MyBillBook                                |
|  • "No" = New item, not in MyBillBook                               |
|  • Used by Transform 2 to split ADD/UPDATE                          |
+---------------------------------------------------------------------+

+---------------------------------------------------------------------+
|  COLUMN J: "Inventory Item Barcode"                                 |
|  ----------------------------                                       |
|  • Set by Transform 1 (MyBillBook SKU or generated barcode)         |
|  • MyBillBook SKU if matched (e.g., "84 0110")                      |
|  • Generated barcode if new (e.g., "24 0118")                       |
|  • Used by Transform 2 for Item code                                |
|  • Used by Transform 3 for label barcodes                           |
|  • THIS IS THE ACTUAL BARCODE TO USE EVERYWHERE                     |
+---------------------------------------------------------------------+
```
