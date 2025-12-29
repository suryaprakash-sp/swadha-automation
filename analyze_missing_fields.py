#!/usr/bin/env python3
"""
Analyze all MyBillBook API responses to identify missing fields
that could be useful for future analytics
"""

import sys
from pathlib import Path
import json
sys.path.insert(0, str(Path.cwd()))

from mybillbook.api_client import MyBillBookAPI

api = MyBillBookAPI()

print("="*80)
print("ANALYZING MYBILLBOOK API RESPONSES FOR MISSING FIELDS")
print("="*80)
print()

# ============================================================================
# 1. INVENTORY/ITEMS
# ============================================================================
print("="*80)
print("1. INVENTORY API (/items)")
print("="*80)
print()

items_result = api.get_all_items(per_page=5)
if items_result and items_result.get('items'):
    sample_item = items_result['items'][0]

    print("FULL ITEM STRUCTURE (first item):")
    print(json.dumps(sample_item, indent=2))
    print()

    print("ALL AVAILABLE FIELDS:")
    all_keys = set()
    for item in items_result['items'][:5]:
        all_keys.update(item.keys())

    for key in sorted(all_keys):
        print(f"  - {key}")
    print()

    print("CURRENTLY CAPTURED FIELDS:")
    captured = [
        'id', 'name', 'sku_code', 'mbb_id', 'barcode', 'selling_price',
        'cost_price', 'stock_quantity', 'unit', 'category_name',
        'opening_stock', 'item_type', 'gst_percentage', 'hsn_sac_code',
        'description', 'min_stock_to_maintain', 'max_stock_to_maintain',
        'cess_percentage'
    ]
    for field in captured:
        print(f"  - {field}")
    print()

    # Find missing fields
    missing = all_keys - set(captured)
    if missing:
        print("MISSING FIELDS (potentially useful):")
        for field in sorted(missing):
            sample_value = sample_item.get(field)
            print(f"  - {field}: {type(sample_value).__name__} = {sample_value}")
    else:
        print("[OK] All fields are captured!")
    print()

# ============================================================================
# 2. SALES INVOICES
# ============================================================================
print("="*80)
print("2. SALES INVOICES API (/vouchers - sales_invoice)")
print("="*80)
print()

sales_result = api.get_sales_invoices(per_page=5, status='final')
if sales_result and sales_result.get('vouchers'):
    sample_invoice = sales_result['vouchers'][0]

    print("FULL INVOICE STRUCTURE (first invoice):")
    print(json.dumps(sample_invoice, indent=2))
    print()

    print("ALL AVAILABLE FIELDS:")
    all_keys = set()
    for inv in sales_result['vouchers'][:5]:
        all_keys.update(inv.keys())

    for key in sorted(all_keys):
        print(f"  - {key}")
    print()

    print("CURRENTLY CAPTURED FIELDS:")
    captured = [
        'invoice_number', 'invoice_date', 'serial_number', 'contact_name',
        'contact_type', 'total_amount', 'initial_payment_amount',
        'remaining_amount', 'payment_mode', 'payment_type', 'due_date',
        'status', 'created_at', 'id', 'mbb_id', 'share_link', 'notes',
        'source', 'ledger_category_name', 'bank_account_id',
        'convertable_id', 'recurring_id', 'einvoice_status'
    ]
    for field in captured:
        print(f"  - {field}")
    print()

    # Find missing fields
    missing = all_keys - set(captured)
    if missing:
        print("MISSING FIELDS (potentially useful):")
        for field in sorted(missing):
            sample_value = sample_invoice.get(field)
            print(f"  - {field}: {type(sample_value).__name__} = {sample_value}")
    else:
        print("[OK] All fields are captured!")
    print()

# ============================================================================
# 3. EXPENSES
# ============================================================================
print("="*80)
print("3. EXPENSES API (/vouchers - expense)")
print("="*80)
print()

