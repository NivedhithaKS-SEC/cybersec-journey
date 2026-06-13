# ============================================================
# gmail_auth.py — One-time Gmail OAuth2 authentication
# Run this ONCE to generate token.pickle
# ============================================================

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

def authenticate():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("[!] credentials.json not found!")
                print("    Download it from Google Cloud Console → APIs & Services → Credentials")
                return None

            print("[*] Opening browser for Google authentication...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
        print("[+] token.pickle saved successfully")

    # Verify connection
    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()
    print(f"[+] Connected to Gmail: {profile['emailAddress']}")
    print(f"[+] Total messages in mailbox: {profile.get('messagesTotal', '?')}")
    print("[+] Authentication successful!")
    return creds

if __name__ == '__main__':
    authenticate()
