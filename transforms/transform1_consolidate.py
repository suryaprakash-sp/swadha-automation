import random
import string
import re
from config import SHEET_RAW, SHEET_INVENTORY, SHEET_MYBILLBOOK_CURRENT


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


def extract_variant_from_mybillbook_name(mybillbook_name, category):
    """
    Extract variant from MyBillBook name by removing category and last 4 characters

    MyBillBook format: [Category] [Optional Variant] [4 CHARS]
    Examples:
    - "Ear Rings XCNR" → variant: "" (empty)
    - "Ear Rings SL ABCD" → variant: "SL"
    - "Traditional Ear Rings GL PWAW" → variant: "GL"

    Returns: variant string (could be empty)
    """
    # Remove category from the beginning (case-insensitive)
    name_without_category = mybillbook_name
    if mybillbook_name.lower().startswith(category.lower()):
        name_without_category = mybillbook_name[len(category):].strip()

    # Remove last 4 characters (random code) if length allows
    if len(name_without_category) >= 4:
        # Last 4 chars should be the random code (uppercase letters/numbers)
        last_4 = name_without_category[-4:]
        # Check if last 4 chars look like a code (all uppercase alphanumeric)
        if last_4.replace(' ', '').isupper() or last_4.replace(' ', '').isalnum():
            variant = name_without_category[:-4].strip()
            return variant

    return ""


def safe_float(value):
    """Safely convert to float, handling commas and empty values"""
    if not value:
        return 0.0
    try:
        return float(str(value).replace(',', ''))
    except (ValueError, AttributeError):
        return 0.0


def find_matching_mybillbook_item(category, raw_name, cost_price, selling_price, mybillbook_items):
    """
    Find matching item in MyBillBook inventory

    Matching criteria:
    1. Category matches
    2. Cost Price matches (purchase price)
    3. Selling Price matches
    4. Name matches: RAW name == variant extracted from MyBillBook name

    Returns: MyBillBook item dict if found, None otherwise
    """
    raw_name_clean = str(raw_name).strip() if raw_name else ""

    for mb_item in mybillbook_items:
        # Check category
        if mb_item['category'].lower() != category.lower():
            continue

        # Check cost price (within small tolerance for float comparison)
        if abs(safe_float(mb_item['purchase_price']) - safe_float(cost_price)) > 0.01:
            continue

        # Check selling price
        if abs(safe_float(mb_item['selling_price']) - safe_float(selling_price)) > 0.01:
            continue

        # Check name: extract variant from MyBillBook name and compare with RAW name
        variant = extract_variant_from_mybillbook_name(mb_item['name'], category)

        if variant.lower() == raw_name_clean.lower():
            # Match found!
            return mb_item

    return None




