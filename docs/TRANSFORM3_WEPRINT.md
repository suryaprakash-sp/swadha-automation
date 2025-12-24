# Transform 3: WePrint Label Export

## Overview

Transform 3 generates label printing data for WePrint. It reads the consolidated inventory and creates a sheet where **each row represents one label**. Items are duplicated based on their quantity, so if an item has quantity 4, it appears as 4 separate label rows.

## Prerequisites

**MUST run before Transform 3**:
1. **Menu Option 0**: Sync MyBillBook Inventory
2. **Menu Option 1**: Transform 1 (Consolidate Inventory)

Transform 3 reads from the consolidated "Inventory" sheet created by Transform 1.

## Input

**Source Sheet**: `Inventory`

**Input Columns Used**:
- **B**: Name
- **D**: Quantity (determines how many labels to print)
- **E**: Per Item (Selling Price)
- **J**: Inventory Item Barcode (actual barcode for labels)

## Output

**Target Sheet**: `WePrint`

**Output Columns** (3 columns):
- **A**: Product (Item name)
- **B**: Barcode (from Column J - actual barcode)
- **C**: Price (Selling price)

**Sample Output**:
```
Product               Barcode      Price
Ear Rings XCNR        84 0110      250.00
Ear Rings XCNR        84 0110      250.00
Ear Rings XCNR        84 0110      250.00
Ear Rings XCNR        84 0110      250.00
Bracelets R AXPZ      78 0611      250.00
Bracelets R AXPZ      78 0611      250.00
Bracelets R AXPZ      78 0611      250.00
Bracelets R AXPZ      78 0611      250.00
Bracelets R AXPZ      78 0611      250.00
Ear Rings HXXL        24 0118      250.00
Ear Rings HXXL        24 0118      250.00
Ear Rings HXXL        24 0118      250.00
Ear Rings HXXL        24 0118      250.00
```

## Processing Logic

### 1. Read Inventory Data

Reads all consolidated inventory items (71 items)

### 2. Filter Items

