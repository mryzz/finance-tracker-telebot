from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES, redirect_uri="http://localhost:8008/")
auth_url, _ = flow.authorization_url(port=8008, prompt="consent", access_type="offline")

