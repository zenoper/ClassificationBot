import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import config as Config

class GoogleSheetsManager:
    def __init__(self):
        # Load credentials from config
        credentials_info = json.loads(Config.GOOGLE_CREDENTIALS)
        
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = Credentials.from_service_account_info(
            credentials_info,
            scopes=self.SCOPES
        )
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.spreadsheet_id = Config.SPREADSHEET_ID

    def _get_next_row(self, sheet_name: str) -> int:
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'{sheet_name}!A:A'
            ).execute()
            values = result.get('values', [])
            return len(values) + 1
        except HttpError as e:
            print(f"Error getting next row: {e}")
            raise

    async def add_human_entry(self, unique_number: str, initiator_name: str, data: dict):
        try:
            sheet_name = 'Humans'
            next_row = self._get_next_row(sheet_name)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            values = [[
                next_row,  # No. of line
                f"#{unique_number}",  # Unique Bot Data #
                initiator_name,  # Initiator Name
                data['gender'],  # Category 1
                data['age'],  # Category 2
                data['nationality'],  # Category 3
                data['education'],  # Category 4
                data['eye_color'],  # Category 5
                data['hair_color'],  # Category 6
                data['height'],  # Category 7
                current_date  # Date
            ]]

            body = {
                'values': values
            }

            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f'{sheet_name}!A:K',
                valueInputOption='RAW',
                body=body
            ).execute()

        except HttpError as e:
            print(f"Error adding human entry: {e}")
            raise

    async def add_animal_entry(self, unique_number: str, initiator_name: str, data: dict):
        try:
            sheet_name = 'Animals'
            next_row = self._get_next_row(sheet_name)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            values = [[
                next_row,  # No. of line
                f"#{unique_number}",  # Unique Bot Data #
                initiator_name,  # Initiator Name
                data['species'],  # Category 1
                data['mammal'],  # Category 2
                data['predator'],  # Category 3
                data['color'],  # Category 4
                data['weight'],  # Category 5
                data['age'],  # Category 6
                current_date  # Date
            ]]

            body = {
                'values': values
            }

            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f'{sheet_name}!A:J',
                valueInputOption='RAW',
                body=body
            ).execute()

        except HttpError as e:
            print(f"Error adding animal entry: {e}")
            raise

    async def add_alien_entry(self, unique_number: str, initiator_name: str, data: dict):
        try:
            sheet_name = 'Aliens'
            next_row = self._get_next_row(sheet_name)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Initialize all possible fields with None
            values = [[
                next_row,  # No. of line
                f"#{unique_number}",  # Unique Bot Data #
                initiator_name,  # Initiator Name
                data['humanoid'],  # Category 1
                None,  # Race
                None,  # Skin color
                None,  # Dangerous
                None,  # Has reason
                data['weight'],  # Weight
                current_date  # Date
            ]]

            # If humanoid is yes, update the relevant fields
            if data['humanoid'] == 'yes':
                values[0][4] = data['race']
                values[0][5] = data['skin_color']
                values[0][6] = data['dangerous']
                values[0][7] = data['has_reason']

            body = {
                'values': values
            }

            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f'{sheet_name}!A:J',
                valueInputOption='RAW',
                body=body
            ).execute()

        except HttpError as e:
            print(f"Error adding alien entry: {e}")
            raise 