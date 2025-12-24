import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, SPREADSHEET_ID


class SheetsManager:
    def __init__(self):
        self.creds = None
        self.service = None
        self.spreadsheet_id = SPREADSHEET_ID
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API using OAuth 2.0"""
        if os.path.exists(TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('sheets', 'v4', credentials=self.creds)

    def read_sheet(self, sheet_name, range_notation=None):
        """
        Read data from a Google Sheet

        Args:
            sheet_name: Name of the sheet tab
            range_notation: Optional range (e.g., 'A1:D10'). If None, reads all data.

        Returns:
            List of lists containing the sheet data
        """
        try:
            if range_notation:
                range_name = f"{sheet_name}!{range_notation}"
            else:
                range_name = sheet_name

            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            return result.get('values', [])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def write_sheet(self, sheet_name, data, start_cell='A1', value_input_option='USER_ENTERED'):
        """
        Write data to a Google Sheet (creates sheet if it doesn't exist)

        Args:
            sheet_name: Name of the sheet tab
            data: List of lists containing the data to write
            start_cell: Starting cell (default 'A1')
            value_input_option: How to interpret input values (default 'USER_ENTERED')
                - 'USER_ENTERED': Parse values (numbers as numbers, formulas as formulas)
                - 'RAW': Store exactly as provided (everything as strings)
        """
        try:
            # Create sheet if it doesn't exist
            if not self.sheet_exists(sheet_name):
                self.create_sheet(sheet_name)

            range_name = f"{sheet_name}!{start_cell}"

            body = {
                'values': data
            }

            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()

            print(f"{result.get('updatedCells')} cells updated in {sheet_name}")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def sheet_exists(self, sheet_name):
        """
        Check if a sheet exists in the spreadsheet

        Args:
            sheet_name: Name of the sheet to check

        Returns:
            Boolean indicating if sheet exists
        """
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()

            for sheet in sheet_metadata.get('sheets', []):
                if sheet['properties']['title'] == sheet_name:
                    return True
            return False

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def create_sheet(self, sheet_name):
        """
        Create a new sheet in the spreadsheet

        Args:
            sheet_name: Name of the sheet to create
        """
        try:
            if self.sheet_exists(sheet_name):
                print(f"Sheet {sheet_name} already exists")
                return

            requests = [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }]

            body = {'requests': requests}

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            print(f"Created sheet: {sheet_name}")

        except HttpError as error:
            print(f"An error occurred: {error}")

    def clear_sheet(self, sheet_name):
        """Clear all data from a sheet (creates sheet if it doesn't exist)"""
        try:
            # Create sheet if it doesn't exist
            if not self.sheet_exists(sheet_name):
                self.create_sheet(sheet_name)
                return  # New sheet is already empty

            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name
            ).execute()
            print(f"Sheet {sheet_name} cleared")

        except HttpError as error:
            print(f"An error occurred: {error}")

    def _get_sheet_id(self, sheet_name):
        """Helper method to get sheet ID from sheet name"""
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()

            for sheet in sheet_metadata.get('sheets', []):
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            return None
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def _parse_range(self, range_notation):
        """Helper method to parse range notation like 'A1:B10'"""
        import re
        match = re.match(r'([A-Z]+)(\d+):([A-Z]+)(\d+)', range_notation)
        if not match:
            return None

        return {
            'start_col': self._column_letter_to_index(match.group(1)),
            'start_row': int(match.group(2)) - 1,
            'end_col': self._column_letter_to_index(match.group(3)),
            'end_row': int(match.group(4)) - 1
        }

    def format_as_text(self, sheet_name, range_notation):
        """
        Format cells as plain text (to prevent scientific notation for barcodes)

        Args:
            sheet_name: Name of the sheet tab
            range_notation: Range to format (e.g., 'B2:B100')
        """
        try:
            sheet_id = self._get_sheet_id(sheet_name)
            if sheet_id is None:
                print(f"Sheet {sheet_name} not found")
                return

            range_info = self._parse_range(range_notation)
            if not range_info:
                print("Invalid range notation")
                return

            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': range_info['start_row'],
                        'endRowIndex': range_info['end_row'] + 1,
                        'startColumnIndex': range_info['start_col'],
                        'endColumnIndex': range_info['end_col'] + 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'numberFormat': {
                                'type': 'TEXT'
                            }
                        }
                    },
                    'fields': 'userEnteredFormat.numberFormat'
                }
            }]

            body = {'requests': requests}

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            print(f"Formatted {range_notation} in {sheet_name} as text")

        except HttpError as error:
            print(f"An error occurred: {error}")

    def format_as_number_2decimals(self, sheet_name, range_notation):
        """
        Format cells as numbers with 2 decimal places (convenience method)

        Args:
            sheet_name: Name of the sheet tab
            range_notation: Range to format (e.g., 'C2:C100')
        """
        self.format_as_number(sheet_name, range_notation, decimal_places=2)

    def format_as_number(self, sheet_name, range_notation, decimal_places=0):
        """
        Format cells as numbers with specified decimal places

        Args:
            sheet_name: Name of the sheet tab
            range_notation: Range to format (e.g., 'C2:C100')
            decimal_places: Number of decimal places (0 for whole numbers, 2 for currency, etc.)
        """
        try:
            sheet_id = self._get_sheet_id(sheet_name)
            if sheet_id is None:
                print(f"Sheet {sheet_name} not found")
                return

            range_info = self._parse_range(range_notation)
            if not range_info:
                print("Invalid range notation")
                return

            # Create format pattern based on decimal places
            if decimal_places == 0:
                pattern = '#,##0'  # Whole number with thousands separator
            else:
                pattern = '#,##0.' + '0' * decimal_places  # Number with decimals

            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': range_info['start_row'],
                        'endRowIndex': range_info['end_row'] + 1,
                        'startColumnIndex': range_info['start_col'],
                        'endColumnIndex': range_info['end_col'] + 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'numberFormat': {
                                'type': 'NUMBER',
                                'pattern': pattern
                            }
                        }
                    },
                    'fields': 'userEnteredFormat.numberFormat'
                }
            }]

            body = {'requests': requests}

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            print(f"Formatted {range_notation} in {sheet_name} as number with {decimal_places} decimals")

        except HttpError as error:
            print(f"An error occurred: {error}")

    def write_formulas(self, sheet_name, formulas, start_cell='A1'):
        """
        Write formulas to a Google Sheet (creates sheet if it doesn't exist)

        Args:
            sheet_name: Name of the sheet tab
            formulas: List of lists containing formulas
            start_cell: Starting cell (default 'A1')
        """
        try:
            # Create sheet if it doesn't exist
            if not self.sheet_exists(sheet_name):
                self.create_sheet(sheet_name)

            range_name = f"{sheet_name}!{start_cell}"

            body = {
                'values': formulas
            }

            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',  # Important: USER_ENTERED to process formulas
                body=body
            ).execute()

            print(f"{result.get('updatedCells')} formula cells updated in {sheet_name}")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    @staticmethod
    def _column_letter_to_index(column_letter):
        """Convert column letter (A, B, AA, etc.) to zero-based index"""
        index = 0
        for char in column_letter:
            index = index * 26 + (ord(char.upper()) - ord('A')) + 1
        return index - 1
