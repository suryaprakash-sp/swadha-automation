#!/usr/bin/env python3
"""
Standalone Sales Invoices Sync Script
Syncs MyBillBook sales invoices (vouchers) to Google Sheets
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path (two levels up: scripts/mybillbook -> scripts -> root)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.sheets import SheetsManager
from mybillbook.api_client import MyBillBookAPI
from mybillbook.config import has_credentials
from utils.csv_exporter import export_sheet_data, create_safety_backup


# Configuration
SALES_INVOICES_SHEET = "Sales Invoices"  # Sheet name in Google Sheets


def sync_sales_invoices_to_sheets(
    sheets_manager,
    start_date: str = None,
    end_date: str = None,
):
    """
    Sync MyBillBook sales invoices to Google Sheets

    Args:
        sheets_manager: SheetsManager instance
        start_date: Start date filter (YYYY-MM-DD), default is 1 year ago
        end_date: End date filter (YYYY-MM-DD), default is today

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("SYNCING MYBILLBOOK SALES INVOICES")
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

    # Fetch sales invoices
    result = api.get_sales_invoices(
        per_page=15,
        start_date=start_date,
        end_date=end_date,
        status="final",
    )

    if not result or "vouchers" not in result:
        print("[ERROR] No invoices fetched. Sync failed.")
        return False

    vouchers = result.get("vouchers", [])
    total_count = result.get("total_count", 0)

    if not vouchers:
        print("[INFO] No invoices found for the specified date range.")
        return True

    # Prepare data for Google Sheets
    headers = [
        "Invoice Number",
        "Invoice Date",
        "Serial Number",
        "Contact Name",
        "Contact Type",
        "Contact ID",
        "Total Amount",
        "Paid Amount",
        "Remaining Amount",
        "Payment Mode",
        "Payment Type",
        "Due Date",
        "Status",
        "Created At",
        "ID",
        "MBB ID",
        "Share Link",
        "Notes",
        "Source",
        "Ledger Category",
        "Bank Account ID",
        "Convertable ID",
        "Recurring ID",
        "E-Invoice Status",
    ]

    rows = []
    for voucher in vouchers:
        row = [
            voucher.get("invoice_number", ""),
            voucher.get("invoice_date", ""),
            voucher.get("serial_number", ""),
            voucher.get("contact_name", ""),
            voucher.get("contact_type", ""),
            voucher.get("contact_id", ""),
            float(voucher.get("total_amount") or 0),
            float(voucher.get("initial_payment_amount") or 0),
            float(voucher.get("remaining_amount") or 0),
            voucher.get("payment_mode", ""),
            voucher.get("payment_type", ""),
            voucher.get("due_date", ""),
            voucher.get("status", ""),
            voucher.get("created_at", ""),
            voucher.get("id", ""),
            voucher.get("mbb_id", ""),
            voucher.get("share_link", ""),
            voucher.get("notes", ""),
            voucher.get("source", ""),
            voucher.get("ledger_category_name", ""),
            voucher.get("bank_account_id", ""),
            voucher.get("convertable_id", ""),
            voucher.get("recurring_id", ""),
            voucher.get("einvoice_status", ""),
        ]
        rows.append(row)

    output = [headers] + rows

    # Create SAFETY BACKUP before clearing (automatic, no prompt)
    create_safety_backup(sheets_manager, SALES_INVOICES_SHEET, "sales_invoices_BACKUP")

    # Write to Google Sheets
    print(f"\nWriting {len(rows)} invoices to Google Sheets...")
    sheets_manager.clear_sheet(SALES_INVOICES_SHEET)
    sheets_manager.write_sheet(SALES_INVOICES_SHEET, output)

    # Apply formatting
    if len(rows) > 0:
        last_row = len(rows) + 1

        # Text columns
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"A2:A{last_row}")  # Invoice Number
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"B2:B{last_row}")  # Invoice Date
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"C2:C{last_row}")  # Serial Number
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"D2:D{last_row}")  # Contact Name
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"E2:E{last_row}")  # Contact Type
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"F2:F{last_row}")  # Contact ID
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"J2:J{last_row}")  # Payment Mode
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"K2:K{last_row}")  # Payment Type
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"L2:L{last_row}")  # Due Date
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"M2:M{last_row}")  # Status
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"N2:N{last_row}")  # Created At
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"O2:O{last_row}")  # ID
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"P2:P{last_row}")  # MBB ID
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"Q2:Q{last_row}")  # Share Link
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"R2:R{last_row}")  # Notes
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"S2:S{last_row}")  # Source
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"T2:T{last_row}")  # Ledger Category
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"U2:U{last_row}")  # Bank Account ID
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"V2:V{last_row}")  # Convertable ID
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"W2:W{last_row}")  # Recurring ID
        sheets_manager.format_as_text(SALES_INVOICES_SHEET, f"X2:X{last_row}")  # E-Invoice Status

        # Numeric columns with 2 decimals
        sheets_manager.format_as_number(SALES_INVOICES_SHEET, f"G2:G{last_row}", decimal_places=2)  # Total Amount
        sheets_manager.format_as_number(SALES_INVOICES_SHEET, f"H2:H{last_row}", decimal_places=2)  # Paid Amount
        sheets_manager.format_as_number(SALES_INVOICES_SHEET, f"I2:I{last_row}", decimal_places=2)  # Remaining Amount

    print(f"\n[OK] Successfully synced {len(rows)} sales invoices to '{SALES_INVOICES_SHEET}' sheet!")
    print(f"     Date range: {start_date} to {end_date}")

    # Export to CSV if user wants
    print("\n" + "="*60)
    export_sheet_data(sheets_manager, SALES_INVOICES_SHEET, "sales_invoices", prompt_user=True)
    print("="*60 + "\n")

    return True


def main():
    """Main function to sync sales invoices"""
    print("\n" + "="*60)
    print("MYBILLBOOK SALES INVOICES SYNC")
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
        success = sync_sales_invoices_to_sheets(sheets, start_date, end_date)

        if success:
            print("\n" + "="*60)
            print("[SUCCESS] Sales invoices sync completed!")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("[FAILED] Sales invoices sync failed!")
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