def consolidate_inventory(sheets_manager):
    """
    Main function to consolidate inventory from RAW sheet

    NEW Process:
    1. Read MyBillBook inventory (synced data)
    2. Read Inventory RAW sheet
    3. Consolidate rows by Type|Name|Cost Price|Selling Price (sum quantities)
    4. For each item, check if it exists in MyBillBook:
       - Match by: Category + Cost Price + Selling Price + Name variant
       - If FOUND: Use existing MyBillBook name & barcode, mark "Already Present" = Yes
       - If NOT found: Generate new name & barcode, mark "Already Present" = No
    5. Write to Inventory sheet with 2 new columns (I, J)
    """
    print("Starting inventory consolidation...")

    # Step 1: Read MyBillBook inventory
    mybillbook_data = sheets_manager.read_sheet(SHEET_MYBILLBOOK_CURRENT)
    mybillbook_items = []

    if mybillbook_data and len(mybillbook_data) > 1:
        mybillbook_rows = mybillbook_data[1:]
        print(f"Loaded {len(mybillbook_rows)} items from MyBillBook inventory")

        # Parse MyBillBook items
        for mb_row in mybillbook_rows:
            if len(mb_row) >= 8:  # Need ID, Name, SKU, Category, MRP, Selling, Sales, Purchase
                mybillbook_items.append({
                    'id': mb_row[0],
                    'name': mb_row[1],
                    'sku_code': mb_row[2],
                    'category': mb_row[3],
                    'selling_price': mb_row[5] if len(mb_row) > 5 else 0,  # Column F
                    'purchase_price': mb_row[7] if len(mb_row) > 7 else 0,  # Column H
                })
    else:
        print("Warning: No MyBillBook inventory found. All items will be treated as new.")

    # Step 2: Read raw data
    data = sheets_manager.read_sheet(SHEET_RAW)
    if not data:
        print("No data found in Inventory RAW sheet")
        return

    headers = data[0]
    rows = data[1:]

    print(f"Processing {len(rows)} rows from RAW sheet...")

    # Step 3: Consolidate by key: Type|Name|Cost Price|Selling Price
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

    # Step 4: Process each consolidated item
    output_headers = headers + ["Total Cost Price", "Total Selling Price", "Barcode", "Already Present", "Inventory Item Barcode"]
    output_rows = []
    barcodes = []
    already_present_flags = []
    inventory_item_barcodes = []

    matched_count = 0
    new_count = 0

    for row in consolidated.values():
        category = row[0]
        raw_name = row[1] if row[1] else ""
        cost_price = row[2]
        selling_price = row[4]

        # Try to find matching item in MyBillBook
        mb_match = find_matching_mybillbook_item(category, raw_name, cost_price, selling_price, mybillbook_items)

        if mb_match:
            # MATCH FOUND - Use existing MyBillBook item
            row[1] = mb_match['name']  # Use existing MyBillBook name
            barcode = generate_barcode(cost_price)  # Generate barcode for column H (for reference)
            already_present = "Yes"
            inventory_barcode = mb_match['sku_code']  # Use MyBillBook SKU as actual barcode
            matched_count += 1
            print(f"  MATCH: {mb_match['name']} (SKU: {inventory_barcode})")
        else:
            # NO MATCH - Generate new name and barcode
            original_name = raw_name.strip() if raw_name else ""
            if original_name:
                row[1] = generate_name_with_existing(category, original_name)
            else:
                row[1] = generate_name(category)

            barcode = generate_barcode(cost_price)
            already_present = "No"
            inventory_barcode = barcode  # Use generated barcode
            new_count += 1

        barcodes.append(barcode)
        already_present_flags.append(already_present)
        inventory_item_barcodes.append(inventory_barcode)

        # Keep only 5 columns: Type, Name, Cost, Qty, Sell
        output_rows.append(row[:5])

    print(f"  Matched with MyBillBook: {matched_count} items")
    print(f"  New items: {new_count} items")

    # Combine headers and rows
    output = [output_headers] + output_rows

    # Clear and write to Inventory sheet
    sheets_manager.clear_sheet(SHEET_INVENTORY)
    sheets_manager.write_sheet(SHEET_INVENTORY, output)

    # Add formulas and data columns
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

        # Column H: Barcodes (generated)
        barcode_data = [[barcode] for barcode in barcodes]
        sheets_manager.write_sheet(SHEET_INVENTORY, barcode_data, 'H2')

        # Column I: Already Present (Yes/No)
        already_present_data = [[flag] for flag in already_present_flags]
        sheets_manager.write_sheet(SHEET_INVENTORY, already_present_data, 'I2')

        # Column J: Inventory Item Barcode (actual barcode to use)
        inventory_barcode_data = [[barcode] for barcode in inventory_item_barcodes]
        sheets_manager.write_sheet(SHEET_INVENTORY, inventory_barcode_data, 'J2')

    # Apply column formatting
    if len(output_rows) > 0:
        last_row = len(output_rows) + 1

        # Text columns
        sheets_manager.format_as_text(SHEET_INVENTORY, f"A2:A{last_row}")  # Type
        sheets_manager.format_as_text(SHEET_INVENTORY, f"B2:B{last_row}")  # Name
        sheets_manager.format_as_text(SHEET_INVENTORY, f"H2:H{last_row}")  # Barcode (generated)
        sheets_manager.format_as_text(SHEET_INVENTORY, f"I2:I{last_row}")  # Already Present
        sheets_manager.format_as_text(SHEET_INVENTORY, f"J2:J{last_row}")  # Inventory Item Barcode

        # Numeric columns
        sheets_manager.format_as_number(SHEET_INVENTORY, f"C2:C{last_row}", decimal_places=2)  # Per Item CP
        sheets_manager.format_as_number(SHEET_INVENTORY, f"D2:D{last_row}", decimal_places=0)  # Quantity
        sheets_manager.format_as_number(SHEET_INVENTORY, f"E2:E{last_row}", decimal_places=2)  # Per Item SP
        sheets_manager.format_as_number(SHEET_INVENTORY, f"F2:F{last_row}", decimal_places=2)  # Total CP
        sheets_manager.format_as_number(SHEET_INVENTORY, f"G2:G{last_row}", decimal_places=2)  # Total SP

    print(f"[OK] Inventory consolidated successfully! {len(output_rows)} items processed")
