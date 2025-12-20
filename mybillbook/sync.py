"""
Sync MyBillBook inventory to Google Sheets
"""

from typing import List, Dict, Any
from mybillbook.api_client import MyBillBookAPI
from mybillbook.config import has_credentials


SYNC_SHEET_NAME = "MyBillBook Current Inventory"


def fetch_mybillbook_inventory() -> List[Dict[str, Any]]:
    """
    Fetch current inventory from MyBillBook API

    Returns:
        List of inventory items as dictionaries
    """
    api = MyBillBookAPI()

    # Test connection first
    if not api.test_connection():
        return []

    # Fetch all items
    response = api.get_all_items(per_page=500)

    if not response:
        print("[ERROR] Failed to fetch inventory from MyBillBook")
        return []

    inventory_items = response.get("inventory_items", [])
    total_count = response.get("total_count", 0)

    print(f"Fetched {len(inventory_items)} items from MyBillBook")
    print(f"Total items in system: {total_count}")

    return inventory_items


def sync_to_sheets(sheets_manager):
    """
    Sync MyBillBook inventory to Google Sheets

    Args:
        sheets_manager: SheetsManager instance

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("SYNCING MYBILLBOOK INVENTORY")
    print("="*60 + "\n")

    # Check if credentials are configured
    if not has_credentials():
        print("[ERROR] MyBillBook credentials not configured!")
        print("Please add the following to your .env file:")
        print("  MYBILLBOOK_AUTH_TOKEN=Bearer your_token_here")
        print("  MYBILLBOOK_COMPANY_ID=your_company_id")
        print("  MYBILLBOOK_COOKIES=your_cookies_here")
        print("\nSee docs for instructions on getting these credentials.")
        return False

    # Fetch inventory from MyBillBook
    items = fetch_mybillbook_inventory()

    if not items:
        print("[ERROR] No items fetched. Sync failed.")
        return False

    # Prepare data for Google Sheets
    headers = [
        "ID",
        "Name",
        "SKU Code",
        "Category",
        "MRP",
        "Selling Price",
        "Purchase Price",
        "Quantity",
        "Unit",
        "GST %",
        "Description",
    ]

    rows = []
    for item in items:
        row = [
            str(item.get("id", "")),
            item.get("name", ""),
            item.get("sku_code", ""),
            item.get("item_category_name", ""),
            float(item.get("mrp") or 0),
            float(item.get("selling_price") or 0),
            float(item.get("purchase_price") or 0),
            float(item.get("quantity") or 0),
            item.get("unit", ""),
            float(item.get("gst_percentage") or 0),
            item.get("description", ""),
        ]
        rows.append(row)

    output = [headers] + rows

    # Write to Google Sheets
    print(f"\nWriting {len(rows)} items to Google Sheets...")
    sheets_manager.clear_sheet(SYNC_SHEET_NAME)
    sheets_manager.write_sheet(SYNC_SHEET_NAME, output)

    # Apply formatting
    if len(rows) > 0:
        last_row = len(rows) + 1

        # Text columns
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"A2:A{last_row}")  # ID
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"B2:B{last_row}")  # Name
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"C2:C{last_row}")  # SKU
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"D2:D{last_row}")  # Category
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"I2:I{last_row}")  # Unit
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"K2:K{last_row}")  # Description

        # Numeric columns
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"E2:E{last_row}", decimal_places=2)  # MRP
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"F2:F{last_row}", decimal_places=2)  # Selling Price
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"G2:G{last_row}", decimal_places=2)  # Purchase Price
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"H2:H{last_row}", decimal_places=0)  # Quantity
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"J2:J{last_row}", decimal_places=2)  # GST %

    print(f"\n[OK] Successfully synced {len(rows)} items to '{SYNC_SHEET_NAME}' sheet!")
    print("="*60 + "\n")

    return True
