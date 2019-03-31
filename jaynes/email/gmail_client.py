import os.path
import pickle

from google.auth.transport.requests import Request
from googleapiclient.discovery import Resource, build

from google_auth_oauthlib.flow import InstalledAppFlow
from jaynes.constants import ROOT_DIR

SCOPES = ('https://www.googleapis.com/auth/gmail.readonly', )


def _fetch_creds(token_path: str, credentials_path: str):
    creds = None

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(ROOT_DIR, 'credentials.json'), SCOPES)
        creds = flow.run_local_server()

    with open(token_path, 'wb') as token_out:
        pickle.dump(creds, token_out)

    return creds


def gmail_client() -> Resource:
    token_path = os.path.join(ROOT_DIR, 'token.pickle')
    creds_path = os.path.join(ROOT_DIR, 'credentials.json')

    creds = _fetch_creds(token_path, creds_path)
    return build('gmail', 'v1', credentials=creds)
