from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def authenticate():
    # Explicitly set the redirect_uri
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES, redirect_uri="http://localhost:5000/"
    )

    creds = flow.run_local_server(port=5000, access_type="offline", prompt="consent")

    # Save the token so you don't need to authenticate every time
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

    print("Authentication successful! Token saved.")

    return creds


