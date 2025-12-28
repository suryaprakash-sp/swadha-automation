# Swadha Automation

Data cleaning and transformation pipeline for inventory management using Google Sheets.

## Overview

This project automates inventory data transformations for multiple use cases:

1. **Transform 1**: Consolidate inventory with smart matching
2. **Transform 2**: MyBillBook format (inventory management)

**Standalone Tools:**
- **Inventory Sync** (`scripts/mybillbook/sync_inventory.py`): Standalone MyBillBook inventory sync
- **Label Generator** (`scripts/generate_labels.py`): Generate WePrint labels from MyBillBook inventory

## 📖 Documentation

- **[Web UI Guide](docs/WEB_UI_GUIDE.md)** - Browser-based interface guide (recommended for new users!)
- **[Simple Workflow Guide](docs/SIMPLE_WORKFLOW.md)** - Easy-to-understand guide for everyone
- **[Detailed Workflow Diagram](docs/WORKFLOW_DIAGRAM.md)** - Technical workflow with visual diagrams
- **[CSV Exports Guide](docs/CSV_EXPORTS.md)** - How to save timestamped backups of your data
- **[MyBillBook Setup](docs/MYBILLBOOK_SETUP.md)** - How to configure MyBillBook API
- **[Transform 1 Guide](docs/TRANSFORM1_CONSOLIDATE.md)** - Smart matching and consolidation
- **[Transform 2 Guide](docs/TRANSFORM2_MYBILLBOOK.md)** - MyBillBook import files

## Workflow

### Main Pipeline

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
✅ Import to MyBillBook
```

### Standalone Scripts

**Inventory Sync:**
```
Run: python scripts/mybillbook/sync_inventory.py

Fetches from MyBillBook API → Writes to Google Sheets
```

**Label Generator:**
```
Run: python scripts/generate_labels.py

Reads: MyBillBook Inventory (synced data)
    ↓
Select items for labels (by number, search, or all)
    ↓
Enter label count for each item
    ↓
Generates: WePrint sheet with label rows
    ↓
Export to CSV → Print labels
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
   python scripts/main.py
   ```
   Or use the web UI:
   ```cmd
   streamlit run scripts/app.py
   ```

5. On first run, a browser will open for authentication
6. Sign in with your Google account and grant permissions
7. A `token.json` will be created for future runs (no need to login again)

## Usage

### Option 1: Web UI (Recommended)

Launch the modern web interface:

```cmd
streamlit run scripts/app.py
```

The web interface will open in your browser with:
- Visual progress indicators
- Interactive label generator
- CSV download buttons
- One-click operations

See **[Web UI Guide](docs/WEB_UI_GUIDE.md)** for detailed instructions.

### Option 2: Command Line

Run the CLI script and follow the interactive menu:

```cmd
python scripts/main.py
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
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── SETUP.md                            # Google Sheets setup instructions
├── .env.example                        # MyBillBook credentials template
├── scripts/                            # ⭐ Main executable scripts
│   ├── mybillbook/                     # MyBillBook-related scripts
│   │   ├── sync_inventory.py           # Inventory sync
│   │   └── README.md
│   ├── README.md                       # Scripts documentation
│   ├── main.py                         # CLI interactive menu
│   ├── app.py                          # Streamlit web UI
│   └── generate_labels.py              # Standalone label generator
├── docs/
│   ├── WEB_UI_GUIDE.md                 # Web UI usage guide
│   ├── SIMPLE_WORKFLOW.md              # Easy workflow guide
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
├── utils/
│   ├── sheets.py                       # Google Sheets API wrapper
│   └── csv_exporter.py                 # CSV export utilities
└── csv_exports/                        # CSV export files (timestamped)
    ├── mybillbook_inventory/           # MyBillBook inventory exports
    ├── mybillbook_add/                 # ADD items exports
    ├── mybillbook_update/              # UPDATE items exports
    └── weprint/                        # WePrint label exports
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
