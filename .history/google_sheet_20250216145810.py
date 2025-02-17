from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "13FHli56sdt1pWQ-wApkF6P2foeGZnC_IPcfpA72HGpU"


class GoogleSheets:
    def __init__(self):
        self.creds = None
        self.service = None
        self.token_file = "token.json"
        self.credentials_file = "credentials.json"
        self.scopes = SCOPES
        self.authenticate()


    def authenticate(self):
        # Check id token exists and authenticate if not
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        else:
            self.get_new_token()
        # Build service sheet object
        self.service = build("sheets", "v4", credentials=self.creds)


    def get_new_token(self):
        # Load credentials
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)

        # Starts a local server for authentication
        self.creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")

        # Save token to file
        with open("token.json", "w") as f:
            f.write(self.creds.to_json())

        print("Authentication successful!")


    def check_detail_balance(self):
        """Reads data of a range from a Google Sheet."""
        try: 
            combined = ""
            sheet = self.service.spreadsheets()
            range_names = ["A:A", "C:C", "D:D", "E:E"]
            result = (
                sheet
                .values()
                .batchGet(spreadsheetId=SPREADSHEET_ID, ranges=range_names)
                .execute()
            )
            ranges = result.get("valueRanges", [])
            datetime_list = ranges[0]['values'][1:]
            amount_list = ranges[1]['values'][1:]
            purpose_list = ranges[2]['values'][1:]
            remarks_list = ranges[3]['values'][1:]
            print(remarks_list)
            length = len(datetime_list)
            # for i in range(length):
            #     combined += f"{datetime_list[i][0]} {amount_list[i][0]} {purpose_list[i][0]} {remarks_list[i][0]}\n"
            # return combined  
        except HttpError as e:
            print(f"Error: {e}")

    def write_sheet(self, range_name, values):
        """Writes data to a Google Sheet."""
        body = {'values': values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result
    

    def append_sheet(self, spreadsheet_id, range_name, values):
        """Appends data to a Google Sheet."""
        body = {'values': values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result
    
google_sheets = GoogleSheets()
print(google_sheets.check_detail_balance())