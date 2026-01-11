#!/usr/bin/env python3
"""
Swadha Automation - Premium Inventory Management Interface
"""

import streamlit as st
import pandas as pd
import sys
import traceback
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import automation modules
from utils.sheets import SheetsManager
from transforms.transform1_consolidate import consolidate_inventory
from transforms.transform2_mybillbook import export_to_mybillbook
from mybillbook.sync import sync_to_sheets
from utils.csv_exporter import list_exports, EXPORT_FOLDERS
from config import SHEET_MYBILLBOOK_CURRENT, SHEET_WEPRINT


# Page config
st.set_page_config(
    page_title="Swadha",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Unique Design System - Warm Industrial
st.markdown("""
<style>
    /* Import Fonts - DM Sans for body, Space Grotesk for headings */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Design Tokens */
    :root {
        --bg-primary: #faf9f7;
        --bg-secondary: #f0eeeb;
        --bg-card: #ffffff;
        --bg-dark: #1c1c1c;
        --bg-dark-hover: #2a2a2a;

        --text-primary: #1c1c1c;
        --text-secondary: #6b6b6b;
        --text-muted: #9a9a9a;
        --text-inverse: #faf9f7;

        --accent: #c9a227;
        --accent-hover: #b8922a;
        --accent-subtle: #f5f0e1;

        --success: #2d8a5f;
        --success-bg: #e8f5ef;
        --warning: #c9a227;
        --warning-bg: #fdf8e8;
        --error: #c44536;
        --error-bg: #fce8e6;

        --border: #e5e3df;
        --border-strong: #d1cfc9;

        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 14px;

        --shadow-sm: 0 1px 2px rgba(28,28,28,0.04);
        --shadow-md: 0 2px 8px rgba(28,28,28,0.06);
        --shadow-lg: 0 4px 16px rgba(28,28,28,0.08);

        --font-body: 'DM Sans', -apple-system, sans-serif;
        --font-heading: 'Space Grotesk', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* Global Reset */
    .stApp {
        background: var(--bg-primary);
        font-family: var(--font-body);
    }

    /* Hide Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Sidebar - Dark elegant */
    [data-testid="stSidebar"] {
        background: var(--bg-dark);
        border-right: none;
        padding-top: 0;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: var(--text-inverse) !important;
    }

    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-muted) !important;
    }

    /* Main content */
    .main .block-container {
        padding: 2.5rem 3rem;
        max-width: 1200px;
    }

    /* Typography */
    h1 {
        font-family: var(--font-heading) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        font-family: var(--font-heading) !important;
        font-weight: 600 !important;
        font-size: 1.35rem !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.01em !important;
    }

    h3 {
        font-family: var(--font-heading) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: var(--text-primary) !important;
    }

    p, span, div {
        font-family: var(--font-body);
    }

    /* Navigation Buttons */
    .nav-btn {
        display: block;
        width: 100%;
        padding: 14px 18px;
        margin: 4px 0;
        background: transparent;
        border: none;
        border-radius: var(--radius-md);
        color: rgba(255,255,255,0.7);
        font-family: var(--font-body);
        font-size: 0.95rem;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.15s ease;
        text-decoration: none;
    }

    .nav-btn:hover {
        background: var(--bg-dark-hover);
        color: #fff;
    }

    .nav-btn.active {
        background: var(--accent);
        color: var(--bg-dark);
        font-weight: 600;
    }

    .nav-icon {
        display: inline-block;
        width: 20px;
        margin-right: 12px;
        text-align: center;
    }

    /* Cards */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }

    .card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--border-strong);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }

    .card-icon {
        width: 44px;
        height: 44px;
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        background: var(--bg-secondary);
    }

    .card-icon.sync { background: #e3f2fd; }
    .card-icon.transform { background: #fce4ec; }
    .card-icon.export { background: #e8f5e9; }
    .card-icon.primary { background: var(--accent-subtle); }

    .card-title {
        font-family: var(--font-heading);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }

    .card-subtitle {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0;
    }

    .card-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
    }

    /* Metric Cards */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 20px 24px;
        text-align: left;
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
    }

    .metric-value {
        font-family: var(--font-heading);
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    .metric-value.accent {
        color: var(--accent);
    }

    /* Streamlit Metrics Override */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        padding: 20px 24px;
        border-radius: var(--radius-md);
        border: 1px solid var(--border);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    [data-testid="stMetricValue"] {
        font-family: var(--font-heading) !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
    }

    /* Buttons */
    .stButton > button {
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 12px 24px !important;
        border-radius: var(--radius-md) !important;
        border: none !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--bg-dark) !important;
        color: var(--text-inverse) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #333 !important;
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .stButton > button[kind="secondary"] {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-strong) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--bg-secondary) !important;
        border-color: var(--text-muted) !important;
    }

    /* Primary Action Button */
    .primary-action > button {
        background: var(--accent) !important;
        color: var(--bg-dark) !important;
        font-weight: 600 !important;
        padding: 16px 32px !important;
        font-size: 0.95rem !important;
    }

    .primary-action > button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(201, 162, 39, 0.3);
    }

    /* Status Indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .status-connected {
        background: var(--success-bg);
        color: var(--success);
    }

    .status-disconnected {
        background: var(--error-bg);
        color: var(--error);
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
    }

    /* Section Header */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border);
    }

    .section-title {
        font-family: var(--font-heading);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }

    /* Page Header */
    .page-header {
        margin-bottom: 32px;
    }

    .page-title {
        font-family: var(--font-heading);
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 4px 0;
        letter-spacing: -0.02em;
    }

    .page-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        margin: 0;
    }

    /* Brand */
    .brand {
        padding: 28px 24px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 8px;
    }

    .brand-name {
        font-family: var(--font-heading);
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .brand-tagline {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.4);
        margin-top: 2px;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: var(--border);
        margin: 24px 0;
    }

    .divider-dark {
        background: rgba(255,255,255,0.08);
        margin: 16px 24px;
    }

    /* Pipeline visual */
    .pipeline-step {
        display: flex;
        align-items: center;
        padding: 12px 0;
        color: rgba(255,255,255,0.6);
        font-size: 0.85rem;
    }

    .pipeline-num {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 12px;
        font-family: var(--font-mono);
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border) !important;
        overflow: hidden !important;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        font-family: var(--font-body) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border) !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-subtle) !important;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        border-radius: var(--radius-md) !important;
        border-color: var(--border) !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        font-family: var(--font-body) !important;
        font-weight: 500 !important;
        background: var(--bg-secondary) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Success/Error messages */
    .stSuccess {
        background: var(--success-bg) !important;
        border: 1px solid #b8dcc9 !important;
        border-radius: var(--radius-md) !important;
        color: var(--success) !important;
    }

    .stError {
        background: var(--error-bg) !important;
        border: 1px solid #f5c6c0 !important;
        border-radius: var(--radius-md) !important;
        color: var(--error) !important;
    }

    .stWarning {
        background: var(--warning-bg) !important;
        border: 1px solid #f0e2b3 !important;
        border-radius: var(--radius-md) !important;
        color: #8a7119 !important;
    }

    .stInfo {
        background: #f0f7ff !important;
        border: 1px solid #b3d4ff !important;
        border-radius: var(--radius-md) !important;
        color: #1a5fa8 !important;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: var(--accent) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* Sidebar footer */
    .sidebar-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 20px 24px;
        border-top: 1px solid rgba(255,255,255,0.08);
        font-size: 0.75rem;
        color: rgba(255,255,255,0.3);
    }

    /* Code/mono text */
    code {
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
        background: var(--bg-secondary) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-strong);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }

    /* Download button */
    .stDownloadButton > button {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        font-weight: 500 !important;
    }

    .stDownloadButton > button:hover {
        background: var(--bg-secondary) !important;
        border-color: var(--border-strong) !important;
    }

    /* Checkbox */
    .stCheckbox {
        padding: 8px 0;
    }

    .stCheckbox label {
        font-size: 0.9rem !important;
        color: rgba(255,255,255,0.7) !important;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: var(--text-muted);
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 16px;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'sheets_manager' not in st.session_state:
    st.session_state.sheets_manager = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'auto_export_csv' not in st.session_state:
    st.session_state.auto_export_csv = True


def init_sheets_manager():
    """Initialize Google Sheets connection"""
    if st.session_state.sheets_manager is None:
        try:
            st.session_state.sheets_manager = SheetsManager()
            return True
        except Exception as e:
            st.error(f"Failed to connect: {str(e)}")
            return False
    return True


def render_sidebar():
    """Render sidebar with proper navigation"""
    with st.sidebar:
        # Brand
        st.markdown("""
        <div class="brand">
            <div class="brand-name">Swadha</div>
            <div class="brand-tagline">Inventory Automation</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation using actual buttons
        st.markdown('<div style="padding: 8px 16px;">', unsafe_allow_html=True)

        pages = [
            ("Dashboard", "◈"),
            ("Labels", "▣"),
            ("Exports", "↓"),
            ("Settings", "⚙")
        ]

        for page_name, icon in pages:
            is_active = st.session_state.current_page == page_name
            if st.button(
                f"{icon}  {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page_name
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Divider
        st.markdown('<div class="divider-dark"></div>', unsafe_allow_html=True)

        # Status
        st.markdown('<div style="padding: 0 24px;">', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.4); margin-bottom: 12px;">Status</p>', unsafe_allow_html=True)

        if st.session_state.sheets_manager:
            st.markdown("""
            <div class="status-badge status-connected">
                <span class="status-dot"></span>
                Connected
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-badge status-disconnected">
                <span class="status-dot"></span>
                Disconnected
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Settings toggle
        st.markdown('<div class="divider-dark"></div>', unsafe_allow_html=True)
        st.markdown('<div style="padding: 0 24px;">', unsafe_allow_html=True)

        import os
        auto_export = st.checkbox("Auto-save CSV", value=st.session_state.auto_export_csv)
        st.session_state.auto_export_csv = auto_export
        if auto_export:
            os.environ['STREAMLIT_AUTO_EXPORT'] = 'true'
        else:
            os.environ.pop('STREAMLIT_AUTO_EXPORT', None)

        st.markdown('</div>', unsafe_allow_html=True)


def dashboard_page():
    """Dashboard - Main operations hub"""

    # Page header
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Manage your inventory sync operations</p>
    </div>
    """, unsafe_allow_html=True)

    if not init_sheets_manager():
        return

    sheets = st.session_state.sheets_manager

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        try:
            data = sheets.read_sheet(SHEET_MYBILLBOOK_CURRENT)
            item_count = len(data) - 1 if data else 0
        except:
            item_count = 0
        st.metric("Items", f"{item_count:,}")

    with col2:
        csv_folder = Path(__file__).parent.parent / "csv_exports"
        file_count = sum(1 for _ in csv_folder.rglob("*.csv")) if csv_folder.exists() else 0
        st.metric("Exports", f"{file_count}")

    with col3:
        status = "Online" if st.session_state.sheets_manager else "Offline"
        st.metric("Status", status)

    with col4:
        st.metric("Auto-Save", "On" if st.session_state.auto_export_csv else "Off")

    st.markdown("<div style='height: 32px'></div>", unsafe_allow_html=True)

    # Run All Section
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Quick Actions</h2>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_info = st.columns([2, 1])

    with col_main:
        st.markdown("""
        <div class="card" style="border-color: var(--accent); border-width: 2px;">
            <div class="card-header">
                <div class="card-icon primary">◈</div>
                <div>
                    <p class="card-subtitle">Recommended</p>
                    <h3 class="card-title">Run Complete Pipeline</h3>
                </div>
            </div>
            <p class="card-desc">Execute the full sync workflow: fetch inventory from MyBillBook, consolidate items, and generate export files.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="primary-action">', unsafe_allow_html=True)
        if st.button("Run All Operations", key="run_all", type="primary", use_container_width=True):
            run_all_operations(sheets)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div style="background: var(--bg-secondary); border-radius: var(--radius-md); padding: 20px; height: 100%;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 16px;">Pipeline Steps</p>
            <div class="pipeline-step" style="color: var(--text-secondary);">
                <span class="pipeline-num" style="background: var(--border);">1</span>
                Sync inventory
            </div>
            <div class="pipeline-step" style="color: var(--text-secondary);">
                <span class="pipeline-num" style="background: var(--border);">2</span>
                Consolidate items
            </div>
            <div class="pipeline-step" style="color: var(--text-secondary);">
                <span class="pipeline-num" style="background: var(--border);">3</span>
                Generate exports
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

    # Individual Operations
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Individual Operations</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <div class="card-icon sync">↻</div>
                <div>
                    <p class="card-subtitle">Step 1</p>
                    <h3 class="card-title">Sync Inventory</h3>
                </div>
            </div>
            <p class="card-desc">Fetch latest data from MyBillBook API and update Google Sheet.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        if st.button("Sync Now", key="sync_btn", use_container_width=True):
            run_sync_operation(sheets)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <div class="card-icon transform">⇄</div>
                <div>
                    <p class="card-subtitle">Step 2</p>
                    <h3 class="card-title">Consolidate</h3>
                </div>
            </div>
            <p class="card-desc">Smart matching to merge duplicates and reconcile inventory.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        if st.button("Consolidate", key="transform1_btn", use_container_width=True):
            run_consolidate_operation(sheets)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <div class="card-icon export">↗</div>
                <div>
                    <p class="card-subtitle">Step 3</p>
                    <h3 class="card-title">Export Data</h3>
                </div>
            </div>
            <p class="card-desc">Generate ADD and UPDATE sheets for MyBillBook import.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        if st.button("Export", key="transform2_btn", use_container_width=True):
            run_export_operation(sheets)


def run_sync_operation(sheets):
    """Run sync with status"""
    with st.status("Syncing inventory...", expanded=True) as status:
        try:
            import io
            from contextlib import redirect_stdout

            st.write("Connecting to MyBillBook API...")
            f = io.StringIO()
            with redirect_stdout(f):
                result = sync_to_sheets(sheets)
            output = f.getvalue()

            if result:
                status.update(label="Sync complete", state="complete", expanded=False)
                st.success("Inventory synced successfully")
                with st.expander("View details"):
                    st.code(output, language="text")
            else:
                status.update(label="Sync failed", state="error")
                st.error("Sync failed")
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Error: {str(e)}")


def run_consolidate_operation(sheets):
    """Run consolidation"""
    with st.status("Consolidating...", expanded=True) as status:
        try:
            import io
            from contextlib import redirect_stdout

            st.write("Running smart matching...")
            f = io.StringIO()
            with redirect_stdout(f):
                consolidate_inventory(sheets)
            output = f.getvalue()

            status.update(label="Consolidation complete", state="complete", expanded=False)
            st.success("Inventory consolidated")
            with st.expander("View details"):
                st.code(output, language="text")
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Error: {str(e)}")


def run_export_operation(sheets):
    """Run export"""
    with st.status("Exporting...", expanded=True) as status:
        try:
            import io
            from contextlib import redirect_stdout

            st.write("Generating export files...")
            f = io.StringIO()
            with redirect_stdout(f):
                export_to_mybillbook(sheets)
            output = f.getvalue()

            status.update(label="Export complete", state="complete", expanded=False)
            st.success("Export files generated")
            with st.expander("View details"):
                st.code(output, language="text")
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Error: {str(e)}")


def run_all_operations(sheets):
    """Run complete pipeline"""
    progress = st.progress(0)
    status_text = st.empty()

    try:
        import io
        from contextlib import redirect_stdout

        # Step 1
        status_text.markdown("**Step 1/3** — Syncing inventory...")
        progress.progress(10)
        f = io.StringIO()
        with redirect_stdout(f):
            sync_to_sheets(sheets)
        progress.progress(33)

        # Step 2
        status_text.markdown("**Step 2/3** — Consolidating items...")
        f = io.StringIO()
        with redirect_stdout(f):
            consolidate_inventory(sheets)
        progress.progress(66)

        # Step 3
        status_text.markdown("**Step 3/3** — Generating exports...")
        f = io.StringIO()
        with redirect_stdout(f):
            export_to_mybillbook(sheets)
        progress.progress(100)

        status_text.markdown("**Complete** — All operations finished successfully")
        st.success("Pipeline completed. Your inventory is synced and exports are ready.")
        st.balloons()

    except Exception as e:
        status_text.markdown("**Error** — Operation failed")
        st.error(f"Error: {str(e)}")


def labels_page():
    """Label Generator page"""

    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Label Generator</h1>
        <p class="page-subtitle">Create product labels from inventory</p>
    </div>
    """, unsafe_allow_html=True)

    if not init_sheets_manager():
        return

    sheets = st.session_state.sheets_manager

    try:
        with st.spinner("Loading inventory..."):
            data = sheets.read_sheet(SHEET_MYBILLBOOK_CURRENT)

        if not data or len(data) <= 1:
            st.warning("Inventory is empty. Run sync first.")
            return

        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)

        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", f"{len(df):,}")
        with col2:
            total_qty = df['Quantity'].apply(lambda x: int(float(str(x).replace(',', ''))) if x else 0).sum()
            st.metric("Total Qty", f"{total_qty:,}")
        with col3:
            categories = df['Category'].nunique() if 'Category' in df.columns else 0
            st.metric("Categories", f"{categories}")

        st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)

        # Search
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">Search & Filter</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("Search", placeholder="Type product name...", label_visibility="collapsed")
        with col2:
            if 'Category' in df.columns:
                cats = ['All'] + sorted(df['Category'].dropna().unique().tolist())
                cat = st.selectbox("Category", cats, label_visibility="collapsed")
            else:
                cat = 'All'

        # Filter
        filtered = df.copy()
        if search:
            filtered = filtered[filtered['Name'].str.contains(search, case=False, na=False)]
        if cat != 'All':
            filtered = filtered[filtered['Category'] == cat]

        st.caption(f"Showing {len(filtered)} items")

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        # Table
        display_cols = ['Name', 'SKU Code', 'Quantity', 'Selling Price', 'Category']
        available_cols = [c for c in display_cols if c in filtered.columns]

        st.dataframe(
            filtered[available_cols],
            use_container_width=True,
            height=300,
            column_config={
                "Name": st.column_config.TextColumn("Product", width="large"),
                "SKU Code": st.column_config.TextColumn("SKU", width="small"),
                "Quantity": st.column_config.NumberColumn("Qty", width="small"),
                "Selling Price": st.column_config.NumberColumn("Price", format="₹%.2f"),
                "Category": st.column_config.TextColumn("Category"),
            }
        )

        st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)

        # Generate section
        st.markdown("""
        <div class="section-header">
            <h2 class="section-title">Generate Labels</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            method = st.radio(
                "Method",
                ["Use current quantities", "Manual entry"],
                horizontal=True,
                label_visibility="collapsed"
            )

        with col2:
            generate = st.button("Generate Labels", type="primary", use_container_width=True)

        if generate and method == "Use current quantities":
            with st.status("Generating labels...", expanded=True) as status:
                try:
                    output = [["Product", "Barcode", "Price"]]
                    total = 0

                    for _, row in filtered.iterrows():
                        name = row.get('Name', '')
                        sku = row.get('SKU Code', '')
                        price = row.get('Selling Price', '')
                        qty_str = str(row.get('Quantity', 0)).replace(',', '')
                        qty = int(float(qty_str)) if qty_str else 0

                        for _ in range(qty):
                            output.append([name, sku, price])
                            total += 1

                    sheets.clear_sheet(SHEET_WEPRINT)
                    sheets.write_sheet(SHEET_WEPRINT, output)

                    if len(output) > 1:
                        sheets.format_as_text(SHEET_WEPRINT, f"B2:B{len(output)}")

                    status.update(label="Labels generated", state="complete")
                    st.success(f"Generated {total:,} labels")

                except Exception as e:
                    status.update(label="Error", state="error")
                    st.error(f"Error: {str(e)}")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def exports_page():
    """CSV Exports page"""

    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Exports</h1>
        <p class="page-subtitle">Download your exported data files</p>
    </div>
    """, unsafe_allow_html=True)

    if 'preview_file' not in st.session_state:
        st.session_state.preview_file = None

    try:
        files = list_exports()

        if not files:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">↓</div>
                <p>No exports yet</p>
                <p style="font-size: 0.85rem;">Run operations to generate CSV files</p>
            </div>
            """, unsafe_allow_html=True)
            return

        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files", f"{len(files)}")
        with col2:
            total_size = sum(f.stat().st_size for f in files)
            st.metric("Total Size", f"{total_size / 1024 / 1024:.1f} MB")
        with col3:
            folders = len(set(f.parent.name for f in files))
            st.metric("Categories", f"{folders}")

        st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)

        # Filter
        export_type = st.selectbox(
            "Filter",
            ["All"] + list(EXPORT_FOLDERS.keys()),
            label_visibility="collapsed"
        )

        if export_type != "All":
            files = [f for f in files if f.parent.name == EXPORT_FOLDERS.get(export_type, export_type)]

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        # Group by folder
        by_folder = {}
        for f in files:
            folder = f.parent.name
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(f)

        # Display
        for folder, folder_files in sorted(by_folder.items()):
            with st.expander(f"**{folder}** ({len(folder_files)} files)", expanded=True):
                for fp in sorted(folder_files, reverse=True)[:10]:
                    col1, col2, col3 = st.columns([4, 1, 1])

                    with col1:
                        size = fp.stat().st_size
                        mod = datetime.fromtimestamp(fp.stat().st_mtime)
                        st.markdown(f"**{fp.name}**")
                        st.caption(f"{size:,} bytes · {mod.strftime('%Y-%m-%d %H:%M')}")

                    with col2:
                        key = str(fp).replace('\\', '_').replace('/', '_').replace(':', '_')
                        if st.button("Preview", key=f"prev_{key}"):
                            st.session_state.preview_file = str(fp)

                    with col3:
                        with open(fp, 'rb') as f:
                            st.download_button(
                                "Download",
                                data=f,
                                file_name=fp.name,
                                mime="text/csv",
                                key=f"dl_{key}"
                            )

                    if st.session_state.preview_file == str(fp):
                        try:
                            preview_df = pd.read_csv(fp)
                            st.dataframe(preview_df.head(20), use_container_width=True)
                        except Exception as e:
                            st.error(f"Preview error: {e}")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def settings_page():
    """Settings page"""

    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Settings</h1>
        <p class="page-subtitle">Configure application preferences</p>
    </div>
    """, unsafe_allow_html=True)

    # About
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">About</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <p class="card-desc" style="margin-bottom: 16px;">
            <strong>Swadha Automation</strong> streamlines inventory management by syncing data between
            MyBillBook and Google Sheets. It handles consolidation, deduplication, and export generation automatically.
        </p>
        <div style="display: flex; gap: 24px; flex-wrap: wrap;">
            <div>
                <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0;">VERSION</p>
                <p style="font-family: var(--font-mono); margin: 4px 0 0 0;">2.0.0</p>
            </div>
            <div>
                <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0;">PYTHON</p>
                <p style="font-family: var(--font-mono); margin: 4px 0 0 0;">""" + f"{sys.version_info.major}.{sys.version_info.minor}" + """</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)

    # System Status
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">System Status</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        status = "Connected" if st.session_state.sheets_manager else "Disconnected"
        st.metric("Google Sheets", status)

    with col2:
        csv_folder = Path(__file__).parent.parent / "csv_exports"
        count = sum(1 for _ in csv_folder.rglob("*.csv")) if csv_folder.exists() else 0
        st.metric("CSV Files", f"{count}")

    with col3:
        st.metric("Auto-Save", "Enabled" if st.session_state.auto_export_csv else "Disabled")

    st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)

    # Actions
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Actions</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Reconnect to Google Sheets", use_container_width=False):
        st.session_state.sheets_manager = None
        st.rerun()


def main():
    """Main app"""
    render_sidebar()

    page = st.session_state.current_page

    if page == "Dashboard":
        dashboard_page()
    elif page == "Labels":
        labels_page()
    elif page == "Exports":
        exports_page()
    elif page == "Settings":
        settings_page()


if __name__ == "__main__":
    main()
