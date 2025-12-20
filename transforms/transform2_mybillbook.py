from config import SHEET_RAW, SHEET_INVENTORY, SHEET_MYBILLBOOK_ADD, SHEET_MYBILLBOOK_UPDATE, SHEET_MYBILLBOOK_CURRENT


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

    NEW Logic (uses synced MyBillBook inventory):
    - Reads consolidated "Inventory" sheet (69 items)
    - Reads synced "myBillBook Inventory" sheet (352 items from MyBillBook API)
    - For each inventory item, check if it exists in MyBillBook by matching SKU Code (barcode)
    - If found in MyBillBook → UPDATE tab (update existing item)
    - If not found → ADD tab (new item to add)
    """
    print("Starting MyBillBook export...")

    # Read inventory and MyBillBook current data
    inventory_data = sheets_manager.read_sheet(SHEET_INVENTORY)
    mybillbook_data = sheets_manager.read_sheet(SHEET_MYBILLBOOK_CURRENT)

    if not inventory_data:
        print("Missing required data in Inventory sheet")
        return

    inventory_rows = inventory_data[1:]
    print(f"Processing {len(inventory_rows)} inventory items...")

    # Build lookup dictionary for MyBillBook items by SKU Code (barcode)
    mybillbook_items = {}
    if mybillbook_data and len(mybillbook_data) > 1:
        mybillbook_rows = mybillbook_data[1:]
        print(f"Checking against {len(mybillbook_rows)} existing MyBillBook items...")

        for mb_row in mybillbook_rows:
            if len(mb_row) > 2:  # Need at least ID, Name, SKU Code
                sku_code = str(mb_row[2]).strip() if mb_row[2] else ""  # Column C: SKU Code
                if sku_code:
                    mybillbook_items[sku_code] = {
                        'id': mb_row[0] if len(mb_row) > 0 else "",
                        'name': mb_row[1] if len(mb_row) > 1 else "",
                        'sku_code': sku_code,
                        'quantity': safe_float(mb_row[7]) if len(mb_row) > 7 else 0,  # Column H: Quantity
                    }
    else:
        print("Warning: No MyBillBook inventory data found. All items will go to ADD tab.")

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
        # Ensure row has enough columns (now 8 columns: A-H)
        while len(inv_row) < 8:
            inv_row.append("")

        # Get barcode from inventory (Column H, index 7)
        barcode = str(inv_row[7]).strip() if inv_row[7] else ""

        # Check if this item exists in MyBillBook (by SKU Code/barcode)
        if barcode and barcode in mybillbook_items:
            # Item EXISTS in MyBillBook → UPDATE tab
            mb_item = mybillbook_items[barcode]

            # Calculate new stock: MyBillBook current stock + new inventory quantity
            mybillbook_stock = mb_item['quantity']
            new_inventory_stock = safe_float(inv_row[3])  # Column D: Quantity
            total_stock = mybillbook_stock + new_inventory_stock

            output_update.append([
                mb_item['name'],      # Item Name (use existing MyBillBook name)
                "",                   # Description
                inv_row[0],           # Category (Type from Column A)
                barcode,              # Item code (Barcode)
                "",                   # HSN Code
                "",                   # GST Tax Rate(%)
                inv_row[4],           # Sales Price (Column E)
                "Inclusive",          # Sales Tax inclusive
                inv_row[2],           # Purchase Price (Column C)
                "Inclusive",          # Purchase Tax inclusive
                inv_row[4],           # MRP (same as Sales Price)
                total_stock,          # Current stock (MyBillBook stock + new stock)
                0,                    # Low stock alert quantity
                "No"                  # Visible on Online Store?
            ])
            update_count += 1
            print(f"  UPDATE: {mb_item['name']} (SKU: {barcode}) - Stock: {mybillbook_stock} + {new_inventory_stock} = {total_stock}")

        else:
            # Item does NOT exist in MyBillBook → ADD tab
            output_add.append([
                inv_row[1],           # Item Name (from consolidated inventory)
                "",                   # Description
                inv_row[0],           # Category
                "PIECES",             # Unit
                "",                   # Alternate Unit
                "",                   # Conversion Rate
                barcode,              # Item code (Barcode)
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
