# Transform 1: Consolidate Inventory

## Overview

Transform 1 consolidates raw inventory data by grouping duplicate items and summing their quantities. It generates unique names and barcodes for each consolidated item, and calculates total cost and selling prices.

## Input

**Source Sheet**: `Inventory RAW`

**Input Columns** (5 columns):
- **A**: Type (e.g., "Traditional Ear Rings")
- **B**: Name (e.g., "GL", "SL")
- **C**: Per Item (Cost Price) - numeric
- **D**: Quantity - numeric
- **E**: Per Item (Selling Price) - numeric

**Sample Input**:
```
Type                    Name    Cost    Qty    Sell
Traditional Ear Rings   GL      45      2      199
Traditional Ear Rings   SL      45      2      199
Traditional Ear Rings   SL      70      2      250
```

## Output

**Target Sheet**: `Inventory`

**Output Columns** (8 columns):
- **A**: Type - text
- **B**: Name - text (generated: "Type + Original Name + 4 random letters")
- **C**: Per Item (Cost Price) - number with 2 decimals
- **D**: Quantity - number with 0 decimals
- **E**: Per Item (Selling Price) - number with 2 decimals
- **F**: Total Cost Price - number with 2 decimals (formula: =C*D)
- **G**: Total Selling Price - number with 2 decimals (formula: =D*E)
- **H**: Barcode - text (generated from cost price)

**Sample Output**:
```
Type                    Name                                Cost    Qty    Sell    Total CP    Total SP    Barcode
Traditional Ear Rings   Traditional Ear Rings GL ABCD      45.00   2      199.00  90.00       398.00      45 5432
Traditional Ear Rings   Traditional Ear Rings SL EFGH      45.00   2      199.00  90.00       398.00      67 5498
Traditional Ear Rings   Traditional Ear Rings SL IJKL      70.00   2      250.00  140.00      500.00      32 0789
```

## Processing Logic

### 1. Consolidation

**Consolidation Key**: `Type | Name | Cost Price | Selling Price`

Items are grouped by this key. If multiple rows have the same key, their quantities are summed.

**Example**:
```
Input:
  Row 1: Traditional Ear Rings | GL | 45 | 2 | 199
  Row 2: Traditional Ear Rings | GL | 45 | 3 | 199

Output:
  Traditional Ear Rings | GL | 45 | 5 | 199  (quantity: 2+3=5)
```

### 2. Name Generation

Generated names follow the pattern: `Type + Original Name + 4 Random Letters`

**Logic**:
- If original Name exists: `Type + Name + XXXX`
  - Example: `Traditional Ear Rings GL ABCD`
- If original Name is empty: `Type + XXXX`
  - Example: `Traditional Ear Rings EFGH`

**Random Letters**: 4 uppercase letters (A-Z)

### 3. Barcode Generation

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
- Cost Price: 120 → Barcode: `89 0218` (reversed: 021, padded: 0218)
- Cost Price: 1500 → Barcode: `45 0051` (reversed: 0051)

### 4. Formulas

**Column F (Total Cost Price)**: `=C*D`
- Multiplies Per Item Cost Price by Quantity

**Column G (Total Selling Price)**: `=D*E`
- Multiplies Quantity by Per Item Selling Price

### 5. Column Formatting

All columns are automatically formatted:

| Column | Format | Pattern | Example |
|--------|--------|---------|---------|
| A (Type) | Text | - | Traditional Ear Rings |
| B (Name) | Text | - | Traditional Ear Rings GL ABCD |
| C (Per Item CP) | Number | #,##0.00 | 45.00 |
| D (Quantity) | Number | #,##0 | 2 |
| E (Per Item SP) | Number | #,##0.00 | 199.00 |
| F (Total CP) | Number | #,##0.00 | 90.00 |
| G (Total SP) | Number | #,##0.00 | 398.00 |
| H (Barcode) | Text | - | 67 5432 |

## Usage

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
Processing 76 rows from RAW sheet...
Consolidated into 69 unique items
Sheet Inventory cleared
353 cells updated in Inventory
69 formula cells updated in Inventory
69 formula cells updated in Inventory
69 cells updated in Inventory
Formatted A2:A70 in Inventory as text
Formatted B2:B70 in Inventory as text
Formatted H2:H70 in Inventory as text
Formatted C2:C70 in Inventory as number with 2 decimals
Formatted D2:D70 in Inventory as number with 0 decimals
Formatted E2:E70 in Inventory as number with 2 decimals
Formatted F2:F70 in Inventory as number with 2 decimals
Formatted G2:G70 in Inventory as number with 2 decimals
[OK] Inventory consolidated successfully! 69 items processed
```

## Technical Details

### Functions

**`generate_name(category)`**
- Generates name without existing name: `Category + 4 random letters`

**`generate_name_with_existing(category, existing_name)`**
- Generates name with existing name: `Category + Existing + 4 random letters`

**`generate_barcode(cost_price)`**
- Generates unique barcode from cost price

**`consolidate_inventory(sheets_manager)`**
- Main consolidation function

### Dependencies

- `utils.sheets.SheetsManager` - Google Sheets API wrapper
- `config.SHEET_RAW` - Raw sheet name
- `config.SHEET_INVENTORY` - Output sheet name

### Data Flow

```
Read RAW sheet
    ↓
Parse rows (A-E columns)
    ↓
Group by consolidation key
    ↓
Sum quantities for duplicates
    ↓
Generate names and barcodes
    ↓
Write data (A-E) + headers (F-H)
    ↓
Write formulas (F, G)
    ↓
Write barcodes (H)
    ↓
Apply formatting (all columns)
    ↓
Complete
```

## Error Handling

- Missing RAW sheet: Error message displayed
- Empty data: Skips processing
- Missing columns: Auto-filled with empty strings
- Invalid numbers: Treated as 0

## Performance

- **Typical Processing Time**: 5-10 seconds for 100 rows
- **API Calls**: ~8 calls per run
  - 1 read (RAW sheet)
  - 1 clear (Inventory sheet)
  - 1 write (main data)
  - 2 write (formulas F, G)
  - 1 write (barcodes H)
  - 8 format (A, B, C, D, E, F, G, H)

## Notes

- Consolidation reduces 76 input rows to ~69 output rows (typical)
- Random elements (names, barcodes) change each run
- Formulas are live - updating C, D, or E will update F and G automatically
- All formatting is preserved when copying data
