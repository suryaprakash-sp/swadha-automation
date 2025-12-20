# MyBillBook API Setup Guide

## Overview

The MyBillBook sync functionality fetches your current inventory from MyBillBook and syncs it to Google Sheets. This allows Transform 2 to properly determine which items should be added vs updated.

## Why is this needed?

When generating MyBillBook import files, we need to know which items already exist in your MyBillBook inventory:
- **Existing items** → Go to "myBillBook update" sheet (update quantity/price)
- **New items** → Go to "myBillBook add" sheet (add new product)

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `requests` and `python-dotenv` for API communication.

### Step 2: Get MyBillBook Credentials

MyBillBook doesn't have a public API, so we use the internal web API that the browser uses. You need to capture authentication tokens from your browser:

1. **Login to MyBillBook** at https://mybillbook.in

2. **Open Developer Tools** (F12 or Right-click → Inspect)

3. **Go to Network tab**

4. **Filter by "Fetch/XHR"** requests

5. **Navigate to Items page**:
   - Click on "Inventory" or "Items" in MyBillBook
   - Or go to: `https://mybillbook.in/app/home/items`

6. **Find an API request**:
   - Look for requests to `/api/web/items` or similar
   - Click on one of them

7. **Copy Request Headers**:

   Find and copy these headers:

   **Authorization** (looks like):
   ```
   Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI...
   ```

   **Company-Id** (looks like):
   ```
   8fa87fa8-79e4-4a00-951d-7b9c3a41eefa
   ```

   **Note**: Cookies are optional and not required for the API to work.

### Step 3: Configure Environment Variables

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and paste your credentials:
   ```env
   MYBILLBOOK_AUTH_TOKEN=Bearer eyJhbGciOiJIUzI1NiJ9...
   MYBILLBOOK_COMPANY_ID=8fa87fa8-79e4-4a00-951d-7b9c3a41eefa
   MYBILLBOOK_COOKIES=
   ```

   **Note**: You only need the Authorization token and Company ID. Cookies can be left empty.

3. **Save the file**

### Step 4: Test the Connection

Run the sync function to test:

```bash
python main.py
# Select option 0: Sync MyBillBook Inventory
```

If successful, you'll see:
```
[OK] MyBillBook API connection successful!
Fetched X items from MyBillBook
[OK] Successfully synced X items to 'MyBillBook Current Inventory' sheet!
```

## Troubleshooting

### "Authentication failed" or "403 Error"

**Problem**: Your credentials have expired

**Solution**:
- Tokens typically expire after a few hours
- Re-capture the credentials from browser DevTools
- Update the `.env` file with fresh tokens

### "No items fetched"

**Problem**: API request failed or no inventory in MyBillBook

**Solution**:
- Check that you have items in your MyBillBook inventory
- Verify credentials are correct
- Check internet connection

### "MyBillBook credentials not configured"

**Problem**: `.env` file is missing or empty

**Solution**:
- Make sure `.env` file exists in project root
- Verify required credentials are set:
  - `MYBILLBOOK_AUTH_TOKEN` (required)
  - `MYBILLBOOK_COMPANY_ID` (required)
  - `MYBILLBOOK_COOKIES` (optional - can be left empty)

## What Gets Synced

The sync pulls the following data from MyBillBook:

### Basic Information
| Field | Description |
|-------|-------------|
| ID | MyBillBook item ID |
| Name | Product name |
| SKU Code | Item code/barcode |
| Category | Product category |
| Description | Item description |

### Pricing
| Field | Description |
|-------|-------------|
| MRP | Maximum retail price |
| Selling Price | Current selling price |
| Sales Price | Sales price (may differ from selling price) |
| Purchase Price | Cost price |
| Wholesale Price | Bulk/wholesale pricing |
| Wholesale Min Qty | Minimum quantity for wholesale price |

### Inventory
| Field | Description |
|-------|-------------|
| Quantity | Current stock level |
| Minimum Quantity | Minimum stock level / reorder point |
| Unit | Unit of measurement (short) |
| Unit Long | Unit of measurement (full name) |

### Tax & Compliance
| Field | Description |
|-------|-------------|
| GST % | GST percentage |
| Sales Tax Included | Whether tax is included in selling price |
| Purchase Tax Included | Whether tax is included in purchase price |

### Metadata
| Field | Description |
|-------|-------------|
| Item Type | Product type identifier |
| Show on Store | Whether item is visible on online store |
| Excel Imported | Whether item was imported from Excel |
| Created Date | When the item was created in MyBillBook |
| Identification Code | Additional identification code |
| Conversion Factor | Unit conversion factor |

This data is written to the **"myBillBook Inventory"** sheet in Google Sheets.

## Usage in Workflow

### Option 1: Manual Sync

```bash
python main.py
# Select 0: Sync MyBillBook Inventory
# Then run other transforms as needed
```

### Option 2: Full Pipeline

```bash
python main.py
# Select 4: Run All Operations
# This automatically syncs before running transforms
```

## Security Notes

- **Never commit `.env` to git** - it contains sensitive credentials
- `.env` is already in `.gitignore`
- Tokens expire regularly - update them as needed
- Use read-only access - script only fetches data, never modifies

## Workflow Integration

```
Sync MyBillBook Inventory
   ↓
   Creates/Updates "myBillBook Inventory" sheet
   ↓
Transform 1: Consolidate Inventory RAW
   ↓
Transform 2: MyBillBook Import (uses synced data)
   ↓
   Checks if items exist in "myBillBook Inventory"
   ↓
   Existing → "myBillBook update"
   New → "myBillBook add"
   ↓
Transform 3: WePrint Export
```

## Frequency

**How often should you sync?**

- Before running Transform 2 (to get latest inventory)
- After manually adding/removing items in MyBillBook
- At least once a day if you're actively managing inventory

The sync is fast (5-10 seconds for 100+ items) and can be run as often as needed.

## API Rate Limits

MyBillBook may have rate limits on API requests:
- The script has built-in retry logic
- Wait 2-5 minutes if you hit rate limits
- Avoid running sync too frequently (once per minute should be fine)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify credentials are fresh (re-capture if > 24 hours old)
3. Test connection using option 0 in the menu
4. Check that MyBillBook website is accessible
