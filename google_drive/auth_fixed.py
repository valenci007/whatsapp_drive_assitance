import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDriveAuthFixed:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, credentials_file, token_file):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None

    def authenticate(self):
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Create the flow using the client secrets file
                flow = Flow.from_client_secrets_file(
                    self.credentials_file,
                    scopes=self.SCOPES,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # This fixes the redirect issue
                )

                # Generate authorization URL
                auth_url, _ = flow.authorization_url(prompt='consent')

                print('Please go to this URL and authorize access:')
                print(auth_url)

                # Get the authorization code from the user
                code = input('Enter the authorization code: ')

                # Exchange the authorization code for credentials
                flow.fetch_token(code=code)
                self.creds = flow.credentials

            # Save the credentials for the next run
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

        return build('drive', 'v3', credentials=self.creds)