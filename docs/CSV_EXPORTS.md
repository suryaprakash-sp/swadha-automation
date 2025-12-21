# CSV Export Feature

## Overview

The CSV export feature allows you to save timestamped copies of your data at each step of the transformation pipeline. This is useful for:
- **Data backup**: Keep historical records of your inventory data
- **Audit trail**: Track changes over time with timestamped exports
- **External analysis**: Use the CSV files in Excel, databases, or other tools
- **Manual verification**: Review data before importing to MyBillBook

## How It Works

After each transformation completes, the system will prompt you:

```
[EXPORT] <export_type>
   Save as CSV? (y/n):
```

- Type `y` to save the data as CSV
- Type `n` to skip saving

## Folder Structure

All CSV exports are saved in the `csv_exports/` directory with the following structure:

```
csv_exports/
├── inventory_raw/          # Raw input data (before consolidation)
├── inventory/              # Consolidated inventory (Transform 1 output)
├── mybillbook_inventory/   # MyBillBook sync data (all existing items)
├── mybillbook_add/         # New items to add to MyBillBook (Transform 2)
├── mybillbook_update/      # Existing items to update (Transform 2)
└── weprint/                # Label printing data (Transform 3)
```

## File Naming Convention

Files are automatically named with timestamps:

```
<export_type>_YYYYMMDD_HHMMSS.csv
```

**Examples:**
- `inventory_raw_20251221_143022.csv`
- `inventory_20251221_143025.csv`
- `mybillbook_add_20251221_143030.csv`

## Export Types

### 1. inventory_raw
**When**: After Transform 1 (Consolidation)
**Source**: "Inventory RAW" sheet
**Contains**: Your original manual entry data before consolidation
**Columns**: Type, Name, Cost Price, Quantity, Selling Price

**Use case**: Keep a backup of your raw input for reference

---

### 2. inventory
**When**: After Transform 1 (Consolidation)
**Source**: "Inventory" sheet
**Contains**: Consolidated inventory with smart matching results
**Columns**: Type, Name, Cost Price, Quantity, Selling Price, Total CP, Total SP, Barcode, Already Present, Inventory Item Barcode (10 columns)

**Use case**: Review which items were matched vs new, verify consolidation

---

### 3. mybillbook_inventory
**When**: After MyBillBook Sync (Menu Option 0)
**Source**: "myBillBook Inventory" sheet
**Contains**: All items currently in your MyBillBook account
**Columns**: 24 columns including ID, Name, SKU, Category, Prices, Quantities, etc.

**Use case**: Keep a snapshot of your MyBillBook inventory at this moment

---

### 4. mybillbook_add
**When**: After Transform 2 (MyBillBook Import)
**Source**: "myBillBook add" sheet
**Contains**: New items to be imported to MyBillBook
**Columns**: 18 columns formatted for MyBillBook import

**Use case**:
- Import these items to MyBillBook
- Review new items before import
- Keep a record of what was added

---

### 5. mybillbook_update
**When**: After Transform 2 (MyBillBook Import)
**Source**: "myBillBook update" sheet
**Contains**: Existing items with updated quantities/prices
**Columns**: 14 columns formatted for MyBillBook update

**Use case**:
- Update existing items in MyBillBook
- Review changes before updating
- Track quantity/price changes over time

---

### 6. weprint
**When**: After Transform 3 (WePrint Export)
**Source**: "WePrint" sheet
**Contains**: Label data with duplicates based on quantity
**Columns**: Product, Barcode, Price

**Use case**:
- Import to label printer software
- Print labels for your inventory
- Manual label creation

## Example Workflow

```
Step 0: Sync MyBillBook
   -> [EXPORT] mybillbook_inventory (Save? y/n)
   -> Creates: mybillbook_inventory_20251221_140000.csv

Step 1: Transform 1 (Consolidation)
   -> [EXPORT] inventory_raw (Save? y/n)
   -> Creates: inventory_raw_20251221_140100.csv
   -> [EXPORT] inventory (Save? y/n)
   -> Creates: inventory_20251221_140101.csv

Step 2: Transform 2 (MyBillBook Import)
   -> [EXPORT] mybillbook_add (Save? y/n)
   -> Creates: mybillbook_add_20251221_140200.csv
   -> [EXPORT] mybillbook_update (Save? y/n)
   -> Creates: mybillbook_update_20251221_140201.csv

Step 3: Transform 3 (WePrint)
   -> [EXPORT] weprint (Save? y/n)
   -> Creates: weprint_20251221_140300.csv
```

## Tips

1. **Always save exports before importing to MyBillBook** - This gives you a backup in case something goes wrong

2. **Use timestamps to track changes** - Compare exports from different times to see what changed

3. **Skip exports during testing** - Save time by saying 'n' when you're just testing the transformations

4. **Clean up old exports periodically** - The exports are not automatically deleted, so clean them up manually when needed

5. **Don't commit exports to git** - The `csv_exports/` folder is already in `.gitignore` to prevent accidentally committing sensitive data

## File Format

All CSV files are:
- UTF-8 encoded
- Comma-separated values
- Compatible with Excel, Google Sheets, and other tools
- Include headers in the first row

## Accessing Exports

### View in Excel/Google Sheets
Simply open the CSV files in Excel or import them to Google Sheets

### Use in Python/Pandas
```python
import pandas as pd

# Read any export
df = pd.read_csv('csv_exports/inventory/inventory_20251221_140101.csv')
print(df.head())
```

### Import to Database
Use the CSV files to import data into PostgreSQL, MySQL, or other databases for analysis

## Troubleshooting

### Export prompt not appearing
- Make sure you're running the latest version of the code
- Check that the transformation completed successfully

### Files not being created
- Check folder permissions
- Make sure you typed 'y' when prompted
- Look for error messages during export

### Files in wrong location
- All exports should be in `csv_exports/<subfolder>/`
- If they're elsewhere, check your working directory

### Encoding issues
- All files are UTF-8 encoded
- If characters look wrong, ensure your tool supports UTF-8

## Security Note

**Important**: CSV exports may contain sensitive business data (prices, quantities, etc.)

- The `csv_exports/` folder is excluded from git
- Do not share these files publicly
- Store them securely
- Delete old exports when no longer needed
