#!/usr/bin/env python3
"""
Swadha Automation - Web UI
Streamlit-based web interface for inventory automation
"""

import streamlit as st
import pandas as pd
import sys
import traceback
from pathlib import Path
from datetime import datetime

# Import automation modules
from utils.sheets import SheetsManager
from transforms.transform1_consolidate import consolidate_inventory
from transforms.transform2_mybillbook import export_to_mybillbook
from mybillbook.sync import sync_to_sheets
from utils.csv_exporter import list_exports, EXPORT_FOLDERS
from config import SHEET_MYBILLBOOK_CURRENT, SHEET_WEPRINT


# Page config
st.set_page_config(
    page_title="Swadha Automation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: 600;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'sheets_manager' not in st.session_state:
    st.session_state.sheets_manager = None
if 'last_operation' not in st.session_state:
    st.session_state.last_operation = None
if 'operation_status' not in st.session_state:
    st.session_state.operation_status = None
if 'auto_export_csv' not in st.session_state:
    st.session_state.auto_export_csv = True  # Default to auto-export
if 'running_operation' not in st.session_state:
    st.session_state.running_operation = False


def init_sheets_manager():
    """Initialize Google Sheets connection"""
    if st.session_state.sheets_manager is None:
        try:
            with st.spinner("Connecting to Google Sheets..."):
                st.session_state.sheets_manager = SheetsManager()
            st.success("✅ Connected to Google Sheets!")
            return True
        except Exception as e:
            st.error(f"❌ Failed to connect to Google Sheets: {str(e)}")
            st.info("Please ensure credentials.json is in the project directory.")
            return False
    return True


def main_operations_page():
    """Main operations page - Sync, Transform 1, Transform 2"""
    st.title("📊 Main Operations")
    st.markdown("---")

    if not init_sheets_manager():
        return

    sheets = st.session_state.sheets_manager

    # CSV Export Settings
    st.sidebar.markdown("### ⚙️ Settings")
    st.session_state.auto_export_csv = st.sidebar.checkbox(
        "Auto-export to CSV",
        value=st.session_state.auto_export_csv,
        help="Automatically export data to CSV files after transformations (no prompts)"
    )

    # Monkeypatch the export functions to respect the auto_export setting
    import os
    if st.session_state.auto_export_csv:
        os.environ['STREAMLIT_AUTO_EXPORT'] = 'true'
    else:
        os.environ.pop('STREAMLIT_AUTO_EXPORT', None)

    # Only show individual operations if not currently running "Run All"
    if not st.session_state.running_operation:
        # Create columns for operations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔄 Step 0: Sync MyBillBook")
            st.write("Fetch latest inventory from MyBillBook API")
            if st.button("🔄 Sync MyBillBook Inventory", key="sync_btn"):
                try:
                    with st.spinner("Syncing MyBillBook inventory..."):
                        # Capture output
                        import io
                        from contextlib import redirect_stdout

                        f = io.StringIO()
                        with redirect_stdout(f):
                            result = sync_to_sheets(sheets)

                        output = f.getvalue()

                        if result:
                            st.success("✅ MyBillBook inventory synced successfully!")
                            with st.expander("View Details"):
                                st.code(output)
                        else:
                            st.error("❌ Sync failed. Check details below.")
                            with st.expander("Error Details"):
                                st.code(output)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    with st.expander("Error Traceback"):
                        st.code(traceback.format_exc())

            st.markdown("---")

            st.subheader("🔀 Step 1: Consolidate Inventory")
            st.write("Smart matching & consolidation")
            if st.button("🔀 Run Transform 1", key="transform1_btn"):
                try:
                    with st.spinner("Consolidating inventory..."):
                        import io
                        from contextlib import redirect_stdout

                        f = io.StringIO()
                        with redirect_stdout(f):
                            consolidate_inventory(sheets)

                        output = f.getvalue()
                        st.success("✅ Inventory consolidated successfully!")
                        with st.expander("View Details"):
                            st.code(output)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    with st.expander("Error Traceback"):
                        st.code(traceback.format_exc())

        with col2:
            st.subheader("📤 Step 2: MyBillBook Export")
            st.write("Generate ADD/UPDATE sheets for import")
            if st.button("📤 Run Transform 2", key="transform2_btn"):
                try:
                    with st.spinner("Generating MyBillBook import data..."):
                        import io
                        from contextlib import redirect_stdout

                        f = io.StringIO()
                        with redirect_stdout(f):
                            export_to_mybillbook(sheets)

                        output = f.getvalue()
                        st.success("✅ MyBillBook data exported successfully!")
                        with st.expander("View Details"):
                            st.code(output)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    with st.expander("Error Traceback"):
                        st.code(traceback.format_exc())

            st.markdown("---")

            st.subheader("⚡ Run All Operations")
            st.write("Execute all steps in sequence")
            if st.button("⚡ Run All (Steps 0-2)", key="run_all_btn", type="primary"):
                st.session_state.running_operation = True
                st.rerun()

    # Run All Operations execution (shown separately when running)
    if st.session_state.running_operation:
        st.subheader("⚡ Running All Operations")
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Step 0
            status_text.text("Step 1/3: Syncing MyBillBook...")
            progress_bar.progress(10)
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                sync_to_sheets(sheets)
            progress_bar.progress(33)

            # Step 1
            status_text.text("Step 2/3: Consolidating inventory...")
            f = io.StringIO()
            with redirect_stdout(f):
                consolidate_inventory(sheets)
            progress_bar.progress(66)

            # Step 2
            status_text.text("Step 3/3: Generating MyBillBook data...")
            f = io.StringIO()
            with redirect_stdout(f):
                export_to_mybillbook(sheets)
            progress_bar.progress(100)

            status_text.text("✅ All operations completed!")
            st.success("🎉 All operations completed successfully!")
            st.balloons()

            # Reset flag
            st.session_state.running_operation = False

            # Add button to go back
            if st.button("↩️ Back to Operations", key="back_btn"):
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error during operations: {str(e)}")
            with st.expander("Error Traceback"):
                st.code(traceback.format_exc())

            # Reset flag on error
            st.session_state.running_operation = False

            if st.button("↩️ Back to Operations", key="back_btn_error"):
                st.rerun()


def label_generator_page():
    """Label generator page - Standalone WePrint generator"""
    st.title("🏷️ Label Generator")
    st.markdown("---")

    if not init_sheets_manager():
        return

    sheets = st.session_state.sheets_manager

    st.info("📌 Generate labels from MyBillBook inventory. Select items and specify how many labels you need.")

    # Read MyBillBook inventory
    try:
        with st.spinner("Loading MyBillBook inventory..."):
            data = sheets.read_sheet(SHEET_MYBILLBOOK_CURRENT)

            if not data or len(data) <= 1:
                st.warning("⚠️ MyBillBook inventory is empty! Please run 'Sync MyBillBook' first.")
                return

            headers = data[0]
            rows = data[1:]

            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Show item count
            st.success(f"✅ Loaded {len(df)} items from MyBillBook inventory")

            # Search/Filter
            st.subheader("🔍 Search & Filter")
            search_term = st.text_input("Search by product name:", "")

            if search_term:
                filtered_df = df[df['Name'].str.contains(search_term, case=False, na=False)]
                st.write(f"Found {len(filtered_df)} items matching '{search_term}'")
            else:
                filtered_df = df

            # Display items with selection
            st.subheader("📦 Select Items for Labels")

            # Show dataframe with selection
            display_cols = ['Name', 'SKU Code', 'Quantity', 'Selling Price', 'Category']
            available_cols = [col for col in display_cols if col in filtered_df.columns]

            st.dataframe(filtered_df[available_cols], use_container_width=True, height=400)

            # Label count input
            st.subheader("🎯 Generate Labels")

            col1, col2 = st.columns([3, 1])

            with col1:
                label_method = st.radio(
                    "How do you want to specify labels?",
                    ["Manual entry (enter counts for each item)", "Use current MyBillBook quantities"],
                    key="label_method"
                )

            with col2:
                if st.button("🏷️ Generate Labels", type="primary"):
                    try:
                        # Generate labels based on method
                        headers_out = ["Product", "Barcode", "Price"]
                        output = [headers_out]
                        total_labels = 0

                        if label_method == "Use current MyBillBook quantities":
                            # Use quantities from MyBillBook
                            for _, row in filtered_df.iterrows():
                                name = row.get('Name', '')
                                sku = row.get('SKU Code', '')
                                price = row.get('Selling Price', '')
                                qty = int(float(row.get('Quantity', 0)))

                                for _ in range(qty):
                                    output.append([name, sku, price])
                                    total_labels += 1

                        # Write to WePrint sheet
                        with st.spinner("Writing labels to WePrint sheet..."):
                            sheets.clear_sheet(SHEET_WEPRINT)
                            sheets.write_sheet(SHEET_WEPRINT, output)

                            if len(output) > 1:
                                sheets.format_as_text(SHEET_WEPRINT, f"B2:B{len(output)}")

                        st.success(f"✅ Generated {total_labels} labels in WePrint sheet!")
                        st.info("💡 Go to 'CSV Exports' page to download the labels as CSV")

                    except Exception as e:
                        st.error(f"❌ Error generating labels: {str(e)}")
                        with st.expander("Error Traceback"):
                            st.code(traceback.format_exc())

            # Manual entry section
            if label_method == "Manual entry (enter counts for each item)":
                st.markdown("---")
                st.subheader("✏️ Manual Label Counts")
                st.write("Enter the number of labels needed for each item:")

                label_counts = {}

                for idx, row in filtered_df.iterrows():
                    name = row.get('Name', '')
                    sku = row.get('SKU Code', '')
                    current_qty = row.get('Quantity', 0)

                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    with col_a:
                        st.write(f"**{name}**")
                        st.caption(f"SKU: {sku} | Current Qty: {current_qty}")
                    with col_b:
                        count = st.number_input(
                            "Labels",
                            min_value=0,
                            value=0,
                            step=1,
                            key=f"label_count_{idx}",
                            label_visibility="collapsed"
                        )
                        label_counts[idx] = count

                if st.button("Generate with Manual Counts", type="primary", key="manual_generate"):
                    try:
                        headers_out = ["Product", "Barcode", "Price"]
                        output = [headers_out]
                        total_labels = 0

                        for idx, count in label_counts.items():
                            if count > 0:
                                row = filtered_df.iloc[idx]
                                name = row.get('Name', '')
                                sku = row.get('SKU Code', '')
                                price = row.get('Selling Price', '')

                                for _ in range(count):
                                    output.append([name, sku, price])
                                    total_labels += 1

                        if total_labels == 0:
                            st.warning("⚠️ No labels to generate. Please enter counts for at least one item.")
                        else:
                            with st.spinner("Writing labels to WePrint sheet..."):
                                sheets.clear_sheet(SHEET_WEPRINT)
                                sheets.write_sheet(SHEET_WEPRINT, output)

                                if len(output) > 1:
                                    sheets.format_as_text(SHEET_WEPRINT, f"B2:B{len(output)}")

                            st.success(f"✅ Generated {total_labels} labels in WePrint sheet!")
                            st.info("💡 Go to 'CSV Exports' page to download the labels as CSV")

                    except Exception as e:
                        st.error(f"❌ Error generating labels: {str(e)}")
                        with st.expander("Error Traceback"):
                            st.code(traceback.format_exc())

    except Exception as e:
        st.error(f"❌ Error loading inventory: {str(e)}")
        with st.expander("Error Traceback"):
            st.code(traceback.format_exc())


def csv_exports_page():
    """CSV exports page - View and download exports"""
    st.title("📥 CSV Exports")
    st.markdown("---")

    st.info("📌 View and download your timestamped CSV exports")

    # Export type selector
    export_type = st.selectbox(
        "Select export type:",
        ["All Exports"] + list(EXPORT_FOLDERS.keys())
    )

    try:
        # List exports
        if export_type == "All Exports":
            files = list_exports()
        else:
            files = list_exports(export_type)

        if not files:
            st.warning(f"⚠️ No exports found for '{export_type}'")
            return

        st.success(f"✅ Found {len(files)} export files")

        # Group by folder
        exports_by_folder = {}
        for file_path in files:
            folder_name = file_path.parent.name
            if folder_name not in exports_by_folder:
                exports_by_folder[folder_name] = []
            exports_by_folder[folder_name].append(file_path)

        # Display by folder
        for folder_name, folder_files in exports_by_folder.items():
            with st.expander(f"📁 {folder_name} ({len(folder_files)} files)", expanded=True):
                for file_path in sorted(folder_files, reverse=True)[:10]:  # Show latest 10
                    col1, col2, col3 = st.columns([3, 1, 1])

                    with col1:
                        st.write(f"**{file_path.name}**")
                        # File size and modified time
                        file_size = file_path.stat().st_size
                        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        st.caption(f"Size: {file_size:,} bytes | Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")

                    with col2:
                        # Preview button
                        if st.button("👁️ Preview", key=f"preview_{file_path}"):
                            try:
                                df = pd.read_csv(file_path)
                                st.dataframe(df.head(20), use_container_width=True)
                            except Exception as e:
                                st.error(f"Error reading file: {str(e)}")

                    with col3:
                        # Download button
                        with open(file_path, 'rb') as f:
                            st.download_button(
                                "⬇️ Download",
                                data=f,
                                file_name=file_path.name,
                                mime="text/csv",
                                key=f"download_{file_path}"
                            )

    except Exception as e:
        st.error(f"❌ Error listing exports: {str(e)}")
        with st.expander("Error Traceback"):
            st.code(traceback.format_exc())


def about_page():
    """About page - Info and status"""
    st.title("ℹ️ About")
    st.markdown("---")

    st.markdown("""
    ## Swadha Automation

    **Version:** 1.0.0
    **Description:** Inventory management automation using Google Sheets

    ### Features

    ✅ **MyBillBook Sync** - Fetch latest inventory from MyBillBook API
    ✅ **Smart Consolidation** - Automatic matching with 4-criteria algorithm
    ✅ **MyBillBook Export** - Generate ADD/UPDATE sheets for bulk import
    ✅ **Label Generator** - Flexible label printing from MyBillBook inventory
    ✅ **CSV Exports** - Timestamped backups with automatic safety backups

    ### How to Use

    1. **Main Operations** - Run sync and transformations
    2. **Label Generator** - Generate labels for printing
    3. **CSV Exports** - Download your exported data

    ### Documentation

    📖 See the `docs/` folder for detailed guides

    ---

    ### System Status
    """)

    # System status
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Google Sheets", "Connected" if st.session_state.sheets_manager else "Not Connected")

    with col2:
        # Check if csv_exports folder exists
        csv_folder = Path("csv_exports")
        if csv_folder.exists():
            file_count = sum(1 for _ in csv_folder.rglob("*.csv"))
            st.metric("CSV Exports", f"{file_count} files")
        else:
            st.metric("CSV Exports", "0 files")

    with col3:
        st.metric("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def main():
    """Main app function"""

    # Sidebar
    st.sidebar.title("📊 Swadha Automation")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Main Operations", "🏷️ Label Generator", "📥 CSV Exports", "ℹ️ About"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")

    if st.session_state.sheets_manager:
        st.sidebar.success("✅ Google Sheets Connected")
    else:
        st.sidebar.warning("⚠️ Not Connected")

    # Route to pages
    if page == "🏠 Main Operations":
        main_operations_page()
    elif page == "🏷️ Label Generator":
        label_generator_page()
    elif page == "📥 CSV Exports":
        csv_exports_page()
    elif page == "ℹ️ About":
        about_page()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("Built with ❤️ using Streamlit")


if __name__ == "__main__":
    main()
