#!/usr/bin/env python3
"""
WePrint Label Generator (Standalone)

Generates labels from MyBillBook inventory for printing.
Reads from actual MyBillBook inventory and lets you select which items need labels.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.sheets import SheetsManager
from utils.csv_exporter import export_sheet_data
from config import SHEET_MYBILLBOOK_CURRENT, SHEET_WEPRINT


def print_items(items):
    """Print inventory items in a numbered list"""
    print("\n" + "="*80)
    print("MYBILLBOOK INVENTORY ITEMS")
    print("="*80)
    print(f"{'#':<5} {'Name':<40} {'SKU':<15} {'Qty':<10}")
    print("-"*80)

    for idx, item in enumerate(items, 1):
        name = item['name'][:38]  # Truncate long names
        sku = item['sku']
        qty = item['quantity']
        print(f"{idx:<5} {name:<40} {sku:<15} {qty:<10}")

    print("="*80)


def select_items_for_labels(items):
    """Let user select which items need labels"""
    print("\n" + "="*80)
    print("SELECT ITEMS FOR LABEL PRINTING")
    print("="*80)
    print("\nOptions:")
    print("1. Select specific items by number (comma-separated)")
    print("2. Search by name")
    print("3. Print labels for ALL items")
    print("4. Cancel")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == '1':
        # Select by number
        numbers = input("\nEnter item numbers (comma-separated, e.g., 1,5,12): ").strip()
        try:
            indices = [int(n.strip()) - 1 for n in numbers.split(',')]
            selected = [items[i] for i in indices if 0 <= i < len(items)]
            return selected
        except (ValueError, IndexError):
            print("[ERROR] Invalid item numbers!")
            return []

    elif choice == '2':
        # Search by name
        search = input("\nEnter search term: ").strip().lower()
        selected = [item for item in items if search in item['name'].lower()]
        if not selected:
            print(f"[WARN] No items found matching '{search}'")
        else:
            print(f"\nFound {len(selected)} items:")
            for item in selected:
                print(f"  - {item['name']} (SKU: {item['sku']})")
        return selected

    elif choice == '3':
        # All items
        confirm = input(f"\nPrint labels for ALL {len(items)} items? (y/n): ").strip().lower()
        if confirm == 'y':
            return items
        return []

    else:
        return []


def get_label_count(item):
    """Ask user how many labels needed for an item"""
    print(f"\nItem: {item['name']}")
    print(f"SKU: {item['sku']}")
    print(f"Current Quantity in MyBillBook: {item['quantity']}")

    while True:
        count = input(f"How many labels to print? (0 to skip): ").strip()
        try:
            count = int(count)
            if count >= 0:
                return count
            print("[ERROR] Please enter a non-negative number")
        except ValueError:
            print("[ERROR] Please enter a valid number")


def generate_weprint_labels(sheets_manager):
    """Main function to generate WePrint labels"""
    print("\n" + "="*80)
    print("WEPRINT LABEL GENERATOR")
    print("="*80)
    print("\nReading MyBillBook inventory...")

    # Read MyBillBook inventory
    data = sheets_manager.read_sheet(SHEET_MYBILLBOOK_CURRENT)

    if not data or len(data) <= 1:
        print("[ERROR] MyBillBook inventory is empty!")
        print("Please run 'Sync MyBillBook Inventory' first (Menu Option 0 in main.py)")
        return

    headers = data[0]
    rows = data[1:]

    # Find column indices
    try:
        name_idx = headers.index("Name")
        sku_idx = headers.index("SKU Code")
        qty_idx = headers.index("Quantity")
        price_idx = headers.index("Selling Price")
    except ValueError as e:
        print(f"[ERROR] Missing required column: {e}")
        return

    # Parse items
    items = []
    for row in rows:
        if len(row) > max(name_idx, sku_idx, qty_idx, price_idx):
            items.append({
                'name': row[name_idx],
                'sku': row[sku_idx],
                'quantity': row[qty_idx],
                'price': row[price_idx]
            })

    print(f"Loaded {len(items)} items from MyBillBook inventory")

    # Show items
    print_items(items)

    # Select items
    selected_items = select_items_for_labels(items)

    if not selected_items:
        print("\n[INFO] No items selected. Exiting...")
        return

    print(f"\n{len(selected_items)} items selected for label printing")

    # Get label counts for each item
    label_data = []
    for item in selected_items:
        count = get_label_count(item)
        if count > 0:
            label_data.append({
                'item': item,
                'count': count
            })

    if not label_data:
        print("\n[INFO] No labels to generate. Exiting...")
        return

    # Generate WePrint sheet
    print("\n" + "="*80)
    print("GENERATING WEPRINT LABELS")
    print("="*80)

    headers = ["Product", "Barcode", "Price"]
    output = [headers]

    total_labels = 0
    for data_item in label_data:
        item = data_item['item']
        count = data_item['count']

        # Add 'count' number of label rows
        for _ in range(count):
            output.append([item['name'], item['sku'], item['price']])
            total_labels += 1

        print(f"  {item['name']}: {count} labels")

    # Write to WePrint sheet
    print(f"\nWriting {total_labels} labels to WePrint sheet...")
    sheets_manager.clear_sheet(SHEET_WEPRINT)
    sheets_manager.write_sheet(SHEET_WEPRINT, output)

    # Format Barcode column as text
    if len(output) > 1:
        sheets_manager.format_as_text(SHEET_WEPRINT, f"B2:B{len(output)}")

    print(f"\n[OK] WePrint labels generated successfully! {total_labels} labels total")

    # Export to CSV
    print("\n" + "="*80)
    export_sheet_data(sheets_manager, SHEET_WEPRINT, "weprint", prompt_user=True)
    print("="*80)

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Download the WePrint sheet as CSV")
    print("2. Import to your label printer software")
    print("3. Print the labels")
    print("="*80)


def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("WEPRINT LABEL GENERATOR - STANDALONE")
    print("="*80)

    try:
        # Initialize Google Sheets
        print("\nConnecting to Google Sheets...")
        sheets = SheetsManager()
        print("[OK] Connected successfully!\n")

        # Generate labels
        generate_weprint_labels(sheets)

    except FileNotFoundError as e:
        print(f"\n[ERROR] Error: {str(e)}")
        print("\nPlease ensure you have:")
        print("1. Created credentials.json from Google Cloud Console")
        print("2. Placed it in the project directory")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
