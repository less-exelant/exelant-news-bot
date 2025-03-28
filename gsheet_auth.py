# gsheet_auth.py
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def append_test_row():
    creds = authenticate()
    client = gspread.authorize(creds)
    sheet = client.open("Exelant News Log").sheet1
    sheet.append_row(["✅ Bot Test", "News Bot", "Testing OAuth", "https://exelant.io", "Summary Test"])

if __name__ == '__main__':
    append_test_row()
