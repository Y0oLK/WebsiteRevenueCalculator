import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def upload_restrict_data(file_path):
    # Set up Google Sheets API credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet by ID and sheet title
    spreadsheet_id = '1WvHJWyuSa2LUqZrY7yDijsj0g0L3oTGvp8Tr6hAa0lE'
    sheet = client.open_by_key(spreadsheet_id).worksheet('Raw data (Restrict)')

    # Get the number of rows with data before appending new data
    existing_data = sheet.get_all_values()
    last_row_before_upload = len(existing_data)

    # Load data from the provided file (CSV)
    data = pd.read_csv(file_path)

    # Replace NaN values with empty strings
    data = data.fillna('')

    # Convert data to a list of lists
    data_list = data.values.tolist()

    # Append new data to the sheet in one batch
    sheet.append_rows(data_list, value_input_option='RAW')

    # Get the number of rows with data after appending
    num_rows = len(sheet.get_all_values())

    # Determine the starting row for new data
    start_row = last_row_before_upload + 1

    # Format the "Date" column
    date_column_letter = 'V'
    date_range = f'{date_column_letter}{start_row}:{date_column_letter}{num_rows}'

    # Apply date format to the date column (mm/dd/yyyy hh:mm)
    sheet.format(date_range, {
        "numberFormat": {
            "type": "DATE_TIME",
            "pattern": "MM/dd/yyyy HH:mm"
        }
    })

    # Apply formulas to the "Month" and "Quantity" columns

    # Formula for the "Month" column ("W" is the "Month" column)
    month_column_letter = 'W'
    month_range = f'{month_column_letter}{start_row}:{month_column_letter}{num_rows}'
    month_formulas = [[f'=TEXT(V{row},"mmmm")'] for row in range(start_row, num_rows + 1)]

    # Formula for the "Quantity" column ("X" is the "Quantity" column)
    quantity_column_letter = 'X'
    quantity_range = f'{quantity_column_letter}{start_row}:{quantity_column_letter}{num_rows}'
    quantity_formulas = [[f'=IF(B{row}="complete",1,0)'] for row in range(start_row, num_rows + 1)]

    # update the formulas for both columns using value_input_option='USER_ENTERED'
    sheet.update(month_range, month_formulas, value_input_option='USER_ENTERED')
    sheet.update(quantity_range, quantity_formulas, value_input_option='USER_ENTERED')

    print("Data added, date formatted, and formulas updated successfully.")
