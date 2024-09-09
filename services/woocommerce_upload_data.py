import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def upload_woocommerce_data(file_path):
    # Set up Google Sheets API credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet by ID and sheet title
    spreadsheet_id = '1WvHJWyuSa2LUqZrY7yDijsj0g0L3oTGvp8Tr6hAa0lE'
    sheet = client.open_by_key(spreadsheet_id).worksheet('Raw data (Woocommerce)')

    # Load data from the provided file (CSV)
    data = pd.read_csv(file_path)

    # Replace NaN values with empty strings
    data = data.fillna('')

    # Convert data to a list of lists
    data_list = data.values.tolist()

    # Get the last row before uploading data
    last_row_before_upload = len(sheet.get_all_values())

    # Append new data to the sheet
    sheet.append_rows(data_list, value_input_option='RAW')

    # Get the number of rows with data after appending
    num_rows = len(sheet.get_all_values())

    # Determine the range for the new rows where formulas need to be applied
    start_row = last_row_before_upload + 1

    # Formula for Column AO: Item cost * quantity * discount for btc
    ao_range = f'AO{start_row}:AO{num_rows}'
    ao_formulas = [[f'=IF(V{row}="Pay with Bitcoin: on-chain or with Lightning",AG{row}*AH{row}*0.9,AG{row}*AH{row})'] for row in range(start_row, num_rows + 1)]

    # Formula for Column AP: Shipping price
    ap_range = f'AP{start_row}:AP{num_rows}'
    ap_formulas = [[f'=IF(AE{row}=1,Z{row},0)'] for row in range(start_row, num_rows + 1)]

    # Formula for Column AQ: Month based on date in column C
    aq_range = f'AQ{start_row}:AQ{num_rows}'
    aq_formulas = [[f'=TEXT(C{row}, "mmmm")'] for row in range(start_row, num_rows + 1)]

    # Batch update the formulas for AO, AP, and AQ columns using value_input_option='USER_ENTERED'
    sheet.update(ao_range, ao_formulas, value_input_option='USER_ENTERED')
    sheet.update(ap_range, ap_formulas, value_input_option='USER_ENTERED')
    sheet.update(aq_range, aq_formulas, value_input_option='USER_ENTERED')

    print("Data added and formulas updated successfully.")
