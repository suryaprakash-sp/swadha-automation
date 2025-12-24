# Web UI Guide

## Overview

The Swadha Automation Web UI provides a modern, browser-based interface for managing inventory automation tasks. Built with Streamlit, it offers an intuitive alternative to the command-line interface.

## Features

- **Main Operations** - Run sync and transformations with visual feedback
- **Label Generator** - Interactive label creation with search and filtering
- **CSV Exports** - Browse, preview, and download exported data
- **About** - System status and documentation links

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Sheets API credentials (`credentials.json`)
- MyBillBook API credentials (optional, for sync feature)

### Install Dependencies

```cmd
pip install -r requirements.txt
```

This will install all required packages including:
- `streamlit==1.29.0` - Web UI framework
- `pandas==2.1.4` - Data manipulation
- Other existing dependencies (Google API, requests, etc.)

## Running the Web UI

### Start the Application

```cmd
streamlit run app.py
```

The web interface will automatically open in your default browser at:
```
http://localhost:8501
```

### First-Time Setup

1. **Google Sheets Authentication**:
   - On first run, the app will attempt to connect to Google Sheets
   - If `token.json` doesn't exist, a browser window will open for authentication
   - Sign in with your Google account and grant permissions
   - The connection will be saved for future sessions

2. **Navigation**:
   - Use the sidebar to navigate between pages
   - Connection status is displayed in the sidebar

## Pages

### 1. 🏠 Main Operations

Execute the core automation pipeline with visual progress indicators.

**Settings:**

A checkbox in the sidebar allows you to control CSV export behavior:
- **Auto-export to CSV** (checked by default): Automatically exports all data to CSV files after transformations without prompting
- When unchecked: The operations will still complete but won't create CSV exports

**Available Operations:**

#### Step 0: Sync MyBillBook
- **Purpose**: Fetch latest inventory from MyBillBook API
- **Output**: Updates "myBillBook Inventory" sheet
- **Details**: Click "View Details" expander to see sync logs
- **Safety**: Automatic backup created before clearing old data

#### Step 1: Consolidate Inventory
- **Purpose**: Smart matching and consolidation of raw inventory
- **Input**: Reads from "Inventory RAW" and "myBillBook Inventory"
- **Output**: Writes to "Inventory" sheet with match status
- **Details**: Shows consolidation statistics and matching results

#### Step 2: MyBillBook Export
- **Purpose**: Generate ADD/UPDATE sheets for MyBillBook import
- **Input**: Reads from "Inventory" sheet
- **Output**: Creates "myBillBook add" and "myBillBook update" sheets
- **Details**: Shows item counts and CSV export options

#### Run All Operations
- **Purpose**: Execute all three steps in sequence
- **Progress**: Visual progress bar with step-by-step status
- **Clean Interface**: Individual operation buttons are hidden during execution to prevent duplicate runs
- **Success**: Celebration animation on completion
- **Back Button**: After completion or error, click "Back to Operations" to return to the main view
- **Error Handling**: Detailed error messages with tracebacks

**Tips:**
- Expand "View Details" to see operation logs (for individual operations)
- Expand "Error Traceback" if something goes wrong
- Use "Run All" for complete pipeline execution
- The interface automatically hides individual buttons when "Run All" is active
- Enable "Auto-export to CSV" in the sidebar to save all outputs automatically

### 2. 🏷️ Label Generator

Interactive label generation from MyBillBook inventory.

**Features:**

#### Search & Filter
- Search by product name (case-insensitive)
- Real-time filtering as you type
- Shows match count

#### Item Selection
- View all items in a sortable table
- Columns: Name, SKU Code, Quantity, Selling Price, Category
- Scrollable interface for large inventories

#### Label Generation Methods

**Method 1: Use Current MyBillBook Quantities**
- Automatically uses quantity from MyBillBook inventory
- One label per item in stock
- Quick generation for full inventory labeling

**Method 2: Manual Entry**
- Enter custom label count for each item
- Shows current quantity as reference
- Flexible for partial inventory or specific needs
- Input 0 to skip items

**Workflow:**
1. Load MyBillBook inventory (automatic)
2. Search/filter items (optional)
3. Choose label generation method
4. Click "Generate Labels" or "Generate with Manual Counts"
5. Labels written to "WePrint" sheet
6. Download CSV from "CSV Exports" page

**Tips:**
- Run "Sync MyBillBook" first for up-to-date data
- Use search to quickly find specific products
- Manual entry allows precise control over label counts
- Generated labels include Product Name, Barcode, and Price

### 3. 📥 CSV Exports

Browse, preview, and download your exported data.

**Features:**

#### Export Type Filter
- View all exports or filter by type:
  - `mybillbook_add` - New items to add
  - `mybillbook_update` - Existing items to update
  - `weprint` - Label printing data
  - `mybillbook_inventory_BACKUP` - Safety backups

#### File Browser
- Grouped by export type
- Shows latest 10 files per folder
- Displays file size and modification time
- Sorted by newest first

#### File Operations

**Preview Button (👁️)**
- View first 20 rows of CSV in browser
- Verify data before downloading
- No need to download full file

**Download Button (⬇️)**
- One-click CSV download
- Original filename preserved
- Standard CSV format for Excel/MyBillBook

