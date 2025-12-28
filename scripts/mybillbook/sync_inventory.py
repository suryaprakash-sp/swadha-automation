#!/usr/bin/env python3
"""
Standalone Inventory Sync Script
Syncs MyBillBook inventory to Google Sheets
"""

import sys
from pathlib import Path

# Add project root to path (two levels up: scripts/mybillbook -> scripts -> root)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.sheets import SheetsManager
from mybillbook.sync import sync_to_sheets


def main():
    """Main function to sync inventory"""
    print("\n" + "="*60)
    print("MYBILLBOOK INVENTORY SYNC")
    print("="*60 + "\n")

    try:
        # Initialize Google Sheets connection
        print("Connecting to Google Sheets...")
        sheets = SheetsManager()
        print("[OK] Connected to Google Sheets!\n")

        # Run sync
        success = sync_to_sheets(sheets)

        if success:
            print("\n" + "="*60)
            print("[SUCCESS] Inventory sync completed!")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("[FAILED] Inventory sync failed!")
            print("="*60 + "\n")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nPlease ensure you have:")
        print("1. Created credentials.json from Google Cloud Console")
        print("2. Placed it in the project directory")
        print("\nSee README.md for setup instructions.")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
