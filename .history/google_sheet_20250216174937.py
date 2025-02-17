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
        self.recent_entry_cells = None


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
            range_names = ["'Compute (2025)'!A:A", "'Compute (2025)'!C:C", "'Compute (2025)'!D:D", "'Compute (2025)'!E:E"]
            result = (
                sheet
                .values()
                .batchGet(spreadsheetId=SPREADSHEET_ID, ranges=range_names)
                .execute()
            )
            index_list = result["valueRanges"][0]['values'][1:]
            budget_list = result["valueRanges"][1]['values'][1:]
            expense_list = result["valueRanges"][2]['values'][1:]
            net_cash_list = result["valueRanges"][3]['values'][1:]
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
            range_names = ["'Data (2025)'!A:A", "'Data (2025)'!B:B", "'Data (2025)'!C:C"]
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


    def append_values(self, _values):
        """
        Creates the batch_update the user has access to.
        Input amount, purpose, and remarks.
        """
        try:
            sheet = self.service.spreadsheets()
            today = datetime.now()
            datetimenow = today.strftime("%m/%d/%Y %H:%M:%S")
            range_names = "'Data (2025)'!A:E"
            values = [[datetimenow, _values[0], _values[1], _values[2], today.month]]
            body = {"values": values}
            result = (
                sheet
                .values()
                .append(
                    spreadsheetId=SPREADSHEET_ID,
                    range=range_names,
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            self.recent_entry_cells = result['tableRange']
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        

    def get_data(self, cell_range):
        sheet = self.service.spreadsheets()
        range_name = cell_range  
        # Get all current rows
        result = (
            sheet
            .values()
            .get(spreadsheetId=SPREADSHEET_ID, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        if not values or len(values) == 1:  # If empty or only headers exist
            print("No data to delete.")
            return None
        return values


    def delete_recent_entry(self):
        """Deletes the most recent entry from the Google Sheet."""
        sheet = self.service.spreadsheets()
        try:
            if self.recent_entry_cells is None:
                values = self.get_data("'Data (2025)'!A:E")
                last_row = len(values)  # Last row number (assuming no empty rows in between)
                delete_range = f"'Data (2025)'!A{last_row}:E{last_row}"  # Target last row
            else:   
                delete_range = self.recent_entry_cells

            # Clear only the last row
            result = (
                sheet
                .values()
                .clear(spreadsheetId=SPREADSHEET_ID, range=delete_range)
                .execute()
            )

            print(f"Deleted last entry at row {last_row}.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
        
    def update_budget(self, value):
        """Updates a specific cell in the Google Sheet based on row and column index."""
        try:
            current_month = datetime.now().month
            sheet = self.service.spreadsheets()
            body = {"values": [[value]]}  # New value for the cell
            cell_range = f"'Compute (2025)'!C{current_month+1}"  # Cell range to update
            # Update the cell
            result = (
                sheet
                .values()
                .update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=cell_range,
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )

            print(f"Updated cell {cell_range} with value: {value}")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


    
google_sheets = GoogleSheets()
# print(google_sheets.append_values(["1000", "food", "for dinner"]))
# print(google_sheets.check_balance())
# print(google_sheets.recent_entry_cells)
# print(google_sheets.delete_recent_entry())
print(google_sheets.update_budget(500))