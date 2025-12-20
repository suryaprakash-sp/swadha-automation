"""
MyBillBook API Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
BASE_URL = "https://mybillbook.in/api/web"

# Authentication credentials from environment
AUTH_TOKEN = os.getenv("MYBILLBOOK_AUTH_TOKEN", "")
COOKIES = os.getenv("MYBILLBOOK_COOKIES", "")
COMPANY_ID = os.getenv("MYBILLBOOK_COMPANY_ID", "")

# Request configuration
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2


def get_headers():
    """Returns headers for API requests"""
    return {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "authorization": AUTH_TOKEN,
        "client": "web",
        "company-id": COMPANY_ID,
        "content-type": "application/json",
        "cookie": COOKIES,
        "dnt": "1",
        "priority": "u=1, i",
        "referer": "https://mybillbook.in/app/home/items",
        "sec-ch-ua": '"Not_A Brand";v="99", "Chromium";v="142"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }


def has_credentials():
    """Check if credentials are configured"""
    return bool(AUTH_TOKEN and COMPANY_ID)
