import random
import string
from config import SHEET_RAW, SHEET_INVENTORY


def generate_name(category):
    """Generate name with category and 4 random uppercase letters"""
    random_chars = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"{category} {random_chars}"


def generate_name_with_existing(category, existing_name):
    """Generate name with category, existing name, and 4 random uppercase letters"""
    random_chars = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"{category} {existing_name} {random_chars}"


def generate_barcode(cost_price):
    """
    Generate barcode with format: [2-digit prefix 13-99] [reversed price + random suffix]
    Total length after prefix: 4 digits
    """
    # First 2 digits should be between 13-99
    prefix = random.randint(13, 99)

    # Convert cost price to string and reverse it
    price_str = str(cost_price)
    reversed_price = price_str[::-1]
    price_len = len(reversed_price)

    # Calculate suffix length (total 4 digits after prefix)
    suffix_len = 4 - price_len

    # Generate random suffix
    suffix = ''.join(random.choices(string.digits, k=suffix_len))

    return f"{prefix} {reversed_price}{suffix}"




def consolidate_inventory(sheets_manager):
    """
    Main function to consolidate inventory from RAW sheet

    Process:
    1. Read Inventory RAW sheet
    2. Consolidate rows by Type|Name|Cost Price|Selling Price (sum quantities)
    3. Generate names and barcodes
    4. Write to Inventory sheet with formulas
    """
    print("Starting inventory consolidation...")

    # Read raw data
    data = sheets_manager.read_sheet(SHEET_RAW)
    if not data:
        print("No data found in Inventory RAW sheet")
        return

    headers = data[0]
    rows = data[1:]

    print(f"Processing {len(rows)} rows from RAW sheet...")

    # Consolidate by key: Type|Name|Cost Price|Selling Price
    consolidated = {}

    for row in rows:
        # Ensure row has exactly 5 columns (A-E)
        while len(row) < 5:
            row.append("")
        # Keep only first 5 columns
        row = row[:5]

        # Create key from columns A, B, C, E (indices 0, 1, 2, 4)
        # Type | Name | Cost Price | Selling Price
        key = f"{row[0]}|{row[1]}|{row[2]}|{row[4]}"

        if key in consolidated:
            # Sum quantity (column D, index 3)
            consolidated[key][3] = float(consolidated[key][3] or 0) + float(row[3] or 0)
        else:
            consolidated[key] = list(row)

    print(f"Consolidated into {len(consolidated)} unique items")

    # Prepare output with headers (add columns for F, G, H)
    output_headers = headers + ["Total Cost Price", "Total Selling Price", "Barcode"]
    output_rows = []
    barcodes = []

    for row in consolidated.values():
        # Generate name: Type + Original Name + Random 4 letters
        original_name = row[1] if row[1] and str(row[1]).strip() else ""
        if original_name:
            row[1] = generate_name_with_existing(row[0], original_name)
        else:
            row[1] = generate_name(row[0])

        # Generate barcode based on cost price
        barcode = generate_barcode(row[2])
        barcodes.append(barcode)

        # Keep only 5 columns: Type, Name, Cost, Qty, Sell
        output_rows.append(row[:5])

    # Combine headers and rows
    output = [output_headers] + output_rows

    # Clear and write to Inventory sheet (only columns A-E and header for F)
    sheets_manager.clear_sheet(SHEET_INVENTORY)
    sheets_manager.write_sheet(SHEET_INVENTORY, output)

    # Add formulas for columns F and G, and barcodes to H
    if len(output_rows) > 0:
        num_rows = len(output_rows)

        # Column F: =C*D (Cost Price * Quantity)
        formulas_f = []
        for i in range(2, num_rows + 2):
            formulas_f.append([f"=C{i}*D{i}"])
        sheets_manager.write_formulas(SHEET_INVENTORY, formulas_f, 'F2')

        # Column G: =D*E (Quantity * Selling Price)
        formulas_g = []
        for i in range(2, num_rows + 2):
            formulas_g.append([f"=D{i}*E{i}"])
        sheets_manager.write_formulas(SHEET_INVENTORY, formulas_g, 'G2')

        # Column H: Barcodes
        barcode_data = [[barcode] for barcode in barcodes]
        sheets_manager.write_sheet(SHEET_INVENTORY, barcode_data, 'H2')

    # Apply column formatting
    if len(output_rows) > 0:
        last_row = len(output_rows) + 1

        # Text columns
        sheets_manager.format_as_text(SHEET_INVENTORY, f"A2:A{last_row}")  # Type
        sheets_manager.format_as_text(SHEET_INVENTORY, f"B2:B{last_row}")  # Name
        sheets_manager.format_as_text(SHEET_INVENTORY, f"H2:H{last_row}")  # Barcode

        # Numeric columns
        sheets_manager.format_as_number(SHEET_INVENTORY, f"C2:C{last_row}", decimal_places=2)  # Per Item CP
        sheets_manager.format_as_number(SHEET_INVENTORY, f"D2:D{last_row}", decimal_places=0)  # Quantity
        sheets_manager.format_as_number(SHEET_INVENTORY, f"E2:E{last_row}", decimal_places=2)  # Per Item SP
        sheets_manager.format_as_number(SHEET_INVENTORY, f"F2:F{last_row}", decimal_places=2)  # Total CP
        sheets_manager.format_as_number(SHEET_INVENTORY, f"G2:G{last_row}", decimal_places=2)  # Total SP

    print(f"[OK] Inventory consolidated successfully! {len(output_rows)} items processed")
