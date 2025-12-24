from config import SHEET_INVENTORY, SHEET_WEPRINT
from utils.csv_exporter import export_sheet_data


def safe_float(value):
    """Safely convert a value to float, handling commas and empty values"""
    if not value:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    # Remove commas from string values like "6,000"
    return float(str(value).replace(',', ''))


def export_to_weprint(sheets_manager):
    """
    Export data to WePrint format for label printing

    Logic:
    - Reads from Inventory sheet
    - Creates rows: Product, Barcode, Price
    - Duplicates each row based on quantity (for printing multiple labels)
    """
    print("Starting WePrint export...")

    # Read inventory data
    data = sheets_manager.read_sheet(SHEET_INVENTORY)

    if not data:
        print("No data found in Inventory sheet")
        return

    rows = data[1:]

    print(f"Processing {len(rows)} inventory items...")

    # Headers
    headers = ["Product", "Barcode", "Price"]
    output = [headers]

    # Process each inventory row
    total_labels = 0
    skipped_items = 0
    for row in rows:
        # Ensure row has enough columns (now 10 columns: A-J)
        while len(row) < 10:
            row.append("")

        name = row[1]           # Column B - Name
        barcode = row[9]        # Column J - Inventory Item Barcode (index 9) - ACTUAL barcode to use
        price = row[4]          # Column E - Selling Price
        quantity = int(safe_float(row[3]))  # Column D - Quantity (handles commas like "6,000")

        # Skip items where name starts with "Charms 40" (bulk items, don't need individual labels)
        if name.startswith("Charms 40"):
            skipped_items += 1
            print(f"  SKIPPED: {name} (Charms 40 - bulk item, quantity: {quantity})")
            continue

        # Add quantity number of rows (for label printing)
        for _ in range(quantity):
            output.append([name, barcode, price])
            total_labels += 1

    # Write to WePrint sheet
    sheets_manager.clear_sheet(SHEET_WEPRINT)
    sheets_manager.write_sheet(SHEET_WEPRINT, output)

    # Format Barcode column (B) as plain text
    if len(output) > 1:
        sheets_manager.format_as_text(SHEET_WEPRINT, f"B2:B{len(output)}")

    print(f"[OK] WePrint data exported successfully! {total_labels} labels generated")
    if skipped_items > 0:
        print(f"     {skipped_items} items skipped (Charms 40 bulk items)")

    # Export to CSV if user wants
    print("\n" + "="*60)
    export_sheet_data(sheets_manager, SHEET_WEPRINT, "weprint", prompt_user=True)
    print("="*60)
