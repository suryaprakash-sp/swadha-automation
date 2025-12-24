# Transform 2: MyBillBook Data Import

## Overview

Transform 2 generates import-ready data files for MyBillBook in CSV format. It reads the consolidated inventory (from Transform 1) and creates two separate sheets: one for **new items to ADD** and one for **existing items to UPDATE**.

## Prerequisites

**MUST run before Transform 2**:
1. **Menu Option 0**: Sync MyBillBook Inventory
2. **Menu Option 1**: Transform 1 (Consolidate Inventory)

Transform 2 relies on Column I ("Already Present") from Transform 1 to determine which items go to ADD vs UPDATE.

## Input

**Source Sheet**: `Inventory`

**Input Columns** (10 columns from Transform 1):
- **A**: Type
- **B**: Name
- **C**: Per Item (Cost Price)
- **D**: Quantity
- **E**: Per Item (Selling Price)
- **F**: Total Cost Price
- **G**: Total Selling Price
- **H**: Barcode (generated reference)
- **I**: Already Present (Yes/No) ← **KEY COLUMN**
- **J**: Inventory Item Barcode ← **ACTUAL BARCODE TO USE**

## Output

### ADD Sheet: `myBillBook add`

For items where **Already Present = No** (new items)

**Columns** (18 columns):
1. Item Name* (mandatory field)
2. Description
3. Category
4. Unit
5. Alternate Unit
6. Conversion Rate
7. Item code (Barcode)
8. HSN Code
9. GST Tax Rate(%)
10. Sales Price
11. Sales Tax inclusive
12. Purchase Price
13. Purchase Tax inclusive
14. MRP
15. Current stock
16. Low stock alert quantity
17. Item type
18. Visible on Online Store?

**Sample Output**:
```
Item Name                  Description  Category     Unit    ...  Item code  Sales Price  Current stock
Ear Rings HXXL                         Ear Rings    PIECES  ...  24 0118    250.00       4
Traditional Ear Rings GL PWQZ          Traditional         ...  89 5423    199.00       2
```

### UPDATE Sheet: `myBillBook update`

For items where **Already Present = Yes** (existing items)

**Columns** (14 columns):
1. Item Name* (mandatory field)
2. Description
3. Category
4. Item code (Barcode)
5. HSN Code
6. GST Tax Rate(%)
7. Sales Price
8. Sales Tax inclusive
9. Purchase Price
10. Purchase Tax inclusive
11. MRP
12. Current stock
13. Low stock alert quantity
14. Visible on Online Store?

**Sample Output**:
```
Item Name          Description  Category     Item code  Sales Price  Current stock
Ear Rings XCNR                 Ear Rings    84 0110    250.00       4
Bracelets R AXPZ               Bracelets    78 0611    250.00       5
```

## Processing Logic

### 1. Read Inventory Data

Reads all consolidated inventory items (71 items)

### 2. Check "Already Present" Flag

For each inventory item:

```python
if Already Present (Column I) == "Yes":
    → Goes to UPDATE sheet
else:
    → Goes to ADD sheet
```

### 3. ADD Sheet Logic

**For new items** (Already Present = No):

- **Item Name**: Generated name from Transform 1
  - Example: "Ear Rings HXXL"
- **Category**: Type from Column A
- **Unit**: "PIECES" (default)
- **Item code**: Inventory Item Barcode from Column J
- **Sales Price**: Selling Price from Column E
- **Purchase Price**: Cost Price from Column C
- **MRP**: Same as Sales Price
- **Current stock**: Quantity from Column D
- **Sales/Purchase Tax inclusive**: "Inclusive"
- **Item type**: "Product"
- **Visible on Online Store**: "No"

### 4. UPDATE Sheet Logic

**For existing items** (Already Present = Yes):

- **Item Name**: Existing MyBillBook name from Transform 1
  - Example: "Ear Rings XCNR"
- **Category**: Type from Column A
- **Item code**: MyBillBook SKU from Column J
  - Example: "84 0110"
- **Sales Price**: Updated price from Column E
- **Purchase Price**: Updated cost from Column C
- **MRP**: Same as Sales Price
- **Current stock**: Quantity from Column D
  - Note: This represents the NEW quantity (not added to existing)
- **Sales/Purchase Tax inclusive**: "Inclusive"
- **Visible on Online Store**: "No"

### 5. Column Formatting

**ADD sheet**:
- Item code column (G) formatted as TEXT to preserve barcode format
- Sales Price (J), Purchase Price (L), MRP (N) formatted as number with 2 decimals

