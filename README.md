# Swadha Automation

Data cleaning and transformation pipeline for inventory management using Google Sheets.

## Overview

This project automates inventory data transformations for multiple use cases:

1. **Transform 1**: Reference transformation (internal use)
2. **Transform 2**: MyBillBook format (inventory management)
3. **Transform 3**: WePrint format (label printing)

## Workflow

```
Google Sheets (Raw Inventory Data)
    ↓
Transform 1 (Reference)
    ↓
Transform 2 (MyBillBook - Inventory Management)
    ↓
Transform 3 (WePrint - Label Printing)
    ↓
Google Sheets (Output)
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
1. Consolidate Inventory (Transform 1)
   - Reads from "Inventory RAW" sheet
   - Consolidates duplicate items (by Type, Name, Cost Price, Selling Price)
   - Generates item names and barcodes
   - Writes to "Inventory" sheet

2. MyBillBook Data Import (Transform 2)
   - Reads from "Inventory RAW" and "Inventory" sheets
   - Creates two sheets: "myBillBook add" and "myBillBook update"
   - ADD: New items to add to MyBillBook
   - UPDATE: Existing items to update in MyBillBook

3. WePrint Export (Transform 3)
   - Reads from "Inventory" sheet
   - Creates "WePrint" sheet with label data
   - Duplicates rows based on quantity (for printing labels)

4. Run All Operations
   - Runs all three transforms in sequence
   - Recommended for complete pipeline execution
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
├── SETUP.md                            # Detailed setup instructions
├── transforms/
│   ├── transform1_consolidate.py       # Transform 1: Consolidate Inventory
│   ├── transform2_mybillbook.py        # Transform 2: MyBillBook export
│   └── transform3_weprint.py           # Transform 3: WePrint export
└── utils/
    └── sheets.py                       # Google Sheets API wrapper
```

## Configuration

Edit `config.py` to change:
- Spreadsheet ID
- Sheet names
- OAuth settings

## License

Private project
