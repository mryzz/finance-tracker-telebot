from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os
from googleapiclient.errors import HttpError
from datetime import datetime

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

    def check_balance(self):
        """Reads balance from a Google Sheet."""
        try: 
            today = datetime.now()
            combined = f"Current mouth: {today.strftime("%B")}\nMonthly budget | Monthly expense | Monthly left \n"
            sheet = self.service.spreadsheets()
            range_names = ["H:H","I:I", "J:J", "K:K", "L:L"]
            result = (
                sheet
                .values()
                .batchGet(spreadsheetId=SPREADSHEET_ID, ranges=range_names)
                .execute()
            )
            index_list = result["valueRanges"][0]['values'][1:]
            budget_list = result["valueRanges"][2]['values'][1:]
            expense_list = result["valueRanges"][3]['values'][1:]
            net_cash_list = result["valueRanges"][4]['values'][1:]
            for i in range(len(index_list)):
                if int(index_list[i][0]) == today.month:
                    combined += f"      {budget_list[i][0]}      |       {expense_list[i][0]}        |     {net_cash_list[i][0]}  \n"
            return combined  
        except HttpError as e:
            print(f"Error: {e}")

    def check_detail_balance(self):
        """Reads data of a range from a Google Sheet."""
        try: 
            combined = "|Datetime             |Amount   |Purpose\n"
            sheet = self.service.spreadsheets()
            range_names = ["A:A", "C:C", "D:D"]
            result = (
                sheet
                .values()
                .batchGet(spreadsheetId=SPREADSHEET_ID, ranges=range_names)
                .execute()
            )
            # ranges = result.get("valueRanges", [])
            datetime_list = result["valueRanges"][0]['values'][1:]
            amount_list = result["valueRanges"][1]['values'][1:]
            purpose_list = result["valueRanges"][2]['values'][1:]
            length = len(datetime_list)
            for i in range(length):
                combined += f"|{datetime_list[i][0]}   |{amount_list[i][0]}       |{purpose_list[i][0]}\n"
            return combined  
        except HttpError as e:
            print(f"Error: {e}")

    def append_values(spreadsheet_id, range_name, value_input_option, _values):
        """
        Creates the batch_update the user has access to.
        """
        try:
            sheet = self.service.spreadsheets()
            values = [
                [
                    # Cell values ...
                ],
                # Additional rows ...
            ]
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption=value_input_option,
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    

    def append_sheet(self, spreadsheet_id, range_name, values):
        """Appends data to a Google Sheet."""
        body = {'values': values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result
    
google_sheets = GoogleSheets()
print(google_sheets.check_balance())