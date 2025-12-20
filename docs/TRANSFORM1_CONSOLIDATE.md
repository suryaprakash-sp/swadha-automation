# Transform 1: Consolidate Inventory

## Overview

Transform 1 consolidates raw inventory data by grouping duplicate items and summing their quantities. It **now includes smart MyBillBook matching** to identify which items already exist in MyBillBook and which are new. For matched items, it uses the existing MyBillBook name and barcode; for new items, it generates unique names and barcodes.

## Input

### Primary Source: `Inventory RAW`

**Input Columns** (5 columns):
- **A**: Type (e.g., "Traditional Ear Rings", "Ear Rings")
- **B**: Name (e.g., "GL", "SL", or empty)
- **C**: Per Item (Cost Price) - numeric
- **D**: Quantity - numeric
- **E**: Per Item (Selling Price) - numeric

**Sample Input**:
```
Type                    Name    Cost    Qty    Sell
Traditional Ear Rings   GL      45      2      199
Ear Rings                       110     4      250
Bracelets               R       110     5      250
```

### Secondary Source: `myBillBook Inventory`

Used for matching existing items. See [MyBillBook Setup](MYBILLBOOK_SETUP.md) for sync instructions.

**Important**: Run **Menu Option 0 (Sync MyBillBook Inventory)** before Transform 1 to get latest matching data.

## Output

**Target Sheet**: `Inventory`

**Output Columns** (10 columns):
- **A**: Type - text
- **B**: Name - text (MyBillBook name if matched, or generated name)
- **C**: Per Item (Cost Price) - number with 2 decimals
- **D**: Quantity - number with 0 decimals
- **E**: Per Item (Selling Price) - number with 2 decimals
- **F**: Total Cost Price - number with 2 decimals (formula: =C*D)
- **G**: Total Selling Price - number with 2 decimals (formula: =D*E)
- **H**: Barcode - text (generated for reference)
- **I**: Already Present - text ("Yes" or "No")
- **J**: Inventory Item Barcode - text (actual barcode: MyBillBook SKU if matched, generated if new)

**Sample Output**:
```
Type          Name              Cost    Qty  Sell    Total CP  Total SP  Barcode    Already  Inventory Item
                                                                                     Present  Barcode
Ear Rings     Ear Rings XCNR    110.00  4    250.00  440.00    1,000.00  24 0118    Yes      84 0110
Bracelets     Bracelets R AXPZ  110.00  5    250.00  550.00    1,250.00  49 0119    Yes      78 0611
Ear Rings     Ear Rings HXXL    110.00  4    250.00  440.00    1,000.00  24 0118    No       24 0118
```

## Processing Logic

### 1. Load MyBillBook Inventory

**First step**: Read synced MyBillBook inventory (352 items)

This provides the reference data for matching existing items.

### 2. Consolidation

**Consolidation Key**: `Type | Name | Cost Price | Selling Price`

Items are grouped by this key. If multiple rows have the same key, their quantities are summed.

**Example**:
```
Input:
  Row 1: Ear Rings |  | 110 | 2 | 250
  Row 2: Ear Rings |  | 110 | 2 | 250

Output:
  Ear Rings |  | 110 | 4 | 250  (quantity: 2+2=4)
```

### 3. Smart MyBillBook Matching

For each consolidated item, check if it exists in MyBillBook by matching **all 4 criteria**:

#### Matching Criteria

1. ✅ **Category** (Type) matches
2. ✅ **Purchase Price** (Cost Price) matches
3. ✅ **Selling Price** matches
4. ✅ **Name variant** matches

#### Name Variant Matching

MyBillBook names follow the pattern: `[Category] [Variant] [4 CHARS]`

**Algorithm**:
1. Remove category from MyBillBook name
2. Remove last 4 characters (random code)
3. Compare remaining variant with RAW name

**Examples**:

