from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

class GoogleAuth:
    def __init__(self):
        self.creds = None
        self.scopes = ['https://www.googleapis.com/auth/documents']
    
    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    'client_secret.json', self.scopes)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        return self.creds