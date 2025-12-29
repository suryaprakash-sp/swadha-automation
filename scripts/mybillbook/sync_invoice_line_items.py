#!/usr/bin/env python3
"""
Standalone Invoice Line Items Sync Script
Syncs individual products/items from each sales invoice to Google Sheets
Creates a denormalized table with one row per product sold
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
LINE_ITEMS_SHEET = "Invoice Line Items"  # Sheet name in Google Sheets


def fetch_invoice_details(api, invoice_id):
    """
    Fetch detailed invoice including line items

    Args:
        api: MyBillBookAPI instance
        invoice_id: Invoice ID

    Returns:
        Invoice details dict with 'items' array, or None if failed
    """
    result = api._make_request(f'/invoices/{invoice_id}')
    return result


def sync_invoice_line_items_to_sheets(
    sheets_manager,
    start_date: str = None,
    end_date: str = None,
):
    """
    Sync invoice line items to Google Sheets

    Args:
        sheets_manager: SheetsManager instance
        start_date: Start date filter (YYYY-MM-DD), default is 1 year ago
        end_date: End date filter (YYYY-MM-DD), default is today

    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*60)
    print("SYNCING INVOICE LINE ITEMS")
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

    # Step 1: Get all sales invoices (summary)
    print("Step 1: Fetching all sales invoices...")
    print("-" * 60)
    result = api.get_sales_invoices(
        per_page=15,
        start_date=start_date,
        end_date=end_date,
        status="final",
    )

    if not result or "vouchers" not in result:
        print("[ERROR] No invoices fetched. Sync failed.")
        return False

    invoices = result.get("vouchers", [])
    total_invoices = result.get("total_count", 0)

    if not invoices:
        print("[INFO] No invoices found for the specified date range.")
        return True

    print(f"Found {len(invoices)} invoices to process\n")

    # Step 2: Fetch detailed invoice for each to get line items
    print("Step 2: Fetching line items from each invoice...")
    print("-" * 60)

    all_line_items = []
    invoices_with_items = 0
    invoices_without_items = 0
    total_items_found = 0

    for idx, invoice in enumerate(invoices, 1):
        invoice_id = invoice.get("id")
        invoice_number = invoice.get("invoice_number")
        invoice_date = invoice.get("invoice_date")
        contact_name = invoice.get("contact_name")
        total_amount = invoice.get("total_amount")
        payment_mode = invoice.get("payment_mode")

        # Fetch detailed invoice
        print(f"  [{idx}/{len(invoices)}] Invoice #{invoice_number}...", end=" ")

        details = fetch_invoice_details(api, invoice_id)

        if details and "items" in details and details["items"]:
            items = details["items"]
            print(f"OK {len(items)} items")
            invoices_with_items += 1
            total_items_found += len(items)

            # Get invoice-level discount (applied to whole invoice, not per item)
            invoice_discount = float(details.get("discount") or 0)
            invoice_discount_type = details.get("discount_type", "")

            # Get invoice-level tax and charges
            round_off = float(details.get("round_off") or 0)
            tcs_amount = float(details.get("tcs_amount") or 0)
            tds_amount = float(details.get("tds_amount") or 0)
            cess_amount = float(details.get("cess_amount") or 0)

            # Get contact and address IDs
            contact_id = details.get("contact_id", "")
            billing_address_id = details.get("billing_address_id", "")
            shipping_address_id = details.get("shipping_address_id", "")

            # Get additional charges (array of charges)
            additional_charges = details.get("additional_charges", [])
            # Sum up all additional charges
            total_additional_charges = sum(float(charge.get("amount", 0)) for charge in additional_charges)

            # Extract each line item
            for item in items:
                # Get cost price from purchase_info for profit analysis
                purchase_info = item.get("purchase_info", {})
                cost_price = float(purchase_info.get("price_per_unit", 0)) if purchase_info else 0

                quantity = float(item.get("quantity") or 0)
                selling_price = float(item.get("price_per_unit") or 0)
                item_final_amount = float(item.get("item_final_amount") or 0)

                # Calculate profit (item final amount - total cost)
                total_cost = cost_price * quantity
                profit = item_final_amount - total_cost

                # Calculate profit margin percentage
                profit_margin_percent = (profit / item_final_amount * 100) if item_final_amount > 0 else 0

                line_item = {
                    "invoice_number": invoice_number,
                    "invoice_date": invoice_date,
                    "contact_name": contact_name,
                    "contact_id": contact_id,
                    "invoice_total": total_amount,
                    "payment_mode": payment_mode,
                    "invoice_discount": invoice_discount,
                    "invoice_discount_type": invoice_discount_type,
                    "round_off": round_off,
                    "tcs_amount": tcs_amount,
                    "tds_amount": tds_amount,
                    "cess_amount": cess_amount,
                    "additional_charges": total_additional_charges,
                    "billing_address_id": billing_address_id,
                    "shipping_address_id": shipping_address_id,
                    "item_name": item.get("name", ""),
                    "sku_code": item.get("sku_code", ""),
                    "quantity": quantity,
                    "unit": item.get("unit", ""),
                    "selling_price": selling_price,
                    "cost_price": cost_price,
                    "profit": profit,
                    "profit_margin_percent": profit_margin_percent,
                    "item_discount": float(item.get("discount") or 0),
                    "item_discount_type": item.get("discount_type", ""),
                    "item_discount_amount": float(item.get("discount_amount") or 0),
                    "gst_percentage": float(item.get("gst_percentage") or 0),
                    "is_tax_included": "Yes" if item.get("is_tax_included") else "No",
                    "item_final_amount": item_final_amount,
                    "item_type": item.get("item_type", ""),
                    "mrp": float(item.get("mrp") or 0),
                    "description": item.get("description", ""),
                    "notes": item.get("notes", ""),
                }
                all_line_items.append(line_item)
        else:
            print("-- No items")
            invoices_without_items += 1

        # Small delay to be nice to API
        if idx % 10 == 0:
            time.sleep(0.5)

    print()
    print(f"Summary:")
    print(f"  Invoices with items: {invoices_with_items}")
    print(f"  Invoices without items: {invoices_without_items}")
    print(f"  Total line items found: {total_items_found}")
    print()

    if not all_line_items:
        print("[INFO] No line items found.")
        return True

    # Prepare data for Google Sheets
    headers = [
        "Invoice Number",
        "Invoice Date",
        "Customer Name",
        "Contact ID",
        "Invoice Total",
        "Payment Mode",
        "Invoice Discount",
        "Invoice Discount Type",
        "Round Off",
        "TCS Amount",
        "TDS Amount",
        "Cess Amount",
        "Additional Charges",
        "Billing Address ID",
        "Shipping Address ID",
        "Item Name",
        "SKU Code",
        "Quantity",
        "Unit",
        "Selling Price",
        "Cost Price",
        "Profit",
        "Profit Margin %",
        "Item Discount",
        "Item Discount Type",
        "Item Discount Amount",
        "GST %",
        "Tax Included",
        "Item Final Amount",
        "Item Type",
        "MRP",
        "Description",
        "Notes",
    ]

    rows = []
    for item in all_line_items:
        row = [
            item["invoice_number"],
            item["invoice_date"],
            item["contact_name"],
            item["contact_id"],
            item["invoice_total"],
            item["payment_mode"],
            item["invoice_discount"],
            item["invoice_discount_type"],
            item["round_off"],
            item["tcs_amount"],
            item["tds_amount"],
            item["cess_amount"],
            item["additional_charges"],
            item["billing_address_id"],
            item["shipping_address_id"],
            item["item_name"],
            item["sku_code"],
            item["quantity"],
            item["unit"],
            item["selling_price"],
            item["cost_price"],
            item["profit"],
            item["profit_margin_percent"],
            item["item_discount"],
            item["item_discount_type"],
            item["item_discount_amount"],
            item["gst_percentage"],
            item["is_tax_included"],
            item["item_final_amount"],
            item["item_type"],
            item["mrp"],
            item["description"],
            item["notes"],
        ]
        rows.append(row)

    output = [headers] + rows

    # Create SAFETY BACKUP before clearing (automatic, no prompt)
    create_safety_backup(sheets_manager, LINE_ITEMS_SHEET, "invoice_line_items_BACKUP")

    # Write to Google Sheets
    print(f"Writing {len(rows)} line items to Google Sheets...")
    sheets_manager.clear_sheet(LINE_ITEMS_SHEET)
    sheets_manager.write_sheet(LINE_ITEMS_SHEET, output)

    # Apply formatting
    if len(rows) > 0:
        last_row = len(rows) + 1

        # Text columns
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"A2:A{last_row}")  # Invoice Number
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"B2:B{last_row}")  # Invoice Date
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"C2:C{last_row}")  # Customer Name
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"D2:D{last_row}")  # Contact ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"F2:F{last_row}")  # Payment Mode
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"H2:H{last_row}")  # Invoice Discount Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"N2:N{last_row}")  # Billing Address ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"O2:O{last_row}")  # Shipping Address ID
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"P2:P{last_row}")  # Item Name
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"Q2:Q{last_row}")  # SKU Code
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"S2:S{last_row}")  # Unit
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"Y2:Y{last_row}")  # Item Discount Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AB2:AB{last_row}")  # Tax Included
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AD2:AD{last_row}")  # Item Type
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AF2:AF{last_row}")  # Description
        sheets_manager.format_as_text(LINE_ITEMS_SHEET, f"AG2:AG{last_row}")  # Notes

        # Numeric columns with 2 decimals
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"E2:E{last_row}", decimal_places=2)  # Invoice Total
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"G2:G{last_row}", decimal_places=2)  # Invoice Discount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"I2:I{last_row}", decimal_places=2)  # Round Off
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"J2:J{last_row}", decimal_places=2)  # TCS Amount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"K2:K{last_row}", decimal_places=2)  # TDS Amount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"L2:L{last_row}", decimal_places=2)  # Cess Amount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"M2:M{last_row}", decimal_places=2)  # Additional Charges
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"R2:R{last_row}", decimal_places=2)  # Quantity
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"T2:T{last_row}", decimal_places=2)  # Selling Price
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"U2:U{last_row}", decimal_places=2)  # Cost Price
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"V2:V{last_row}", decimal_places=2)  # Profit
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"W2:W{last_row}", decimal_places=2)  # Profit Margin %
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"X2:X{last_row}", decimal_places=2)  # Item Discount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"Z2:Z{last_row}", decimal_places=2)  # Item Discount Amount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"AA2:AA{last_row}", decimal_places=2)  # GST %
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"AC2:AC{last_row}", decimal_places=2)  # Item Final Amount
        sheets_manager.format_as_number(LINE_ITEMS_SHEET, f"AE2:AE{last_row}", decimal_places=2)  # MRP

    print(f"\n[OK] Successfully synced {len(rows)} line items from {invoices_with_items} invoices!")
    print(f"     Sheet: '{LINE_ITEMS_SHEET}'")
    print(f"     Date range: {start_date} to {end_date}")

    # Export to CSV if user wants
    print("\n" + "="*60)
    export_sheet_data(sheets_manager, LINE_ITEMS_SHEET, "invoice_line_items", prompt_user=True)
    print("="*60 + "\n")

    return True


def main():
    """Main function to sync invoice line items"""
    print("\n" + "="*60)
    print("MYBILLBOOK INVOICE LINE ITEMS SYNC")
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
        success = sync_invoice_line_items_to_sheets(sheets, start_date, end_date)

        if success:
            print("\n" + "="*60)
            print("[SUCCESS] Invoice line items sync completed!")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("[FAILED] Invoice line items sync failed!")
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