| MyBillBook Name | Category | Variant Extracted | RAW Name | Match? |
|----------------|----------|-------------------|----------|---------|
| Ear Rings XCNR | Ear Rings | "" (empty) | "" (empty) | ✅ Yes |
| Ear Rings SL ABCD | Ear Rings | SL | SL | ✅ Yes |
| Bracelets R AXPZ | Bracelets | R | R | ✅ Yes |
| Traditional Ear Rings GL PWAW | Traditional Ear Rings | GL | GL | ✅ Yes |
| Ear Rings XCNR | Ear Rings | "" (empty) | SL | ❌ No |

### 4. Item Processing

#### If MATCH Found (Already Present = Yes)

- **Name**: Use existing MyBillBook name
  - Example: "Ear Rings XCNR"
- **Barcode (Column H)**: Generate new barcode (for reference only)
- **Already Present (Column I)**: "Yes"
- **Inventory Item Barcode (Column J)**: Use MyBillBook SKU Code
  - Example: "84 0110"

#### If NO Match (Already Present = No)

- **Name**: Generate new name
  - Pattern: `Type + Original Name + 4 Random Letters`
  - Example: "Ear Rings HXXL"
- **Barcode (Column H)**: Generate new barcode
- **Already Present (Column I)**: "No"
- **Inventory Item Barcode (Column J)**: Use generated barcode

### 5. Name Generation (for New Items)

Generated names follow the pattern: `Type + Original Name + 4 Random Letters`

**Logic**:
- If original Name exists: `Type + Name + XXXX`
  - Example: `Traditional Ear Rings GL ABCD`
- If original Name is empty: `Type + XXXX`
  - Example: `Ear Rings HXXL`

**Random Letters**: 4 uppercase letters (A-Z)

### 6. Barcode Generation

Barcodes are generated from the cost price with the format: `PP RRRR`

**Format**:
- **PP**: 2-digit prefix (random number between 13-99)
- **RRRR**: 4 digits derived from reversed cost price + random suffix

**Algorithm**:
1. Generate random prefix (13-99)
2. Reverse the cost price digits
3. Pad with random digits to make 4 digits total
4. Combine as: `prefix + space + reversed_price_with_padding`

**Examples**:
- Cost Price: 45 → Barcode: `67 5432` (reversed: 54, padded: 5432)
- Cost Price: 110 → Barcode: `24 0118` (reversed: 011, padded: 0118)
- Cost Price: 1500 → Barcode: `45 0051` (reversed: 0051)

### 7. Formulas

**Column F (Total Cost Price)**: `=C*D`
- Multiplies Per Item Cost Price by Quantity

**Column G (Total Selling Price)**: `=D*E`
- Multiplies Quantity by Per Item Selling Price

### 8. Column Formatting

All columns are automatically formatted:

| Column | Format | Pattern | Example |
|--------|--------|---------|---------|
| A (Type) | Text | - | Ear Rings |
| B (Name) | Text | - | Ear Rings XCNR |
| C (Per Item CP) | Number | #,##0.00 | 110.00 |
| D (Quantity) | Number | #,##0 | 4 |
| E (Per Item SP) | Number | #,##0.00 | 250.00 |
| F (Total CP) | Number | #,##0.00 | 440.00 |
| G (Total SP) | Number | #,##0.00 | 1,000.00 |
| H (Barcode) | Text | - | 24 0118 |
| I (Already Present) | Text | - | Yes |
| J (Inventory Item Barcode) | Text | - | 84 0110 |

## Usage

### Recommended Workflow

**Step 1**: Sync MyBillBook inventory first
```bash
python main.py
# Select option 0: Sync MyBillBook Inventory
```

**Step 2**: Run Transform 1
```bash
# Select option 1: Consolidate Inventory
```

### Via Menu
```bash
python main.py
# Select option 1: Consolidate Inventory
```

### Programmatic
```python
from utils.sheets import SheetsManager
from transforms.transform1_consolidate import consolidate_inventory

sheets = SheetsManager()
consolidate_inventory(sheets)
```

## Output Messages