expenses_result = api.get_expenses(per_page=5)
if expenses_result and expenses_result.get('vouchers'):
    sample_expense = expenses_result['vouchers'][0]

    print("FULL EXPENSE STRUCTURE (first expense):")
    print(json.dumps(sample_expense, indent=2))
    print()

    print("ALL AVAILABLE FIELDS:")
    all_keys = set()
    for exp in expenses_result['vouchers'][:5]:
        all_keys.update(exp.keys())

    for key in sorted(all_keys):
        print(f"  - {key}")
    print()

    print("CURRENTLY CAPTURED FIELDS:")
    captured = [
        'invoice_number', 'invoice_date', 'serial_number',
        'ledger_category_name', 'total_amount', 'initial_payment_amount',
        'payment_mode', 'payment_type', 'created_at', 'id', 'mbb_id',
        'notes', 'source', 'bank_account_id', 'contact_name', 'share_link'
    ]
    for field in captured:
        print(f"  - {field}")
    print()

    # Also check txn_ledgers structure
    if 'txn_ledgers' in sample_expense and sample_expense['txn_ledgers']:
        print("TXN_LEDGERS STRUCTURE:")
        print(json.dumps(sample_expense['txn_ledgers'][0], indent=2))
        print()

    # Find missing fields
    missing = all_keys - set(captured)
    if missing:
        print("MISSING FIELDS (potentially useful):")
        for field in sorted(missing):
            sample_value = sample_expense.get(field)
            print(f"  - {field}: {type(sample_value).__name__} = {sample_value}")
    else:
        print("[OK] All fields are captured!")
    print()

# ============================================================================
# 4. INVOICE LINE ITEMS (DETAILED)
# ============================================================================
print("="*80)
print("4. INVOICE LINE ITEMS API (/invoices/:id)")
print("="*80)
print()

# Get a sample invoice ID
if sales_result and sales_result.get('vouchers'):
    sample_id = sales_result['vouchers'][0].get('id')

    invoice_details = api._make_request(f'/invoices/{sample_id}')

    if invoice_details:
        print("FULL INVOICE DETAIL STRUCTURE:")
        print(json.dumps(invoice_details, indent=2, default=str)[:2000])
        print("\n...(truncated for readability)\n")

        print("INVOICE-LEVEL FIELDS:")
        for key in sorted(invoice_details.keys()):
            if key != 'items':
                print(f"  - {key}")
        print()

        print("CURRENTLY CAPTURED INVOICE-LEVEL FIELDS:")
        captured_invoice = [
            'invoice_number', 'invoice_date', 'contact_name', 'total_amount',
            'payment_mode', 'discount', 'discount_type'
        ]
        for field in captured_invoice:
            print(f"  - {field}")
        print()

        # Missing invoice-level fields
        missing_invoice = set(invoice_details.keys()) - set(captured_invoice) - {'items'}
        if missing_invoice:
            print("MISSING INVOICE-LEVEL FIELDS:")
            for field in sorted(missing_invoice):
                value = invoice_details.get(field)
                print(f"  - {field}: {type(value).__name__} = {str(value)[:100]}")
        print()

        # Analyze items structure
        if 'items' in invoice_details and invoice_details['items']:
            sample_line_item = invoice_details['items'][0]

            print("LINE ITEM STRUCTURE:")
            print(json.dumps(sample_line_item, indent=2))
            print()

            print("ALL AVAILABLE ITEM FIELDS:")
            all_item_keys = set()
            for item in invoice_details['items']:
                all_item_keys.update(item.keys())

            for key in sorted(all_item_keys):
                print(f"  - {key}")
            print()

            print("CURRENTLY CAPTURED ITEM FIELDS:")
            captured_items = [
                'name', 'sku_code', 'quantity', 'unit', 'price_per_unit',
                'discount', 'discount_type', 'discount_amount', 'gst_percentage',
                'is_tax_included', 'item_final_amount', 'item_type', 'mrp',
                'description', 'notes'
            ]
            for field in captured_items:
                print(f"  - {field}")
            print()

            # Missing item fields
            missing_items = all_item_keys - set(captured_items)
            if missing_items:
                print("MISSING ITEM FIELDS (potentially useful):")
                for field in sorted(missing_items):
                    value = sample_line_item.get(field)
                    print(f"  - {field}: {type(value).__name__} = {value}")
            else:
                print("[OK] All item fields are captured!")
            print()

print()
print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