Skip items where the product name starts with "Charms 40" (bulk items that don't need individual labels)

**Why?** Some products have very high quantities (1000+) and don't need individual labels printed.

**Example:**
```
Product: Charms 40 XYZ, Quantity: 1000
  ↓
SKIPPED (would generate 1000 labels - not practical)

Product: Ear Rings XCNR, Quantity: 4
  ↓
PROCESSED (generates 4 labels)
```

### 3. Generate Label Rows

For each inventory item (that's not skipped):

```python
quantity = Column D (Quantity)

for i in range(quantity):
    Create label row:
      - Product = Column B (Name)
      - Barcode = Column J (Inventory Item Barcode)
      - Price = Column E (Selling Price)
```

**Example**:
```
Inventory row:
  Name: Ear Rings XCNR
  Quantity: 4
  Price: 250.00
  Barcode: 84 0110

WePrint output (4 rows):
  Ear Rings XCNR | 84 0110 | 250.00
  Ear Rings XCNR | 84 0110 | 250.00
  Ear Rings XCNR | 84 0110 | 250.00
  Ear Rings XCNR | 84 0110 | 250.00
```

### 3. Column Formatting

**Barcode column (B)** formatted as TEXT to preserve format (e.g., "84 0110" with space)

### 4. Label Count Calculation

Total labels = Sum of all quantities from inventory

Example:
- 71 items in inventory
- Various quantities (1, 2, 4, 5, etc.)
- Total: 299 labels generated

## Usage

### Via Menu
```bash
python main.py
# Select option 3: WePrint Export
```

### Programmatic
```python
from utils.sheets import SheetsManager
from transforms.transform3_weprint import export_to_weprint

sheets = SheetsManager()
export_to_weprint(sheets)
```

### Full Pipeline
```bash
python main.py
# Select option 4: Run All Operations
# This runs: Sync → Transform 1 → Transform 2 → Transform 3
```

## Output Messages

```
Starting WePrint export...
Processing 71 inventory items...
  SKIPPED: Charms 40 Silver ABC (Charms 40 - bulk item, quantity: 1000)
  SKIPPED: Charms 40 Gold XYZ (Charms 40 - bulk item, quantity: 500)
Sheet WePrint cleared
900 cells updated in WePrint
Formatted B2:B300 in WePrint as text
[OK] WePrint data exported successfully! 297 labels generated
     2 items skipped (Charms 40 bulk items)
```

## Printing Labels with WePrint

### Step 1: Export to CSV/Excel

**Option A: Download as CSV**
1. Open Google Sheets
2. Go to "WePrint" tab
3. File → Download → Comma Separated Values (.csv)

**Option B: Download as Excel**
1. Go to "WePrint" tab
2. File → Download → Microsoft Excel (.xlsx)

### Step 2: Import to WePrint

1. Open WePrint label printing software
2. Import the CSV/Excel file
3. Map columns:
   - Product → Product name field
   - Barcode → Barcode field
   - Price → Price field
4. Configure label template:
   - Set barcode format (e.g., Code 128)
   - Set label size
   - Position product name, barcode, and price
5. Print labels

## Label Output Examples

### For Matched Items (Already Present = Yes)

**Uses MyBillBook SKU**:
```
Product: Ear Rings XCNR
Barcode: 84 0110  (MyBillBook SKU)
Price: 250.00
```

### For New Items (Already Present = No)

**Uses Generated Barcode**:
```
Product: Ear Rings HXXL
Barcode: 24 0118  (Generated barcode)
Price: 250.00
```

## Technical Details

### Functions

**`export_to_weprint(sheets_manager)`**
- Main export function
- Reads inventory data
- Duplicates rows based on quantity
- Writes WePrint sheet with formatting

### Dependencies

- `utils.sheets.SheetsManager` - Google Sheets API wrapper
- `config.SHEET_INVENTORY` - Consolidated inventory
- `config.SHEET_WEPRINT` - Output sheet name

### Data Flow

```
Read Inventory sheet (71 items)
    ↓
For each item:
  ├─ Get quantity (Column D)
  ├─ Get name (Column B)
  ├─ Get barcode (Column J) ← Uses actual inventory barcode
  ├─ Get price (Column E)
  └─ Create {quantity} label rows
    ↓
Write WePrint sheet (299 label rows)
    ↓
Format Barcode column as TEXT
    ↓
Complete
```

## Error Handling

- Missing Inventory sheet: Error message displayed
- Missing columns: Auto-filled with empty strings
- Invalid quantity: Treated as 0 (no labels generated)
- Missing barcode: Empty string used
- Missing price: 0.00 used

## Performance

- **Typical Processing Time**: 2-4 seconds for 71 items (299 labels)
- **API Calls**: 3 calls per run
  - 1 read (Inventory sheet)
  - 1 clear (WePrint sheet)
  - 1 write (WePrint sheet)
  - 1 format (Barcode column)

## Barcode Formats

### Column J Sources

Transform 3 uses **Column J (Inventory Item Barcode)** which contains:

**For matched items**:
- MyBillBook SKU Code (e.g., "84 0110")
- Format: 2 digits + space + 4 digits

**For new items**:
- Generated barcode (e.g., "24 0118")
- Format: 2 digits + space + 4 digits

Both formats are compatible with standard barcode printers and WePrint software.

## Notes

- **Items starting with "Charms 40" are skipped** to avoid generating thousands of labels
- All other inventory items are processed regardless of "Already Present" status
- Each label row represents ONE physical label to print
- Total label count = sum of quantities (excluding skipped items)
- Barcode column formatted as TEXT to prevent Excel removing leading zeros or spaces
- Uses Column J (Inventory Item Barcode) for the actual barcode to print
- Matched items print with MyBillBook SKU for consistency
- New items print with generated barcode
- Price shown is selling price (not cost price)
- WePrint format is CSV/Excel compatible
- Labels can be sorted/filtered before printing if needed

## Common Use Cases

### Print All Labels
Simply export the entire "WePrint" sheet and import to WePrint

### Print Labels for Specific Items
1. Open "WePrint" sheet in Google Sheets
2. Filter by Product name
3. Download filtered results
4. Import to WePrint

### Print Multiple Copies
Labels are already duplicated based on inventory quantity. If you need more copies:
1. Increase quantity in "Inventory RAW"
2. Re-run Transform 1
3. Re-run Transform 3

### Verify Label Count
Total labels should match sum of quantities in "Inventory" sheet (Column D)
