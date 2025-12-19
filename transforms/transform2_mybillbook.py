from config import SHEET_RAW, SHEET_INVENTORY, SHEET_MYBILLBOOK_ADD, SHEET_MYBILLBOOK_UPDATE


def export_to_mybillbook(sheets_manager):
    """
    Export data to MyBillBook format (ADD and UPDATE sheets)

    Logic:
    - If raw row has data in column F (Already Present Name), goes to UPDATE tab
    - Otherwise goes to ADD tab
    - UPDATE tab: Current stock = Column H + Column D
    - ADD tab: Uses consolidated inventory data
    """
    print("Starting MyBillBook export...")

    # Read raw and inventory data
    raw_data = sheets_manager.read_sheet(SHEET_RAW)
    inventory_data = sheets_manager.read_sheet(SHEET_INVENTORY)

    if not raw_data or not inventory_data:
        print("Missing required data in RAW or Inventory sheets")
        return

    raw_rows = raw_data[1:]
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

    # Process each inventory row
    for inv_row in inventory_rows:
        # Ensure row has enough columns
        while len(inv_row) < 9:
            inv_row.append("")

        # Match raw rows based on Type (Category), Cost Price, and Selling Price
        matching_raw_rows = []
        for raw_row in raw_rows:
            while len(raw_row) < 8:
                raw_row.append("")

            # Compare: Type (col A), Cost Price (col C), Selling Price (col E)
            if (raw_row[0] == inv_row[0] and
                float(raw_row[2] or 0) == float(inv_row[2] or 0) and
                float(raw_row[4] or 0) == float(inv_row[4] or 0)):
                matching_raw_rows.append(raw_row)

        # Check if any matching raw row has data in column F (index 5)
        has_column_f_data = any(
            len(row) > 5 and row[5] and str(row[5]).strip()
            for row in matching_raw_rows
        )

        if has_column_f_data:
            # Goes to UPDATE tab
            raw_row = next(
                (r for r in matching_raw_rows if len(r) > 5 and r[5] and str(r[5]).strip()),
                None
            )

            if raw_row:
                # Calculate current stock: Column H (index 7) + Column D (index 3)
                old_stock = float(raw_row[7] if len(raw_row) > 7 and raw_row[7] else 0)
                new_stock = float(raw_row[3] if len(raw_row) > 3 and raw_row[3] else 0)
                current_stock = old_stock + new_stock

                output_update.append([
                    raw_row[5],           # Item Name from Column F (Already Present Name)
                    "",                   # Description
                    raw_row[0],           # Category (Type from Column A)
                    inv_row[8],           # Item code (Barcode from inventory Column I)
                    "",                   # HSN Code
                    "",                   # GST Tax Rate(%)
                    raw_row[4],           # Sales Price (Column E)
                    "Inclusive",          # Sales Tax inclusive
                    raw_row[2],           # Purchase Price (Column C)
                    "Inclusive",          # Purchase Tax inclusive
                    raw_row[4],           # MRP (same as Sales Price)
                    current_stock,        # Current stock (H + D)
                    1,                    # Low stock alert quantity
                    "No"                  # Visible on Online Store?
                ])
        else:
            # Goes to ADD tab
            output_add.append([
                inv_row[1],           # Item Name (from consolidated inventory)
                "",                   # Description
                inv_row[0],           # Category
                "PIECES",             # Unit
                "",                   # Alternate Unit
                "",                   # Conversion Rate
                inv_row[8],           # Item code (Barcode from inventory Column I)
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

    print(f"✓ MyBillBook data exported successfully!")
    print(f"  ADD sheet: {len(output_add) - 1} items")
    print(f"  UPDATE sheet: {len(output_update) - 1} items")
