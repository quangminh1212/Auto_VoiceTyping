from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

class GoogleAuth:
    def __init__(self):
        self.credentials = None
        self.scopes = [
            'https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive.file'
        ]
        self.token_file = 'token.json'
        
    def load_saved_credentials(self):
        if os.path.exists(self.token_file):
            return Credentials.from_authorized_user_file(self.token_file, self.scopes)
        return None
    
    def authenticate(self):
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    'client_secret.json',
                    scopes=self.scopes
                )
                self.credentials = flow.run_local_server(port=0)
        
        return self.credentials