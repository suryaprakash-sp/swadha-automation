#!/usr/bin/env python3
"""
Validate invoice line items sync
Checks if line item totals match invoice totals and if discounts are captured
"""

import sys
from pathlib import Path
import random
sys.path.insert(0, str(Path.cwd()))

from utils.sheets import SheetsManager
from mybillbook.api_client import MyBillBookAPI

sheets = SheetsManager()
api = MyBillBookAPI()

# Read all line items from Google Sheets
print('Reading Invoice Line Items from Google Sheets...')
data = sheets.read_sheet('Invoice Line Items')
headers = data[0]
rows = data[1:]

# Group by invoice number
invoices_dict = {}
for row in rows:
    if not row or len(row) < 16:
        continue
    invoice_num = row[0]
    if invoice_num not in invoices_dict:
        invoices_dict[invoice_num] = []
    invoices_dict[invoice_num].append(row)

print(f'Found {len(invoices_dict)} unique invoices in Google Sheets')
print()

# Get random 15 invoices
random_invoices = random.sample(list(invoices_dict.keys()), min(15, len(invoices_dict)))

print('Fetching invoice list from API to get IDs...')
result = api.get_sales_invoices(per_page=15, status='final')
all_invoices = result.get('vouchers', [])

# Create mapping of invoice number to ID
invoice_id_map = {inv.get('invoice_number'): inv.get('id') for inv in all_invoices}

print()
print('='*80)
print('VALIDATING 15 RANDOM INVOICES')
print('='*80)
print()

issues_found = []

for idx, invoice_num in enumerate(random_invoices[:15], 1):
    print(f'[{idx}/15] Invoice #{invoice_num}')
    print('-'*80)

    # Get Google Sheets data
    sheet_items = invoices_dict[invoice_num]
    # Remove commas from formatted numbers
    sheet_invoice_total = float(str(sheet_items[0][3]).replace(',', '')) if sheet_items[0][3] else 0
    sheet_items_sum = sum(float(str(row[15]).replace(',', '')) if row[15] else 0 for row in sheet_items)

    print(f'  Google Sheets:')
    print(f'    Invoice Total (column D): {sheet_invoice_total:.2f}')
    print(f'    Sum of Item Final Amounts: {sheet_items_sum:.2f}')
    print(f'    Number of items: {len(sheet_items)}')

    # Check if there are discounts in sheets
    has_item_discounts = any(float(str(row[10]).replace(',', '')) if row[10] else 0 > 0 for row in sheet_items)
    if has_item_discounts:
        print(f'    Item-level discounts found: YES')

    # Get API data
    if invoice_num in invoice_id_map:
        invoice_id = invoice_id_map[invoice_num]
        details = api._make_request(f'/invoices/{invoice_id}')

        if details:
            api_total = float(details.get('total_amount', 0))
            api_items = details.get('items', [])
            api_items_sum = sum(float(item.get('item_final_amount', 0)) for item in api_items)

            # Check for invoice-level discount
            api_invoice_discount = float(details.get('discount_amount', 0))
            api_subtotal = float(details.get('sub_total', 0))

            print(f'  MyBillBook API:')
            print(f'    Invoice Total: {api_total:.2f}')
            print(f'    Subtotal (before invoice discount): {api_subtotal:.2f}')
            print(f'    Invoice-level discount: {api_invoice_discount:.2f}')
            print(f'    Sum of Item Final Amounts: {api_items_sum:.2f}')
            print(f'    Number of items: {len(api_items)}')

            # Validation checks
            print(f'  Validation:')

            # Check 1: Sheet invoice total matches API invoice total
            if abs(sheet_invoice_total - api_total) > 0.01:
                issue = f'Invoice #{invoice_num}: Sheet total ({sheet_invoice_total:.2f}) != API total ({api_total:.2f})'
                print(f'    [FAIL] {issue}')
                issues_found.append(issue)
            else:
                print(f'    [OK] Invoice totals match: {sheet_invoice_total:.2f}')

            # Check 2: Sum of items matches expected
            if abs(sheet_items_sum - api_items_sum) > 0.01:
                issue = f'Invoice #{invoice_num}: Sheet items sum ({sheet_items_sum:.2f}) != API items sum ({api_items_sum:.2f})'
                print(f'    [FAIL] {issue}')
                issues_found.append(issue)
            else:
                print(f'    [OK] Item totals match: {sheet_items_sum:.2f}')

            # Check 3: Invoice-level discount handling
            if api_invoice_discount > 0:
                issue = f'Invoice #{invoice_num}: Has invoice-level discount of {api_invoice_discount:.2f} (NOT captured in line items!)'
                print(f'    [WARNING] {issue}')
                issues_found.append(issue)
                print(f'    Note: Items sum to {api_items_sum:.2f}, but invoice total is {api_total:.2f}')

            # Check 4: Items sum vs invoice total
            diff = abs(api_items_sum - api_total)
            if diff > 0.01:
                print(f'    [WARNING] Items sum ({api_items_sum:.2f}) != Invoice total ({api_total:.2f}), diff: {diff:.2f}')

    print()

print()
print('='*80)
print('SUMMARY')
print('='*80)
if issues_found:
    print(f'[ISSUES FOUND] Total: {len(issues_found)}')
    for i, issue in enumerate(issues_found, 1):
        print(f'{i}. {issue}')
else:
    print('[SUCCESS] All validations passed!')
