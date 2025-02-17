from dotenv import load_dotenv
from google_sheet import GoogleSheets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


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