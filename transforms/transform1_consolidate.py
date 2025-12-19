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


def find_existing_name(rows, category, item_code):
    """
    Search through raw data for matching category and item code
    Returns name from column B or F
    """
    for row in rows:
        if row[0] == category and row[2] == item_code:
            # First check column B (index 1)
            if len(row) > 1 and row[1] and str(row[1]).strip():
                return str(row[1])
            # Then check column F (index 5)
            if len(row) > 5 and row[5] and str(row[5]).strip():
                return str(row[5])
    return None


def find_existing_barcode(rows, category, item_code):
    """
    Search through raw data for matching category and item code
    Returns barcode from column G
    """
    for row in rows:
        if row[0] == category and row[2] == item_code:
            # Check column G (index 6)
            if len(row) > 6 and row[6] and str(row[6]).strip():
                return str(row[6])
    return None


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
        # Ensure row has enough columns
        while len(row) < 8:
            row.append("")

        # Create key from columns A, B, C, E (indices 0, 1, 2, 4)
        key = f"{row[0]}|{row[1]}|{row[2]}|{row[4]}"

        if key in consolidated:
            # Sum quantity (column D, index 3)
            consolidated[key][3] = float(consolidated[key][3] or 0) + float(row[3] or 0)
        else:
            consolidated[key] = list(row)

    print(f"Consolidated into {len(consolidated)} unique items")

    # Prepare output
    output = [headers]

    for row in consolidated.values():
        # Generate name based on existing data
        existing_name = find_existing_name(rows, row[0], row[2])
        if existing_name:
            # If name exists in raw, format as: Category + Name + Random
            row[1] = generate_name_with_existing(row[0], existing_name)
        else:
            # If no name in raw, generate as: Category + Random
            row[1] = generate_name(row[0])

        # Check for existing barcode before generating
        existing_barcode = find_existing_barcode(rows, row[0], row[2])
        if existing_barcode:
            barcode = existing_barcode
        else:
            barcode = generate_barcode(row[2])

        # Append barcode to row
        row.append(barcode)

        output.append(row)

    # Add Barcode column to headers
    output[0].append("Barcode")

    # Clear and write to Inventory sheet
    sheets_manager.clear_sheet(SHEET_INVENTORY)
    sheets_manager.write_sheet(SHEET_INVENTORY, output)

    # Format Item Code column (C) and Barcode column (I) as plain text
    if len(output) > 1:
        # Column C (Item Code) - assuming column I is barcode (index 8)
        sheets_manager.format_as_text(SHEET_INVENTORY, f"C2:C{len(output)}")
        sheets_manager.format_as_text(SHEET_INVENTORY, f"I2:I{len(output)}")

    # Add formulas for columns F and G
    if len(output) > 1:
        # Column F: =C*D (Cost Price * Quantity)
        formulas_f = []
        for i in range(2, len(output) + 1):
            formulas_f.append([f"=C{i}*D{i}"])

        sheets_manager.write_formulas(SHEET_INVENTORY, formulas_f, 'F2')

        # Column G: =D*E (Quantity * Selling Price)
        formulas_g = []
        for i in range(2, len(output) + 1):
            formulas_g.append([f"=D{i}*E{i}"])

        sheets_manager.write_formulas(SHEET_INVENTORY, formulas_g, 'G2')

    print(f"[OK] Inventory consolidated successfully! {len(output) - 1} items processed")
