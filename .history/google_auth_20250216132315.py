from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Load credentials
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

# Starts a local server for authentication
creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")

print("Authentication successful!")

with open("token.json", "w") as f:
    f.write(creds.to_json())
