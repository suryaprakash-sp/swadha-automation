#!/usr/bin/env python3
"""
Standalone Expense Line Items Sync Script
Syncs individual items from each expense to Google Sheets
Creates a denormalized table with one row per expense item
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import time

# Add project root to path (two levels up: scripts/mybillbook -> scripts -> root)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.sheets import SheetsManager
from mybillbook.api_client import MyBillBookAPI
from mybillbook.config import has_credentials
from utils.csv_exporter import export_sheet_data, create_safety_backup


# Configuration
LINE_ITEMS_SHEET = "Expense Line Items"  # Sheet name in Google Sheets


def fetch_expense_details(api, expense_id):
    """
    Fetch detailed expense including line items

    Args:
        api: MyBillBookAPI instance
        expense_id: Expense ID

    Returns:
        Expense details dict with 'txn_ledgers' array, or None if failed
    """
    result = api._make_request(f'/expense/{expense_id}')
    return result


def sync_expense_line_items_to_sheets(
    sheets_manager,
    start_date: str = None,
    end_date: str = None,
):
    """
    Sync expense line items to Google Sheets

    Args:
        sheets_manager: SheetsManager instance
        start_date: Start date filter (YYYY-MM-DD), default is 1 year ago
        end_date: End date filter (YYYY-MM-DD), default is today

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("SYNCING EXPENSE LINE ITEMS")
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

    # Set default date range
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Date range: {start_date} to {end_date}\n")

    # Initialize API client
    api = MyBillBookAPI()

    # Test connection first
    if not api.test_connection():
        return False

    # Step 1: Get all expenses (summary)
    print("Step 1: Fetching all expenses...")
    print("-" * 60)
    result = api.get_expenses(
        per_page=15,
        start_date=start_date,
        end_date=end_date,
    )

    if not result or "vouchers" not in result:
        print("[ERROR] No expenses fetched. Sync failed.")
        return False

    expenses = result.get("vouchers", [])
    total_expenses = result.get("total_count", 0)

    if not expenses:
        print("[INFO] No expenses found for the specified date range.")
        return True

    print(f"Found {len(expenses)} expenses to process\n")

    # Step 2: Fetch detailed expense for each to get line items
    print("Step 2: Fetching line items from each expense...")
    print("-" * 60)

    all_line_items = []
    expenses_with_items = 0
    expenses_without_items = 0
    total_items_found = 0

    for idx, expense in enumerate(expenses, 1):
        expense_id = expense.get("id")
        expense_number = expense.get("invoice_number")
        expense_date = expense.get("invoice_date")
        total_amount = expense.get("total_amount")
        payment_mode = expense.get("payment_mode")

        # Fetch detailed expense
        print(f"  [{idx}/{len(expenses)}] Expense #{expense_number}...", end=" ")

        details = fetch_expense_details(api, expense_id)

        if details and "txn_ledgers" in details and details["txn_ledgers"]:
            items = details["txn_ledgers"]
            print(f"OK {len(items)} items")
            expenses_with_items += 1
            total_items_found += len(items)

            # Get expense-level fields
            expense_category = details.get("ledger_category_name", "")
            expense_category_id = details.get("ledger_category_id", "")
            payment_type = details.get("payment_type", "")
            notes = details.get("notes", "")
            source = details.get("source", "")
            discount = float(details.get("discount") or 0)
            discount_type = details.get("discount_type", "")
            round_off = float(details.get("round_off") or 0)
            place_of_supply = details.get("place_of_supply", "")

            # Get contact info if available
            contact_info = details.get("contact", {}) or {}
            contact_name = contact_info.get("name", "") if contact_info else ""
            contact_id = contact_info.get("id", "") if contact_info else ""

            # Extract each line item
            for item in items:
                line_item = {
                    "expense_number": expense_number,
                    "expense_date": expense_date,
                    "expense_category": expense_category,
                    "expense_category_id": expense_category_id,
                    "expense_total": float(total_amount) if total_amount else 0,
                    "payment_mode": payment_mode,
                    "payment_type": payment_type,
                    "expense_discount": discount,
                    "expense_discount_type": discount_type,
                    "round_off": round_off,
                    "place_of_supply": place_of_supply,
                    "contact_name": contact_name,
                    "contact_id": contact_id,
                    "item_name": item.get("name", ""),
                    "item_id": item.get("id", ""),
                    "ledger_id": item.get("ledger_id", ""),
                    "quantity": float(item.get("quantity") or 0),
                    "unit": item.get("unit", ""),
                    "unit_long": item.get("unit_long", ""),
                    "price_per_unit": float(item.get("price_per_unit") or 0),
                    "rate": float(item.get("rate") or 0),
                    "item_total_amount": float(item.get("total_amount") or 0),
                    "item_discount": float(item.get("discount") or 0),
                    "item_discount_type": item.get("discount_type", ""),
                    "gst_percentage": float(item.get("gst_percentage") or 0),
                    "is_tax_included": "Yes" if item.get("is_tax_included") else "No",
                    "is_tax_applicable": "Yes" if item.get("is_tax_applicable") else "No",
                    "is_tax_exempted": "Yes" if item.get("is_tax_exempted") else "No",
                    "itc_type": item.get("itc_type", ""),
                    "item_type": item.get("item_type", ""),
                    "identification_code": item.get("identification_code", ""),
                    "notes": notes,
                    "source": source,
                }
                all_line_items.append(line_item)
        else:
            print("-- No items")
            expenses_without_items += 1

        # Small delay to be nice to API
        if idx % 10 == 0:
            time.sleep(0.5)

    print()
    print(f"Summary:")
    print(f"  Expenses with items: {expenses_with_items}")
    print(f"  Expenses without items: {expenses_without_items}")
    print(f"  Total line items found: {total_items_found}")
    print()

    if not all_line_items:
        print("[INFO] No line items found.")
        return True

    # Prepare data for Google Sheets
    headers = [
        "Expense Number",
        "Expense Date",
        "Expense Category",
        "Expense Category ID",
        "Expense Total",
        "Payment Mode",
        "Payment Type",
        "Expense Discount",
        "Expense Discount Type",
        "Round Off",
        "Place of Supply",
        "Contact Name",
        "Contact ID",
        "Item Name",
        "Item ID",
        "Ledger ID",
        "Quantity",
        "Unit",
        "Unit Long",
        "Price Per Unit",
        "Rate",
        "Item Total Amount",
        "Item Discount",
        "Item Discount Type",
        "GST %",
        "Tax Included",
        "Tax Applicable",
        "Tax Exempted",
        "ITC Type",
        "Item Type",
        "Identification Code",
        "Notes",
        "Source",
    ]

    rows = []
    for item in all_line_items:
        row = [
            item["expense_number"],
            item["expense_date"],
            item["expense_category"],
            item["expense_category_id"],
            item["expense_total"],
            item["payment_mode"],
            item["payment_type"],
            item["expense_discount"],
            item["expense_discount_type"],
            item["round_off"],
            item["place_of_supply"],
            item["contact_name"],
            item["contact_id"],
            item["item_name"],
            item["item_id"],
            item["ledger_id"],
            item["quantity"],
            item["unit"],
            item["unit_long"],
            item["price_per_unit"],
            item["rate"],
            item["item_total_amount"],
            item["item_discount"],
            item["item_discount_type"],
            item["gst_percentage"],
            item["is_tax_included"],
            item["is_tax_applicable"],
            item["is_tax_exempted"],
            item["itc_type"],
            item["item_type"],
            item["identification_code"],
            item["notes"],
            item["source"],
        ]
        rows.append(row)

    output = [headers] + rows

    # Create SAFETY BACKUP before clearing (automatic, no prompt)
    create_safety_backup(sheets_manager, LINE_ITEMS_SHEET, "expense_line_items_BACKUP")

    # Write to Google Sheets
    print(f"Writing {len(rows)} expense line items to Google Sheets...")
    sheets_manager.clear_sheet(LINE_ITEMS_SHEET)
    sheets_manager.write_sheet(LINE_ITEMS_SHEET, output)

    # Apply formatting
    if len(rows) > 0:
        last_row = len(rows) + 1

        # Text columns
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"A2:A{last_row}")  # Expense Number
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"B2:B{last_row}")  # Expense Date
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"C2:C{last_row}")  # Expense Category
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"D2:D{last_row}")  # Expense Category ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"F2:F{last_row}")  # Payment Mode
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"G2:G{last_row}")  # Payment Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"I2:I{last_row}")  # Expense Discount Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"K2:K{last_row}")  # Place of Supply
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"L2:L{last_row}")  # Contact Name
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"M2:M{last_row}")  # Contact ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"N2:N{last_row}")  # Item Name
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"O2:O{last_row}")  # Item ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"P2:P{last_row}")  # Ledger ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"R2:R{last_row}")  # Unit
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"S2:S{last_row}")  # Unit Long
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"X2:X{last_row}")  # Item Discount Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"Z2:Z{last_row}")  # Tax Included
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AA2:AA{last_row}")  # Tax Applicable
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AB2:AB{last_row}")  # Tax Exempted
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AC2:AC{last_row}")  # ITC Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AD2:AD{last_row}")  # Item Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AE2:AE{last_row}")  # Identification Code
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AF2:AF{last_row}")  # Notes
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AG2:AG{last_row}")  # Source

        # Numeric columns with 2 decimals
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"E2:E{last_row}", decimal_places=2)  # Expense Total
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"H2:H{last_row}", decimal_places=2)  # Expense Discount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"J2:J{last_row}", decimal_places=2)  # Round Off
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"Q2:Q{last_row}", decimal_places=2)  # Quantity
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"T2:T{last_row}", decimal_places=2)  # Price Per Unit
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"U2:U{last_row}", decimal_places=2)  # Rate
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"V2:V{last_row}", decimal_places=2)  # Item Total Amount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"W2:W{last_row}", decimal_places=2)  # Item Discount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"Y2:Y{last_row}", decimal_places=2)  # GST %

    print(f"\n[OK] Successfully synced {len(rows)} expense line items from {expenses_with_items} expenses!")
    print(f"     Sheet: '{LINE_ITEMS_SHEET}'")
    print(f"     Date range: {start_date} to {end_date}")

    # Export to CSV if user wants
    print("\n" + "="*60)
    export_sheet_data(sheets_manager, LINE_ITEMS_SHEET, "expense_line_items", prompt_user=True)
    print("="*60 + "\n")

    return True


