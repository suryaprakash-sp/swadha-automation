from config import SHEET_RAW, SHEET_INVENTORY, SHEET_MYBILLBOOK_ADD, SHEET_MYBILLBOOK_UPDATE, SHEET_MYBILLBOOK_CURRENT
from utils.csv_exporter import export_sheet_data


def safe_float(value):
    """
    Safely convert a value to float, handling comma-separated thousands
    e.g., "1,199" -> 1199.0
    """
    if not value:
        return 0.0
    try:
        # Remove commas and convert to float
        return float(str(value).replace(',', ''))
    except (ValueError, AttributeError):
        return 0.0


def export_to_mybillbook(sheets_manager):
    """
    Export data to MyBillBook format (ADD and UPDATE sheets)

    NEW Logic (uses Transform 1 matching):
    - Reads consolidated "Inventory" sheet with new columns:
      - Column I: "Already Present" (Yes/No)
      - Column J: "Inventory Item Barcode" (actual barcode to use)
    - If "Already Present" = Yes → UPDATE tab
    - If "Already Present" = No → ADD tab
    """
    print("Starting MyBillBook export...")

    # Read inventory data
    inventory_data = sheets_manager.read_sheet(SHEET_INVENTORY)

    if not inventory_data:
        print("Missing required data in Inventory sheet")
        return

    inventory_rows = inventory_data[1:]
    print(f"Processing {len(inventory_rows)} inventory items...")

    # Headers for ADD tab
    headers_add = [
        "Item Name*\n(mandatory field)",
        "Description",
        "Category",
        "Unit",
        "Alternate Unit",
        "Conversion Rate",
        "Item code",
        "HSN Code",
        "GST Tax Rate(%)",
        "Sales Price",
        "Sales Tax inclusive",
        "Purchase Price",
        "Purchase Tax inclusive",
        "MRP",
        "Current stock",
        "Low stock alert quantity",
        "Item type",
        "Visible on Online Store?"
    ]

    # Headers for UPDATE tab
    headers_update = [
        "Item Name*\n(mandatory field)",
        "Description",
        "Category",
        "Item code",
        "HSN Code",
        "GST Tax Rate(%)",
        "Sales Price",
        "Sales Tax inclusive",
        "Purchase Price",
        "Purchase Tax inclusive",
        "MRP",
        "Current stock",
        "Low stock alert quantity",
        "Visible on Online Store?"
    ]

    output_add = [headers_add]
    output_update = [headers_update]

    add_count = 0
    update_count = 0

    # Process each inventory row
    for inv_row in inventory_rows:
        # Ensure row has enough columns (now 10 columns: A-J)
        while len(inv_row) < 10:
            inv_row.append("")

        # Get flags from new columns
        already_present = str(inv_row[8]).strip() if len(inv_row) > 8 and inv_row[8] else "No"  # Column I
        inventory_barcode = str(inv_row[9]).strip() if len(inv_row) > 9 and inv_row[9] else ""  # Column J

        # Check if item already exists in MyBillBook
        if already_present.lower() == "yes":
            # Item EXISTS in MyBillBook → UPDATE tab
            output_update.append([
                inv_row[1],           # Item Name (existing MyBillBook name)
                "",                   # Description
                inv_row[0],           # Category (Type from Column A)
                inventory_barcode,    # Item code (Barcode from Column J)
                "",                   # HSN Code
                "",                   # GST Tax Rate(%)
                inv_row[4],           # Sales Price (Column E)
                "Inclusive",          # Sales Tax inclusive
                inv_row[2],           # Purchase Price (Column C)
                "Inclusive",          # Purchase Tax inclusive
                inv_row[4],           # MRP (same as Sales Price)
                inv_row[3],           # Current stock (just use new quantity)
                0,                    # Low stock alert quantity
                "No"                  # Visible on Online Store?
            ])
            update_count += 1
            print(f"  UPDATE: {inv_row[1]} (SKU: {inventory_barcode})")

        else:
            # Item does NOT exist in MyBillBook → ADD tab
            output_add.append([
                inv_row[1],           # Item Name (from consolidated inventory)
                "",                   # Description
                inv_row[0],           # Category
                "PIECES",             # Unit
                "",                   # Alternate Unit
                "",                   # Conversion Rate
                inventory_barcode,    # Item code (Barcode from Column J)
                "",                   # HSN Code
                "",                   # GST Tax Rate(%)
                inv_row[4],           # Sales Price
                "Inclusive",          # Sales Tax inclusive
                inv_row[2],           # Purchase Price
                "Inclusive",          # Purchase Tax inclusive
                inv_row[4],           # MRP
                inv_row[3],           # Current stock
                0,                    # Low stock alert quantity
                "Product",            # Item type
                "No"                  # Visible on Online Store?
            ])
            add_count += 1

    # Write to ADD sheet
    sheets_manager.clear_sheet(SHEET_MYBILLBOOK_ADD)
    sheets_manager.write_sheet(SHEET_MYBILLBOOK_ADD, output_add)

    # Format Item code column (G) as plain text in ADD sheet
    if len(output_add) > 1:
        sheets_manager.format_as_text(SHEET_MYBILLBOOK_ADD, f"G2:G{len(output_add)}")

    # Write to UPDATE sheet
    sheets_manager.clear_sheet(SHEET_MYBILLBOOK_UPDATE)
    sheets_manager.write_sheet(SHEET_MYBILLBOOK_UPDATE, output_update)

    # Format Item code column (D) as plain text in UPDATE sheet
    if len(output_update) > 1:
        sheets_manager.format_as_text(SHEET_MYBILLBOOK_UPDATE, f"D2:D{len(output_update)}")

    print(f"\n[OK] MyBillBook data exported successfully!")
    print(f"  ADD sheet: {add_count} items (new items not in MyBillBook)")
    print(f"  UPDATE sheet: {update_count} items (existing items in MyBillBook)")
    print(f"  Total processed: {len(inventory_rows)} items")

    # Export to CSV if user wants
    print("\n" + "="*60)
    export_sheet_data(sheets_manager, SHEET_MYBILLBOOK_ADD, "mybillbook_add", prompt_user=True)
    export_sheet_data(sheets_manager, SHEET_MYBILLBOOK_UPDATE, "mybillbook_update", prompt_user=True)
    print("="*60)