```
Starting inventory consolidation...
Loaded 352 items from MyBillBook inventory
Processing 78 rows from RAW sheet...
Consolidated into 71 unique items
  MATCH: Ear Rings XCNR (SKU: 84 0110)
  MATCH: Bracelets R AXPZ (SKU: 78 0611)
  Matched with MyBillBook: 2 items
  New items: 69 items
Sheet Inventory cleared
365 cells updated in Inventory
71 formula cells updated in Inventory
71 formula cells updated in Inventory
71 cells updated in Inventory
71 cells updated in Inventory
71 cells updated in Inventory
Formatted A2:A72 in Inventory as text
Formatted B2:B72 in Inventory as text
Formatted H2:H72 in Inventory as text
Formatted I2:I72 in Inventory as text
Formatted J2:J72 in Inventory as text
Formatted C2:C72 in Inventory as number with 2 decimals
Formatted D2:D72 in Inventory as number with 0 decimals
Formatted E2:E72 in Inventory as number with 2 decimals
Formatted F2:F72 in Inventory as number with 2 decimals
Formatted G2:G72 in Inventory as number with 2 decimals
[OK] Inventory consolidated successfully! 71 items processed
```

## Technical Details

### Functions

**`extract_variant_from_mybillbook_name(mybillbook_name, category)`**
- Extracts name variant by removing category prefix and last 4 characters
- Returns variant string (can be empty)

**`safe_float(value)`**
- Safely converts values to float, handling commas and empty values

**`find_matching_mybillbook_item(category, raw_name, cost_price, selling_price, mybillbook_items)`**
- Searches MyBillBook items for match based on 4 criteria
- Returns matched item dict or None

**`generate_name(category)`**
- Generates name without existing name: `Category + 4 random letters`

**`generate_name_with_existing(category, existing_name)`**
- Generates name with existing name: `Category + Existing + 4 random letters`

**`generate_barcode(cost_price)`**
- Generates unique barcode from cost price

**`consolidate_inventory(sheets_manager)`**
- Main consolidation function with MyBillBook matching

### Dependencies

- `utils.sheets.SheetsManager` - Google Sheets API wrapper
- `config.SHEET_RAW` - Raw sheet name
- `config.SHEET_INVENTORY` - Output sheet name
- `config.SHEET_MYBILLBOOK_CURRENT` - MyBillBook synced inventory

### Data Flow

```
Read MyBillBook Inventory (352 items)
    ↓
Read RAW sheet (78 rows)
    ↓
Parse rows (A-E columns)
    ↓
Group by consolidation key
    ↓
Sum quantities for duplicates (71 unique items)
    ↓
For each item:
  ├─ Search MyBillBook for match
  ├─ If MATCH: Use MyBillBook name & SKU
  └─ If NO MATCH: Generate new name & barcode
    ↓
Write data (A-E) + headers (F-J)
    ↓
Write formulas (F, G)
    ↓
Write barcodes (H)
    ↓
Write flags (I)
    ↓
Write inventory barcodes (J)
    ↓
Apply formatting (all columns)
    ↓
Complete
```

## Error Handling

- Missing RAW sheet: Error message displayed
- Missing MyBillBook inventory: Warning displayed, all items treated as new
- Empty data: Skips processing
- Missing columns: Auto-filled with empty strings
- Invalid numbers: Treated as 0
- Price mismatch tolerance: ±0.01 for float comparison

## Performance

- **Typical Processing Time**: 8-12 seconds for 78 rows
- **API Calls**: ~11 calls per run
  - 2 reads (MyBillBook inventory, RAW sheet)
  - 1 clear (Inventory sheet)
  - 1 write (main data)
  - 2 writes (formulas F, G)
  - 3 writes (barcodes H, flags I, inventory barcodes J)
  - 10 formats (A, B, C, D, E, F, G, H, I, J)

## Notes

- **Always sync MyBillBook inventory first** (Menu Option 0) for accurate matching
- Consolidation reduces 78 input rows to ~71 output rows (typical)
- Random elements (names, generated barcodes) change each run
- Matched items keep the same MyBillBook name and SKU across runs
- Formulas are live - updating C, D, or E will update F and G automatically
- All formatting is preserved when copying data
- **Column J (Inventory Item Barcode)** is the actual barcode to use in Transform 2 & 3