**UPDATE sheet**:
- Item code column (D) formatted as TEXT to preserve barcode format
- Sales Price (G), Purchase Price (I), MRP (K) formatted as number with 2 decimals

## Usage

### Via Menu
```bash
python main.py
# Select option 2: MyBillBook Data Import
```

### Programmatic
```python
from utils.sheets import SheetsManager
from transforms.transform2_mybillbook import export_to_mybillbook

sheets = SheetsManager()
export_to_mybillbook(sheets)
```

### Full Pipeline
```bash
python main.py
# Select option 4: Run All Operations
# This runs: Sync → Transform 1 → Transform 2 → Transform 3
```

## Output Messages

```
Starting MyBillBook export...
Processing 71 inventory items...
  UPDATE: Ear Rings XCNR (SKU: 84 0110)
  UPDATE: Bracelets R AXPZ (SKU: 78 0611)
Sheet myBillBook add cleared
1260 cells updated in myBillBook add
Formatted G2:G70 in myBillBook add as text
Sheet myBillBook update cleared
42 cells updated in myBillBook update
Formatted D2:D3 in myBillBook update as text

[OK] MyBillBook data exported successfully!
  ADD sheet: 69 items (new items not in MyBillBook)
  UPDATE sheet: 2 items (existing items in MyBillBook)
  Total processed: 71 items
```

## Importing to MyBillBook

### Step 1: Download Sheets as CSV

**For ADD sheet**:
1. Open Google Sheets
2. Go to "myBillBook add" tab
3. File → Download → Comma Separated Values (.csv)

**For UPDATE sheet**:
1. Go to "myBillBook update" tab
2. File → Download → Comma Separated Values (.csv)

### Step 2: Import to MyBillBook

**ADD (New Items)**:
1. Login to MyBillBook at https://mybillbook.in
2. Go to Inventory → Items
3. Click "Bulk Upload" or "Import"
4. Select "Add New Items"
5. Upload `myBillBook add.csv`
6. Map columns if needed (should auto-detect)
7. Click "Import"

**UPDATE (Existing Items)**:
1. Go to Inventory → Items
2. Click "Bulk Upload" or "Import"
3. Select "Update Existing Items"
4. Upload `myBillBook update.csv`
5. Map columns if needed
6. Click "Import"

## Technical Details

### Functions

**`safe_float(value)`**
- Safely converts values to float, handling commas and empty values
- Example: "1,199" → 1199.0

**`export_to_mybillbook(sheets_manager)`**
- Main export function
- Reads inventory data
- Splits items into ADD and UPDATE based on Column I
- Writes both sheets with proper formatting

### Dependencies

- `utils.sheets.SheetsManager` - Google Sheets API wrapper
- `config.SHEET_INVENTORY` - Consolidated inventory
- `config.SHEET_MYBILLBOOK_ADD` - ADD sheet name
- `config.SHEET_MYBILLBOOK_UPDATE` - UPDATE sheet name

### Data Flow

```
Read Inventory sheet (71 items)
    ↓
For each item:
  ├─ Read Column I (Already Present)
  ├─ Read Column J (Inventory Item Barcode)
  ├─ If "Yes" → Prepare UPDATE row
  └─ If "No" → Prepare ADD row
    ↓
Write ADD sheet
    ↓
Format Item code as TEXT (ADD sheet)
    ↓
Write UPDATE sheet
    ↓
Format Item code as TEXT (UPDATE sheet)
    ↓
Complete
```

## Error Handling

- Missing Inventory sheet: Error message displayed
- Missing columns: Auto-filled with empty strings
- Invalid numbers: Treated as 0
- Empty "Already Present" flag: Treated as "No" (goes to ADD)

## Performance

- **Typical Processing Time**: 3-5 seconds for 71 items
- **API Calls**: 6 calls per run
  - 1 read (Inventory sheet)
  - 2 clears (ADD and UPDATE sheets)
  - 2 writes (ADD and UPDATE sheets)
  - 2 formats (Item code columns)

## Notes

- **Always run Transform 1 first** to generate Column I and J
- ADD sheet gets items with generated barcodes
- UPDATE sheet gets items with MyBillBook SKU codes
- Both sheets are MyBillBook CSV import compatible
- Item code (barcode) is formatted as TEXT to prevent Excel auto-formatting
- UPDATE does not add to existing stock - it sets the new stock level
- Default values: Unit="PIECES", Tax="Inclusive", Store Visible="No"
