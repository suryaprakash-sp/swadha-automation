from config import SHEET_INVENTORY, SHEET_WEPRINT


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
    for row in rows:
        # Ensure row has enough columns (now 8 columns: A-H)
        while len(row) < 8:
            row.append("")

        name = row[1]           # Column B - Name
        barcode = row[7]        # Column H - Barcode (index 7)
        price = row[4]          # Column E - Selling Price
        quantity = int(float(row[3]) if row[3] else 0)  # Column D - Quantity

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
