#!/usr/bin/env python3
"""
Sync MyBillBook data from Google Sheets to PostgreSQL
Loads data from Google Sheets into the analytics database
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

from utils.sheets import SheetsManager
from config import (
    SHEET_MYBILLBOOK_CURRENT,
    SHEET_SALES_INVOICES,
    SHEET_EXPENSES,
    SHEET_INVOICE_LINE_ITEMS,
)

# PostgreSQL connection settings from environment
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "database": os.getenv("POSTGRES_DATABASE", "mybillbook_analytics"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

# Sheet names
EXPENSE_LINE_ITEMS_SHEET = "Expense Line Items"


def get_db_connection():
    """Create PostgreSQL connection"""
    return psycopg2.connect(**DB_CONFIG)


def parse_date(date_str):
    """Parse date string to date object"""
    if not date_str:
        return None
    try:
        # Try different formats
        for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]:
            try:
                return datetime.strptime(str(date_str), fmt).date()
            except ValueError:
                continue
        return None
    except Exception:
        return None


def parse_float(value):
    """Parse numeric value, handling commas"""
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except (ValueError, TypeError):
        return None


def parse_bool(value):
    """Parse boolean value"""
    if value is None:
        return None
    return str(value).lower() in ("yes", "true", "1")


def sync_products(conn, sheets_manager):
    """Sync products/inventory to PostgreSQL"""
    print("\nSyncing Products (Inventory)...")

    data = sheets_manager.read_sheet(SHEET_MYBILLBOOK_CURRENT)
    if not data or len(data) < 2:
        print("  No product data found")
        return 0

    headers = data[0]
    rows = data[1:]

    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM mybillbook.products")

    insert_sql = """
        INSERT INTO mybillbook.products (
            product_id, product_name, sku_code,
            mrp, selling_price, sales_price, purchase_price,
            wholesale_price, wholesale_min_qty,
            quantity, minimum_quantity, unit, unit_long,
            gst_percentage, sales_tax_included, purchase_tax_included,
            description, item_type, show_on_store, excel_imported,
            created_at, identification_code, conversion_factor
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    batch_data = []
    for row in rows:
        # Pad row to expected length
        row = row + [""] * (24 - len(row)) if len(row) < 24 else row

        batch_data.append((
            str(row[0]) if row[0] else None,  # product_id
            row[1] or None,  # product_name
            row[2] or None,  # sku_code
            parse_float(row[4]),  # mrp
            parse_float(row[5]),  # selling_price
            parse_float(row[6]),  # sales_price
            parse_float(row[7]),  # purchase_price
            parse_float(row[8]),  # wholesale_price
            parse_float(row[9]),  # wholesale_min_qty
            parse_float(row[10]),  # quantity
            parse_float(row[11]),  # minimum_quantity
            row[12] or None,  # unit
            row[13] or None,  # unit_long
            parse_float(row[14]),  # gst_percentage
            parse_bool(row[15]),  # sales_tax_included
            parse_bool(row[16]),  # purchase_tax_included
            row[17] or None,  # description
            row[18] or None,  # item_type
            parse_bool(row[19]),  # show_on_store
            parse_bool(row[20]),  # excel_imported
            row[21] or None,  # created_at
            row[22] or None,  # identification_code
            parse_float(row[23]),  # conversion_factor
        ))

    execute_batch(cursor, insert_sql, batch_data)
    conn.commit()

    print(f"  Synced {len(batch_data)} products")
    return len(batch_data)


def sync_contacts_from_invoices(conn, sheets_manager):
    """Extract and sync unique contacts from invoices and expenses"""
    print("\nSyncing Contacts...")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM mybillbook.contacts")

    contacts = {}

    # Extract from Sales Invoices
    data = sheets_manager.read_sheet(SHEET_SALES_INVOICES)
    if data and len(data) > 1:
        for row in data[1:]:
            row = row + [""] * (24 - len(row)) if len(row) < 24 else row
            contact_id = row[5]  # Contact ID
            if contact_id and contact_id not in contacts:
                contacts[contact_id] = {
                    "contact_id": contact_id,
                    "contact_name": row[3] or "Unknown",  # Contact Name
                    "contact_type": row[4] or "Customer",  # Contact Type
                }

    # Extract from Expenses
    data = sheets_manager.read_sheet(SHEET_EXPENSES)
    if data and len(data) > 1:
        for row in data[1:]:
            row = row + [""] * (19 - len(row)) if len(row) < 19 else row
            contact_id = row[17]  # Contact ID
            if contact_id and contact_id not in contacts:
                contacts[contact_id] = {
                    "contact_id": contact_id,
                    "contact_name": row[16] or "Unknown",  # Contact Name
                    "contact_type": "Vendor",
                }

    insert_sql = """
        INSERT INTO mybillbook.contacts (contact_id, contact_name, contact_type)
        VALUES (%s, %s, %s)
        ON CONFLICT (contact_id) DO UPDATE SET
            contact_name = EXCLUDED.contact_name
    """

    batch_data = [(c["contact_id"], c["contact_name"], c["contact_type"])
                  for c in contacts.values()]

    if batch_data:
        execute_batch(cursor, insert_sql, batch_data)
        conn.commit()

    print(f"  Synced {len(batch_data)} contacts")
    return len(batch_data)


def sync_sales_invoices(conn, sheets_manager):
    """Sync sales invoices to PostgreSQL"""
    print("\nSyncing Sales Invoices...")

    data = sheets_manager.read_sheet(SHEET_SALES_INVOICES)
    if not data or len(data) < 2:
        print("  No invoice data found")
        return 0

    rows = data[1:]
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mybillbook.sales_invoices")

    insert_sql = """
        INSERT INTO mybillbook.sales_invoices (
            invoice_id, mbb_id, invoice_number, serial_number, invoice_date,
            contact_id, contact_name, contact_type,
            total_amount, paid_amount, remaining_amount,
            payment_mode, payment_type, bank_account_id,
            due_date, status, created_at,
            share_link, notes, source, ledger_category,
            convertable_id, recurring_id, einvoice_status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    batch_data = []
    for row in rows:
        row = row + [""] * (24 - len(row)) if len(row) < 24 else row

        batch_data.append((
            row[14] or None,  # invoice_id (ID column)
            row[15] or None,  # mbb_id
            row[0] or None,   # invoice_number
            row[2] or None,   # serial_number
            parse_date(row[1]),  # invoice_date
            row[5] or None,   # contact_id
            row[3] or None,   # contact_name
            row[4] or None,   # contact_type
            parse_float(row[6]),   # total_amount
            parse_float(row[7]),   # paid_amount
            parse_float(row[8]),   # remaining_amount
            row[9] or None,   # payment_mode
            row[10] or None,  # payment_type
            row[20] or None,  # bank_account_id
            parse_date(row[11]),  # due_date
            row[12] or None,  # status
            row[13] or None,  # created_at
            row[16] or None,  # share_link
            row[17] or None,  # notes
            row[18] or None,  # source
            row[19] or None,  # ledger_category
            row[21] or None,  # convertable_id
            row[22] or None,  # recurring_id
            row[23] or None,  # einvoice_status
        ))

    execute_batch(cursor, insert_sql, batch_data)
    conn.commit()

    print(f"  Synced {len(batch_data)} sales invoices")
    return len(batch_data)


def sync_sales_invoice_line_items(conn, sheets_manager):
    """Sync invoice line items to PostgreSQL"""
    print("\nSyncing Sales Invoice Line Items...")

    data = sheets_manager.read_sheet(SHEET_INVOICE_LINE_ITEMS)
    if not data or len(data) < 2:
        print("  No line item data found")
        return 0

    rows = data[1:]
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mybillbook.sales_invoice_line_items")

    insert_sql = """
        INSERT INTO mybillbook.sales_invoice_line_items (
            invoice_number, invoice_date, customer_name, contact_id,
            invoice_total, payment_mode,
            invoice_discount, invoice_discount_type,
            round_off, tcs_amount, tds_amount, cess_amount, additional_charges,
            billing_address_id, shipping_address_id,
            item_name, sku_code, quantity, unit,
            selling_price, cost_price, profit, profit_margin_percent,
            item_discount, item_discount_type, item_discount_amount,
            gst_percentage, tax_included, item_final_amount,
            item_type, mrp, description, notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    batch_data = []
    for row in rows:
        row = row + [""] * (33 - len(row)) if len(row) < 33 else row

        batch_data.append((
            row[0] or None,   # invoice_number
            parse_date(row[1]),  # invoice_date
            row[2] or None,   # customer_name
            row[3] or None,   # contact_id
            parse_float(row[4]),   # invoice_total
            row[5] or None,   # payment_mode
            parse_float(row[6]),   # invoice_discount
            row[7] or None,   # invoice_discount_type
            parse_float(row[8]),   # round_off
            parse_float(row[9]),   # tcs_amount
            parse_float(row[10]),  # tds_amount
            parse_float(row[11]),  # cess_amount
            parse_float(row[12]),  # additional_charges
            row[13] or None,  # billing_address_id
            row[14] or None,  # shipping_address_id
            row[15] or None,  # item_name
            row[16] or None,  # sku_code
            parse_float(row[17]),  # quantity
            row[18] or None,  # unit
            parse_float(row[19]),  # selling_price
            parse_float(row[20]),  # cost_price
            parse_float(row[21]),  # profit
            parse_float(row[22]),  # profit_margin_percent
            parse_float(row[23]),  # item_discount
            row[24] or None,  # item_discount_type
            parse_float(row[25]),  # item_discount_amount
            parse_float(row[26]),  # gst_percentage
            parse_bool(row[27]),  # tax_included
            parse_float(row[28]),  # item_final_amount
            row[29] or None,  # item_type
            parse_float(row[30]),  # mrp
            row[31] or None,  # description
            row[32] or None,  # notes
        ))

    execute_batch(cursor, insert_sql, batch_data)
    conn.commit()

    print(f"  Synced {len(batch_data)} invoice line items")
    return len(batch_data)


def sync_expenses(conn, sheets_manager):
    """Sync expenses to PostgreSQL"""
    print("\nSyncing Expenses...")

    data = sheets_manager.read_sheet(SHEET_EXPENSES)
    if not data or len(data) < 2:
        print("  No expense data found")
        return 0

    rows = data[1:]
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mybillbook.expenses")

    insert_sql = """
        INSERT INTO mybillbook.expenses (
            expense_id, mbb_id, expense_number, serial_number, expense_date,
            ledger_category_name, line_items_count,
            total_amount, paid_amount, payment_mode, payment_type,
            created_at, notes, source, bank_account_id,
            contact_name, contact_id, share_link
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    batch_data = []
    for row in rows:
        row = row + [""] * (19 - len(row)) if len(row) < 19 else row

        batch_data.append((
            row[11] or None,  # expense_id (ID column)
            row[12] or None,  # mbb_id
            row[0] or None,   # expense_number
            row[2] or None,   # serial_number
            parse_date(row[1]),  # expense_date
            row[3] or None,   # ledger_category_name
            parse_float(row[5]),  # line_items_count
            parse_float(row[6]),  # total_amount
            parse_float(row[7]),  # paid_amount
            row[8] or None,   # payment_mode
            row[9] or None,   # payment_type
            row[10] or None,  # created_at
            row[13] or None,  # notes
            row[14] or None,  # source
            row[15] or None,  # bank_account_id
            row[16] or None,  # contact_name
            row[17] or None,  # contact_id
            row[18] or None,  # share_link
        ))

    execute_batch(cursor, insert_sql, batch_data)
    conn.commit()

    print(f"  Synced {len(batch_data)} expenses")
    return len(batch_data)


def sync_expense_line_items(conn, sheets_manager):
    """Sync expense line items to PostgreSQL"""
    print("\nSyncing Expense Line Items...")

    data = sheets_manager.read_sheet(EXPENSE_LINE_ITEMS_SHEET)
    if not data or len(data) < 2:
        print("  No expense line item data found")
        return 0

    rows = data[1:]
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mybillbook.expense_line_items")

    insert_sql = """
        INSERT INTO mybillbook.expense_line_items (
            expense_number, expense_date, expense_category, expense_category_id,
            expense_total, payment_mode, payment_type,
            expense_discount, expense_discount_type, round_off, place_of_supply,
            contact_name, contact_id,
            item_name, item_id, ledger_id,
            quantity, unit, unit_long, price_per_unit, rate, item_total_amount,
            item_discount, item_discount_type, gst_percentage,
            tax_included, tax_applicable, tax_exempted, itc_type,
            item_type, identification_code, notes, source
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    batch_data = []
    for row in rows:
        row = row + [""] * (33 - len(row)) if len(row) < 33 else row

        batch_data.append((
            row[0] or None,   # expense_number
            parse_date(row[1]),  # expense_date
            row[2] or None,   # expense_category
            row[3] or None,   # expense_category_id
            parse_float(row[4]),  # expense_total
            row[5] or None,   # payment_mode
            row[6] or None,   # payment_type
            parse_float(row[7]),  # expense_discount
            row[8] or None,   # expense_discount_type
            parse_float(row[9]),  # round_off
            row[10] or None,  # place_of_supply
            row[11] or None,  # contact_name
            row[12] or None,  # contact_id
            row[13] or None,  # item_name
            row[14] or None,  # item_id
            row[15] or None,  # ledger_id
            parse_float(row[16]),  # quantity
            row[17] or None,  # unit
            row[18] or None,  # unit_long
            parse_float(row[19]),  # price_per_unit
            parse_float(row[20]),  # rate
            parse_float(row[21]),  # item_total_amount
            parse_float(row[22]),  # item_discount
            row[23] or None,  # item_discount_type
            parse_float(row[24]),  # gst_percentage
            parse_bool(row[25]),  # tax_included
            parse_bool(row[26]),  # tax_applicable
            parse_bool(row[27]),  # tax_exempted
            row[28] or None,  # itc_type
            row[29] or None,  # item_type
            row[30] or None,  # identification_code
            row[31] or None,  # notes
            row[32] or None,  # source
        ))

    execute_batch(cursor, insert_sql, batch_data)
    conn.commit()

    print(f"  Synced {len(batch_data)} expense line items")
    return len(batch_data)


def main():
    """Main sync function"""
    print("\n" + "=" * 60)
    print("SYNC GOOGLE SHEETS TO POSTGRESQL")
    print("=" * 60)

    try:
        # Connect to Google Sheets
        print("\nConnecting to Google Sheets...")
        sheets = SheetsManager()
        print("[OK] Connected to Google Sheets")

        # Connect to PostgreSQL
        print("\nConnecting to PostgreSQL...")
        conn = get_db_connection()
        print("[OK] Connected to PostgreSQL")

        # Sync all data
        total_records = 0

        total_records += sync_contacts_from_invoices(conn, sheets)
        total_records += sync_products(conn, sheets)
        total_records += sync_sales_invoices(conn, sheets)
        total_records += sync_sales_invoice_line_items(conn, sheets)
        total_records += sync_expenses(conn, sheets)
        total_records += sync_expense_line_items(conn, sheets)

        print("\n" + "=" * 60)
        print(f"[SUCCESS] Synced {total_records} total records to PostgreSQL")
        print("=" * 60 + "\n")

        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"\n[ERROR] PostgreSQL Error: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
