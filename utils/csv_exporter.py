"""
CSV Export Utility
Handles exporting Google Sheets data to CSV files with timestamps
"""

import os
import csv
from datetime import datetime
from pathlib import Path


# Base export directory
EXPORT_BASE_DIR = "csv_exports"

# Subdirectories for each export type
EXPORT_FOLDERS = {
    "inventory_raw": "inventory_raw",
    "inventory": "inventory",
    "mybillbook_inventory": "mybillbook_inventory",
    "mybillbook_add": "mybillbook_add",
    "mybillbook_update": "mybillbook_update",
    "weprint": "weprint",
    "mybillbook_inventory_BACKUP": "mybillbook_inventory_BACKUP"  # Safety backups
}


def create_export_folders():
    """Create the export folder structure if it doesn't exist"""
    base_path = Path(EXPORT_BASE_DIR)
    base_path.mkdir(exist_ok=True)

    for folder_name in EXPORT_FOLDERS.values():
        folder_path = base_path / folder_name
        folder_path.mkdir(exist_ok=True)

    print(f"[OK] Export folders created at: {base_path.absolute()}")


def generate_filename(export_type):
    """
    Generate a timestamped filename for CSV export

    Args:
        export_type: One of the keys in EXPORT_FOLDERS

    Returns:
        Full file path with timestamp
    """
    if export_type not in EXPORT_FOLDERS:
        raise ValueError(f"Invalid export type: {export_type}. Must be one of {list(EXPORT_FOLDERS.keys())}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{export_type}_{timestamp}.csv"

    folder = EXPORT_FOLDERS[export_type]
    filepath = Path(EXPORT_BASE_DIR) / folder / filename

    return filepath


def save_to_csv(data, export_type, prompt_user=True):
    """
    Save data to CSV file with timestamp

    Args:
        data: List of lists (rows) to save
        export_type: One of the keys in EXPORT_FOLDERS
        prompt_user: Whether to prompt user before saving (default: True)

    Returns:
        str: Path to saved file, or None if user declined
    """
    if not data:
        print(f"[WARN] No data to export for {export_type}")
        return None

    # Create folders if they don't exist
    create_export_folders()

    # Check if running from Streamlit UI with auto-export enabled
    auto_export = os.environ.get('STREAMLIT_AUTO_EXPORT') == 'true'

    # Prompt user if required (skip prompt if auto_export is enabled)
    if prompt_user and not auto_export:
        print(f"\n[EXPORT] {export_type}")
        response = input("   Save as CSV? (y/n): ").strip().lower()
        if response != 'y':
            print("   Skipped.")
            return None
    elif auto_export:
        print(f"\n[EXPORT] {export_type} (auto-export enabled)")

    # Generate filename
    filepath = generate_filename(export_type)

    # Save to CSV
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"   [OK] Saved: {filepath}")
        return str(filepath)

    except Exception as e:
        print(f"   [ERROR] Error saving CSV: {e}")
        return None


def export_sheet_data(sheets_manager, sheet_name, export_type, prompt_user=True):
    """
    Export Google Sheets data directly to CSV

    Args:
        sheets_manager: GoogleSheetsManager instance
        sheet_name: Name of the sheet to export
        export_type: One of the keys in EXPORT_FOLDERS
        prompt_user: Whether to prompt user before saving

    Returns:
        str: Path to saved file, or None if failed/declined
    """
    try:
        # Read data from sheet
        data = sheets_manager.read_sheet(sheet_name)

        if not data:
            print(f"[WARN] Sheet '{sheet_name}' is empty")
            return None

        # Save to CSV
        return save_to_csv(data, export_type, prompt_user)

    except Exception as e:
        print(f"[ERROR] Error exporting sheet '{sheet_name}': {e}")
        return None


def create_safety_backup(sheets_manager, sheet_name, backup_type="mybillbook_inventory_BACKUP"):
    """
    Create a SAFETY BACKUP before clearing data (automatic, no prompt)

    This is different from regular exports - it's a full safety backup
    created automatically before destructive operations.

    Args:
        sheets_manager: GoogleSheetsManager instance
        sheet_name: Name of the sheet to backup
        backup_type: Type of backup (default: mybillbook_inventory_BACKUP)

    Returns:
        str: Path to saved backup file, or None if failed/no data
    """
    import time

    # Retry logic for transient network/SSL errors
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            # Read data from sheet
            data = sheets_manager.read_sheet(sheet_name)

            if not data or len(data) <= 1:  # Only headers or empty
                print(f"   [INFO] No data to backup in '{sheet_name}' (sheet is empty)")
                return None

            print(f"\n{'='*60}")
            print(f"[SAFETY BACKUP] Creating backup before clearing '{sheet_name}'")
            print(f"{'='*60}")

            # Save without prompting
            filepath = save_to_csv(data, backup_type, prompt_user=False)

            if filepath:
                print(f"[OK] Safety backup created: {filepath}")
                print(f"{'='*60}\n")

            return filepath

        except Exception as e:
            error_msg = str(e)

            # Check if it's a transient SSL or network error
            is_transient = any(err in error_msg.lower() for err in [
                'ssl', 'connection', 'timeout', 'network', 'wrong_version_number'
            ])

            if is_transient and attempt < max_retries - 1:
                print(f"[WARN] Transient error on attempt {attempt + 1}/{max_retries}: {error_msg}")
                print(f"   Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
            else:
                # Final attempt failed or non-transient error
                print(f"\n{'='*60}")
                print(f"[ERROR] Safety backup failed after {attempt + 1} attempts")
                print(f"Error: {error_msg}")
                print(f"[WARN] Proceeding WITHOUT backup - data will be cleared!")
                print(f"{'='*60}\n")
                return None

    return None


def list_exports(export_type=None):
    """
    List all exported CSV files

    Args:
        export_type: Optional filter by export type

    Returns:
        List of file paths
    """
    base_path = Path(EXPORT_BASE_DIR)

    if not base_path.exists():
        return []

    if export_type:
        if export_type not in EXPORT_FOLDERS:
            raise ValueError(f"Invalid export type: {export_type}")
        folder = base_path / EXPORT_FOLDERS[export_type]
        return sorted(folder.glob("*.csv"), reverse=True)
    else:
        # List all CSVs across all folders
        all_files = []
        for folder_name in EXPORT_FOLDERS.values():
            folder = base_path / folder_name
            if folder.exists():
                all_files.extend(folder.glob("*.csv"))
        return sorted(all_files, reverse=True)
