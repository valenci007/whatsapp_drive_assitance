import os
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def setup_google_drive_desktop():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('tokens/drive_token.json'):
        creds = Credentials.from_authorized_user_file('tokens/drive_token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use local server flow for desktop app
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        os.makedirs('tokens', exist_ok=True)
        with open('tokens/drive_token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service
    service = build('drive', 'v3', credentials=creds)

    # Test the connection
    print("✅ Testing Google Drive connection...")
    results = service.files().list(pageSize=5, fields="files(id, name)").execute()
    files = results.get('files', [])

    print(f"✅ Google Drive authentication successful!")
    print(f"📁 Found {len(files)} files in your Drive")

    return service


if __name__ == '__main__':
    try:
        service = setup_google_drive_desktop()
    except Exception as e:
        print(f"❌ Error: {e}")