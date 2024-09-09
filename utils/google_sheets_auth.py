from google.oauth2.service_account import Credentials
from gspread import authorize

def authorize_google_sheets():
  
    try:
       
        credentials = Credentials.from_service_account_file(
            'credentials.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = authorize(credentials)
        return client, None
    except Exception as e:
        return None, str(e)
