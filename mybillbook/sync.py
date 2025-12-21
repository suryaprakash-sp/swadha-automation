"""
Sync MyBillBook inventory to Google Sheets
"""

from typing import List, Dict, Any
from mybillbook.api_client import MyBillBookAPI
from mybillbook.config import has_credentials
from config import SHEET_MYBILLBOOK_CURRENT
from utils.csv_exporter import export_sheet_data, create_safety_backup


SYNC_SHEET_NAME = SHEET_MYBILLBOOK_CURRENT


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
        "Sales Price",
        "Purchase Price",
        "Wholesale Price",
        "Wholesale Min Qty",
        "Quantity",
        "Minimum Quantity",
        "Unit",
        "Unit Long",
        "GST %",
        "Sales Tax Included",
        "Purchase Tax Included",
        "Description",
        "Item Type",
        "Show on Store",
        "Excel Imported",
        "Created Date",
        "Identification Code",
        "Conversion Factor",
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
            float(item.get("sales_price") or 0),
            float(item.get("purchase_price") or 0),
            float(item.get("wholesale_price") or 0),
            float(item.get("wholesale_min_quantity") or 0),
            float(item.get("quantity") or 0),
            float(item.get("minimum_quantity") or 0),
            item.get("unit", ""),
            item.get("unit_long", ""),
            float(item.get("gst_percentage") or 0),
            "Yes" if item.get("sales_tax_included") else "No",
            "Yes" if item.get("purchase_tax_included") else "No",
            item.get("description", ""),
            str(item.get("item_type", "")),
            "Yes" if item.get("show_on_store") else "No",
            "Yes" if item.get("excel_imported") else "No",
            item.get("created_at", ""),
            item.get("identification_code", ""),
            float(item.get("conversion_factor") or 0),
        ]
        rows.append(row)

    output = [headers] + rows

    # Create SAFETY BACKUP before clearing (automatic, no prompt)
    create_safety_backup(sheets_manager, SYNC_SHEET_NAME, "mybillbook_inventory_BACKUP")

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
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"C2:C{last_row}")  # SKU Code
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"D2:D{last_row}")  # Category
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"M2:M{last_row}")  # Unit
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"N2:N{last_row}")  # Unit Long
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"P2:P{last_row}")  # Sales Tax Included
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"Q2:Q{last_row}")  # Purchase Tax Included
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"R2:R{last_row}")  # Description
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"S2:S{last_row}")  # Item Type
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"T2:T{last_row}")  # Show on Store
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"U2:U{last_row}")  # Excel Imported
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"V2:V{last_row}")  # Created Date
        sheets_manager.format_as_text(SYNC_SHEET_NAME, f"W2:W{last_row}")  # Identification Code

        # Numeric columns with 2 decimals
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"E2:E{last_row}", decimal_places=2)  # MRP
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"F2:F{last_row}", decimal_places=2)  # Selling Price
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"G2:G{last_row}", decimal_places=2)  # Sales Price
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"H2:H{last_row}", decimal_places=2)  # Purchase Price
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"I2:I{last_row}", decimal_places=2)  # Wholesale Price
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"J2:J{last_row}", decimal_places=2)  # Wholesale Min Qty
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"O2:O{last_row}", decimal_places=2)  # GST %
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"X2:X{last_row}", decimal_places=2)  # Conversion Factor

        # Numeric columns with 0 decimals
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"K2:K{last_row}", decimal_places=0)  # Quantity
        sheets_manager.format_as_number(SYNC_SHEET_NAME, f"L2:L{last_row}", decimal_places=0)  # Minimum Quantity

    print(f"\n[OK] Successfully synced {len(rows)} items to '{SYNC_SHEET_NAME}' sheet!")

    # Export to CSV if user wants
    print("\n" + "="*60)
    export_sheet_data(sheets_manager, SYNC_SHEET_NAME, "mybillbook_inventory", prompt_user=True)
    print("="*60 + "\n")

    return True
