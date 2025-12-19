#!/usr/bin/env python3
"""
Swadha Automation - Inventory Data Transformation Pipeline

Main script to run inventory transformations for Google Sheets.
"""

import sys
from utils.sheets import SheetsManager
from transforms.transform1_consolidate import consolidate_inventory
from transforms.transform2_mybillbook import export_to_mybillbook
from transforms.transform3_weprint import export_to_weprint


def print_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("SWADHA AUTOMATION - INVENTORY TOOLS")
    print("="*50)
    print("1. Consolidate Inventory (Transform 1)")
    print("2. MyBillBook Data Import (Transform 2)")
    print("3. WePrint Export (Transform 3)")
    print("4. Run All Operations")
    print("5. Exit")
    print("="*50)


def main():
    """Main function to run the inventory automation"""
    print("\nInitializing Swadha Automation...")
    print("Connecting to Google Sheets...")

    try:
        # Initialize Google Sheets connection
        sheets = SheetsManager()
        print("[OK] Successfully connected to Google Sheets!\n")

        while True:
            print_menu()
            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == '1':
                print("\n" + "-"*50)
                print("Running Transform 1: Consolidate Inventory")
                print("-"*50)
                consolidate_inventory(sheets)

            elif choice == '2':
                print("\n" + "-"*50)
                print("Running Transform 2: MyBillBook Data Import")
                print("-"*50)
                export_to_mybillbook(sheets)

            elif choice == '3':
                print("\n" + "-"*50)
                print("Running Transform 3: WePrint Export")
                print("-"*50)
                export_to_weprint(sheets)

            elif choice == '4':
                print("\n" + "-"*50)
                print("Running All Operations")
                print("-"*50)
                try:
                    consolidate_inventory(sheets)
                    print()
                    export_to_mybillbook(sheets)
                    print()
                    export_to_weprint(sheets)
                    print("\n" + "="*50)
                    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
                    print("="*50)
                    print("[OK] Inventory consolidated")
                    print("[OK] MyBillBook data exported")
                    print("[OK] WePrint data exported")
                    print("="*50)
                except Exception as e:
                    print(f"\n[ERROR] Error during operations: {str(e)}")

            elif choice == '5':
                print("\nExiting... Goodbye!")
                sys.exit(0)

            else:
                print("\n[ERROR] Invalid choice. Please enter 1-5.")

            input("\nPress Enter to continue...")

    except FileNotFoundError as e:
        print(f"\n[ERROR] Error: {str(e)}")
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
