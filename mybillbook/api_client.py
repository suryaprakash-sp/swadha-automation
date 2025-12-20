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
        self.session.headers.update(self.headers)

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
