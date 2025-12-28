"""
MyBillBook API Client
"""

import requests
import time
from typing import Optional, Dict, Any
from mybillbook.config import (
    BASE_URL,
    get_headers,
    REQUEST_TIMEOUT,
    RETRY_ATTEMPTS,
    RETRY_DELAY,
)


class MyBillBookAPI:
    """Handles API requests to MyBillBook"""

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = get_headers()
        self.session = requests.Session()

        # Update headers carefully to avoid encoding issues
        for key, value in self.headers.items():
            if value:  # Only set non-empty headers
                # Encode to bytes and decode to handle special characters
                try:
                    self.session.headers[key] = value
                except Exception:
                    # Skip headers that can't be encoded
                    print(f"Warning: Skipping header {key} due to encoding issue")
                    pass

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        retry_count: int = 0,
    ) -> Optional[Dict[str, Any]]:
        """Make an API request with retry logic"""
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            elif method == "POST":
                response = self.session.post(
                    url, json=data, params=params, timeout=REQUEST_TIMEOUT
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            if response.status_code == 401:
                print("[ERROR] Authentication failed. Please check your MyBillBook credentials in .env")
                return None
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting before retry...")
                if retry_count < RETRY_ATTEMPTS:
                    time.sleep(RETRY_DELAY * (retry_count + 1))
                    return self._make_request(
                        endpoint, method, params, data, retry_count + 1
                    )
            else:
                print(f"Status Code: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("[ERROR] Connection error. Please check your internet connection.")
            if retry_count < RETRY_ATTEMPTS:
                print(f"Retrying... (Attempt {retry_count + 1}/{RETRY_ATTEMPTS})")
                time.sleep(RETRY_DELAY)
                return self._make_request(
                    endpoint, method, params, data, retry_count + 1
                )

        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out.")
            if retry_count < RETRY_ATTEMPTS:
                print(f"Retrying... (Attempt {retry_count + 1}/{RETRY_ATTEMPTS})")
                time.sleep(RETRY_DELAY)
                return self._make_request(
                    endpoint, method, params, data, retry_count + 1
                )

        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")

        return None

    def get_all_items(self, per_page: int = 500) -> Optional[Dict[str, Any]]:
        """
        Fetch all inventory items

        Args:
            per_page: Number of items per page (default 500)

        Returns:
            Dictionary with inventory_items and total_count
        """
        print("Fetching inventory from MyBillBook API...")
        params = {"page": 1, "per_page": per_page}
        return self._make_request("/items", params=params)

    def get_sales_invoices(
        self,
        per_page: int = 15,
        start_date: str = None,
        end_date: str = None,
        status: str = "final",
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch sales invoices (vouchers) with automatic pagination to get ALL invoices

        Args:
            per_page: Number of invoices per page (default 15, safe page size)
            start_date: Start date filter (YYYY-MM-DD format)
            end_date: End date filter (YYYY-MM-DD format)
            status: Invoice status filter (default "final")

        Returns:
            Dictionary with all vouchers collected from all pages
        """
        print("Fetching sales invoices from MyBillBook API...")

        # Set default date range (last year to today)
        from datetime import datetime, timedelta
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        all_vouchers = []
        page = 1
        total_fetched = 0

        while True:
            params = {
                "per_page": per_page,
                "page": page,
                "status": status,
                "start_date": start_date,
                "end_date": end_date,
                "sort_by": "voucher_date",
                "sort_order": "",
                "voucher_type": "sales_invoice",
                "filter": "true",
            }

            print(f"  Fetching page {page} (per_page={per_page})...")
            result = self._make_request("/vouchers", params=params)

            if not result or "vouchers" not in result:
                print(f"[ERROR] Failed to fetch page {page}")
                break

            vouchers = result.get("vouchers", [])

            if not vouchers:
                print(f"  No more invoices on page {page}. Done!")
                break

            all_vouchers.extend(vouchers)
            total_fetched += len(vouchers)
            print(f"  Page {page}: {len(vouchers)} invoices (Total: {total_fetched})")

            # If we got fewer vouchers than per_page, we're on the last page
            if len(vouchers) < per_page:
                print(f"  Last page reached!")
                break

            page += 1
            time.sleep(0.5)  # Small delay to be nice to the API

        print(f"\n[OK] Fetched {total_fetched} sales invoices total!")
        return {"vouchers": all_vouchers, "total_count": total_fetched}

    def get_expenses(
        self,
        per_page: int = 15,
        start_date: str = None,
        end_date: str = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch expenses (vouchers) with automatic pagination to get ALL expenses

        Args:
            per_page: Number of expenses per page (default 15, safe page size)
            start_date: Start date filter (YYYY-MM-DD format)
            end_date: End date filter (YYYY-MM-DD format)

        Returns:
            Dictionary with all vouchers collected from all pages
        """
        print("Fetching expenses from MyBillBook API...")

        # Set default date range (last year to today)
        from datetime import datetime, timedelta
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        all_vouchers = []
        page = 1
        total_fetched = 0

        while True:
            params = {
                "per_page": per_page,
                "page": page,
                "status": "",
                "start_date": start_date,
                "end_date": end_date,
                "sort_by": "voucher_date",
                "sort_order": "",
                "voucher_type": "expense",
                "filter": "true",
            }

            print(f"  Fetching page {page} (per_page={per_page})...")
            result = self._make_request("/vouchers", params=params)

            if not result or "vouchers" not in result:
                print(f"[ERROR] Failed to fetch page {page}")
                break

            vouchers = result.get("vouchers", [])

            if not vouchers:
                print(f"  No more expenses on page {page}. Done!")
                break

            all_vouchers.extend(vouchers)
            total_fetched += len(vouchers)
            print(f"  Page {page}: {len(vouchers)} expenses (Total: {total_fetched})")

            # If we got fewer vouchers than per_page, we're on the last page
            if len(vouchers) < per_page:
                print(f"  Last page reached!")
                break

            page += 1
            time.sleep(0.5)  # Small delay to be nice to the API

        print(f"\n[OK] Fetched {total_fetched} expenses total!")
        return {"vouchers": all_vouchers, "total_count": total_fetched}

    def test_connection(self) -> bool:
        """Test API connection and authentication"""
        print("Testing MyBillBook API connection...")
        result = self._make_request("/items/stats")
        if result:
            print("[OK] MyBillBook API connection successful!")
            return True
        else:
            print("[ERROR] MyBillBook API connection failed.")
            return False