**Tips:**
- Preview files before downloading to verify data
- Safety backups are created automatically (look for _BACKUP)
- Download files directly to your computer
- Import downloaded CSVs to MyBillBook for bulk operations

### 4. ℹ️ About

System information and documentation.

**Shows:**
- Application version and description
- Feature list with checkmarks
- Usage instructions
- Documentation links
- System status metrics:
  - Google Sheets connection status
  - CSV export file count
  - Python version

## Navigation

### Sidebar
- **Navigation Menu** - Radio buttons to switch between pages
- **Quick Stats** - Google Sheets connection status
- **Footer** - Built with Streamlit attribution

### Page Layout
- **Title** - Page name with icon
- **Content Area** - Main page content
- **Status Messages** - Success/error/info boxes
- **Progress Indicators** - Progress bars and spinners

## Error Handling

### Connection Errors
If you see "Failed to connect to Google Sheets":
1. Verify `credentials.json` exists in project directory
2. Check internet connection
3. Re-authenticate if `token.json` is corrupted (delete it and restart)

### Operation Errors
If an operation fails:
1. Check the error message displayed
2. Expand "Error Traceback" for technical details
3. Verify required sheets exist in Google Sheets
4. Ensure MyBillBook credentials are configured (for sync)

### Import Errors
If app fails to start:
1. Verify all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (3.8+ required)
3. Look for import error messages in console

## Best Practices

### Workflow
1. **Start with Sync** - Always sync MyBillBook first for accurate matching
2. **Check Results** - Preview sheets in Google Sheets after each operation
3. **Download Backups** - Save safety backups from CSV Exports page
4. **Test Labels** - Generate a few test labels before bulk printing

### Performance
- **Large Inventories** - Use search/filter in Label Generator
- **Multiple Operations** - Use "Run All" instead of clicking each step
- **Browser Tab** - Keep only one Streamlit tab open at a time

### Data Safety
- Safety backups are automatic before destructive operations
- Download important exports from CSV Exports page
- Verify data in preview before bulk import to MyBillBook

## Keyboard Shortcuts

Streamlit provides these built-in shortcuts:
- **R** - Rerun the app
- **C** - Clear cache
- **?** - Show keyboard shortcuts

## Troubleshooting

### "MyBillBook inventory is empty"
- Run "Sync MyBillBook" from Main Operations page
- Verify MyBillBook API credentials in `.env` file
- Check network connection to MyBillBook

### "No exports found"
- Run operations first (they create CSV exports)
- Check `csv_exports/` folder exists
- Verify file permissions

### "Session state does not function"
- This warning is normal when testing imports
- Only appears when running `python app.py` directly
- Ignore it when using `streamlit run app.py`

### UI Not Updating
- Press **R** to rerun the app
- Refresh browser page
- Clear cache with **C** key

### Slow Performance
- Close other Streamlit tabs
- Reduce number of items in Label Generator (use search)
- Restart Streamlit if memory usage is high

## Advanced Usage

### Custom Port
Run on a different port:
```cmd
streamlit run app.py --server.port 8502
```

### Network Access
Allow access from other devices on network:
```cmd
streamlit run app.py --server.address 0.0.0.0
```

### Configuration
Create `.streamlit/config.toml` for custom settings:
```toml
[server]
port = 8501
maxUploadSize = 200

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## Comparison: Web UI vs CLI

| Feature | Web UI | CLI (`main.py`) |
|---------|--------|-----------------|
| Interface | Browser-based | Command-line |
| Learning Curve | Easier | Moderate |
| Visual Feedback | Progress bars, colors | Text output |
| Error Display | Expandable tracebacks | Console output |
| CSV Download | Built-in download buttons | File system access |
| Label Entry | Interactive forms | Sequential prompts |
| Multi-tasking | Browser tabs | Terminal windows |
| Best For | Non-technical users | Power users, automation |

**Recommendation**: Use Web UI for daily operations, CLI for scripts/automation.

## Next Steps

After familiarizing yourself with the Web UI:

1. **Review Documentation**:
   - [Simple Workflow Guide](SIMPLE_WORKFLOW.md) - Step-by-step process
   - [Transform 1 Guide](TRANSFORM1_CONSOLIDATE.md) - Smart matching details
   - [Transform 2 Guide](TRANSFORM2_MYBILLBOOK.md) - MyBillBook export format
   - [CSV Exports Guide](CSV_EXPORTS.md) - Export and backup details

2. **Set Up MyBillBook** (if not done):
   - [MyBillBook Setup Guide](MYBILLBOOK_SETUP.md)

3. **Run Your First Pipeline**:
   - Go to Main Operations
   - Click "Run All Operations"
   - Download exports from CSV Exports page
   - Import to MyBillBook

## Support

For issues or questions:
- Check this guide first
- Review error messages and tracebacks
- Consult other documentation in `docs/` folder
- Verify Google Sheets and MyBillBook credentials

## Version History

**v1.0.0** (Current)
- Initial web UI release
- Main Operations page with Sync, Transform 1, Transform 2
- Label Generator with search and manual entry
- CSV Exports browser with preview and download
- About page with system status
- Error handling with expandable tracebacks
