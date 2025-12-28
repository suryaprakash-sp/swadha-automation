# Scripts Directory

This folder contains all main executable scripts for Swadha Automation.

## Folder Structure

```
scripts/
├── mybillbook/          # MyBillBook-related scripts
│   ├── sync_inventory.py
│   └── README.md
├── main.py              # CLI interactive menu
├── app.py               # Streamlit web UI
└── generate_labels.py   # Label generator
```

## Available Scripts

### MyBillBook Scripts (`mybillbook/`)

See [mybillbook/README.md](mybillbook/README.md) for detailed documentation.

**Quick access:**
- `sync_inventory.py` - Sync MyBillBook inventory to Google Sheets
- `sync_sales_invoices.py` - Sync MyBillBook sales invoices to Google Sheets (with date range options)
- `sync_expenses.py` - Sync MyBillBook expenses to Google Sheets (with date range options)

---

### 1. `main.py`
**CLI Interactive Menu**

Command-line interface with an interactive menu for all operations.

**Usage:**
```bash
python scripts/main.py
```

**Features:**
- 0: Sync MyBillBook Inventory
- 1: Consolidate Inventory (Transform 1)
- 2: MyBillBook Data Import (Transform 2)
- 3: Run All Operations
- 4: Exit

---

### 2. `app.py`
**Streamlit Web UI**

Browser-based web interface for all automation tasks.

**Usage:**
```bash
streamlit run scripts/app.py
```

**Features:**
- Main Operations (Sync, Transform 1 & 2)
- Label Generator
- CSV Exports viewer
- About & System Status

---

### 3. `generate_labels.py`
**Standalone Label Generator**

Generates WePrint labels from MyBillBook inventory.

**Usage:**
```bash
python scripts/generate_labels.py
```

**What it does:**
- Reads MyBillBook inventory
- Lists all items with quantities
- Lets you select items and specify label counts
- Generates labels in WePrint format
- Exports to CSV for printing

---

## Quick Start

1. **First time setup:**
   ```bash
   # Sync inventory from MyBillBook
   python scripts/mybillbook/sync_inventory.py

   # Or sync sales invoices
   python scripts/mybillbook/sync_sales_invoices.py

   # Or sync expenses
   python scripts/mybillbook/sync_expenses.py
   ```

2. **Use interactive CLI:**
   ```bash
   python scripts/main.py
   ```

3. **Or use web interface:**
   ```bash
   streamlit run scripts/app.py
   ```

## Project Structure

```
swadha-automation/
├── scripts/                       # All main executable scripts (THIS FOLDER)
│   ├── mybillbook/               # MyBillBook-related scripts
│   │   ├── sync_inventory.py     # Inventory sync
│   │   ├── sync_sales_invoices.py # Sales invoices sync
│   │   ├── sync_expenses.py      # Expenses sync
│   │   └── README.md
│   ├── main.py                   # CLI interface
│   ├── app.py                    # Web UI (Streamlit)
│   └── generate_labels.py        # Label generator
├── mybillbook/                   # MyBillBook API client library
├── transforms/                   # Data transformation modules
├── utils/                        # Shared utilities
└── config.py                     # Configuration
```
