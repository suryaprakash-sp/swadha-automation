# Swadha Automation

Data cleaning and transformation pipeline for inventory management using Google Sheets.

## Overview

This project automates inventory data transformations for multiple use cases:

1. **Transform 1**: Reference transformation (internal use)
2. **Transform 2**: MyBillBook format (inventory management)
3. **Transform 3**: WePrint format (label printing)

## Workflow

```
Step 0: MyBillBook API Sync
    ↓
Google Sheets ("myBillBook Inventory" - 352 items synced)
    ↓
Google Sheets ("Inventory RAW" - Manual Data Entry, 78 rows)
    ↓
Step 1: Transform 1 - Consolidate + Smart Match
    ├─ Consolidates duplicates (78 → 71 items)
    ├─ Matches with MyBillBook inventory (4 criteria)
    ├─ For MATCHED items (2): Uses MyBillBook name & SKU
    └─ For NEW items (69): Generates name & barcode
    ↓
Google Sheets ("Inventory" - 71 items with columns I & J)
    ↓
Step 2: Transform 2 - MyBillBook Import
    ├─ Reads Column I ("Already Present")
    ├─ IF "Yes" → UPDATE sheet (2 items)
    └─ IF "No" → ADD sheet (69 items)
    ↓
Google Sheets ("myBillBook add" + "myBillBook update")
    ↓
Step 3: Transform 3 - WePrint Labels
    ├─ Reads all 71 items
    ├─ Uses Column J (Inventory Item Barcode)
    └─ Duplicates by quantity
    ↓
Google Sheets ("WePrint" - 299 label rows)
```

## Quick Start

### Prerequisites

- Python 3.8+
- Google account with access to the spreadsheet

### Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

3. Set up Google Sheets API access:
   - See **[SETUP.md](SETUP.md)** for detailed step-by-step instructions
   - You'll need to create OAuth credentials from Google Cloud Console
   - Download `credentials.json` and place it in the project root

4. Run the script:
   ```cmd
   python main.py
   ```

5. On first run, a browser will open for authentication
6. Sign in with your Google account and grant permissions
7. A `token.json` will be created for future runs (no need to login again)

## Usage

Run the main script and follow the interactive menu:

```cmd
python main.py
```

### Menu Options

```
0. Sync MyBillBook Inventory (Fetch Latest)
   - Fetches current inventory from MyBillBook API
   - Writes to "myBillBook Inventory" sheet (352 items with 24 columns)
   - REQUIRED before Transform 1 for accurate matching
   - See: docs/MYBILLBOOK_SETUP.md

1. Consolidate Inventory (Transform 1)
   - Reads from "myBillBook Inventory" (352 items) and "Inventory RAW" sheet (78 rows)
   - Smart matching by: Category + Cost Price + Selling Price + Name variant
   - Consolidates duplicate items (78 → 71 unique items)
   - For MATCHED items (2): Uses existing MyBillBook name & SKU
   - For NEW items (69): Generates unique names and barcodes
   - Writes to "Inventory" sheet with 10 columns (A-J):
     * Column I: "Already Present" (Yes/No)
     * Column J: "Inventory Item Barcode" (actual barcode to use)
   - See: docs/TRANSFORM1_CONSOLIDATE.md

2. MyBillBook Data Import (Transform 2)
   - Reads from "Inventory" sheet (71 items)
   - Uses Column I ("Already Present") to determine ADD vs UPDATE
   - Creates two sheets:
     * "myBillBook add": 69 new items with generated barcodes
     * "myBillBook update": 2 existing items with MyBillBook SKU codes
   - CSV import-ready format for MyBillBook
   - See: docs/TRANSFORM2_MYBILLBOOK.md

3. WePrint Export (Transform 3)
   - Reads from "Inventory" sheet (71 items)
   - Uses Column J (Inventory Item Barcode) for labels
   - Creates "WePrint" sheet with 299 label rows
   - Duplicates rows based on quantity (for printing multiple labels)
   - 3 columns: Product, Barcode, Price
   - See: docs/TRANSFORM3_WEPRINT.md

4. Run All Operations
   - Syncs MyBillBook inventory (Step 0)
   - Runs all three transforms in sequence (Steps 1-3)
   - Recommended for complete pipeline execution
   - Total time: ~15-20 seconds
```

## Project Structure

```
swadha-automation/
├── credentials.json                    # Google OAuth credentials (not in git)
├── token.json                          # OAuth token (not in git)
├── config.py                           # Configuration (Sheet ID, names)
├── main.py                             # Main interactive script
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── SETUP.md                            # Google Sheets setup instructions
├── .env.example                        # MyBillBook credentials template
├── docs/
│   ├── TRANSFORM1_CONSOLIDATE.md       # Transform 1 documentation
│   ├── TRANSFORM2_MYBILLBOOK.md        # Transform 2 documentation
│   ├── TRANSFORM3_WEPRINT.md           # Transform 3 documentation
│   └── MYBILLBOOK_SETUP.md             # MyBillBook API setup guide
├── mybillbook/
│   ├── api_client.py                   # MyBillBook API client
│   ├── config.py                       # MyBillBook configuration
│   └── sync.py                         # Inventory sync functionality
├── transforms/
│   ├── transform1_consolidate.py       # Transform 1: Consolidate Inventory
│   ├── transform2_mybillbook.py        # Transform 2: MyBillBook export
│   └── transform3_weprint.py           # Transform 3: WePrint export
└── utils/
    └── sheets.py                       # Google Sheets API wrapper
```

## Configuration

### Google Sheets

Edit `config.py` to change:
- Spreadsheet ID
- Sheet names
- OAuth settings

### MyBillBook API (Optional)

For syncing current MyBillBook inventory:

1. Copy `.env.example` to `.env`
2. Add your MyBillBook credentials
3. See [docs/MYBILLBOOK_SETUP.md](docs/MYBILLBOOK_SETUP.md) for detailed instructions

**Note**: MyBillBook sync is optional. If not configured, Transform 2 will treat all items as new (ADD).

## License

Private project
