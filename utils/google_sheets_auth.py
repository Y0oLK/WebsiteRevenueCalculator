from google.oauth2.service_account import Credentials
from gspread import authorize

def authorize_google_sheets():
    """
    Authorizes the Google Sheets API using service account credentials.
    """
    try:
        # Replace 'path/to/credentials.json' with the path to your service account key file
        credentials = Credentials.from_service_account_file(
            'credentials.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = authorize(credentials)
        return client, None
    except Exception as e:
        return None, str(e)
