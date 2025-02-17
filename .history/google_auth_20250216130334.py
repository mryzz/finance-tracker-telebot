from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", ["https://www.googleapis.com/auth/spreadsheets"])
creds = flow.run_console()

print("Access Token:", creds.token)
print("Refresh Token:", creds.refresh_token)
print("Credentials saved.")
