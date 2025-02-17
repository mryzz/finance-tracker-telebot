from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES, redirect_uri="http://localhost:8080/")
auth_url, _ = flow.authorization_url(port=8080, prompt="consent", access_type="offline")

print("Please go to this URL: ", auth_url)

code = input("Enter the authorization code: ")

flow.fetch_token(code=code)

creds = flow.run_local_server(port=8080)

print("Credentials: ", credentials)