def main():
    """Main function to sync expense line items"""
    print("\n" + "="*60)
    print("MYBILLBOOK EXPENSE LINE ITEMS SYNC")
    print("="*60 + "\n")

    try:
        # Initialize Google Sheets connection
        print("Connecting to Google Sheets...")
        sheets = SheetsManager()
        print("[OK] Connected to Google Sheets!\n")

        # Ask for date range
        print("Date Range Options:")
        print("1. Last 30 days")
        print("2. Last 90 days")
        print("3. Last 1 year (default)")
        print("4. Custom date range")
        choice = input("\nEnter your choice (1-4, default=3): ").strip() or "3"

        start_date = None
        end_date = None

        if choice == "1":
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif choice == "2":
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif choice == "3":
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        elif choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            # Validate dates
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                print("[ERROR] Invalid date format. Using default (last 1 year).")
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
        else:
            print("[INFO] Invalid choice. Using default (last 1 year).")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Run sync
        success = sync_expense_line_items_to_sheets(sheets, start_date, end_date)

        if success:
            print("\n" + "="*60)
            print("[SUCCESS] Expense line items sync completed!")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("[FAILED] Expense line items sync failed!")
            print("="*60 + "\n")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nPlease ensure you have:")
        print("1. Created credentials.json from Google Cloud Console")
        print("2. Placed it in the project directory")
        print("\nSee README.md for setup instructions.")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
