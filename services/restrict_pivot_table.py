from utils.google_sheets_auth import authorize_google_sheets

def update_pivot_table(spreadsheet_id):
    client, error = authorize_google_sheets()

    if client is None:
        return f"Authorization Failed: {error}"

    try:
        # Open the spreadsheet
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Get the data sheet and pivot table sheet
        data_sheet = spreadsheet.worksheet('Raw data (Restrict)')
        pivot_sheet = spreadsheet.worksheet('Restrict Pivot table')

        # Get the number of rows
        num_rows = len(data_sheet.get_all_values())

        # Create the pivot table request
        body = {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": pivot_sheet.id
                        },
                        "fields": "pivotTable"
                    }
                },
                {
                    "updateCells": {
                        "rows": {
                            "values": [
                                {
                                    "pivotTable": {
                                        "source": {
                                            "sheetId": data_sheet.id,
                                            "startRowIndex": 0,
                                            "endRowIndex": num_rows,
                                            "startColumnIndex": 0,
                                            "endColumnIndex": 24  #  columns end at X (24 columns)
                                        },
                                        "rows": [
                                            {
                                                "sourceColumnOffset": 4,  # Column for 'Membership Level Name'
                                                "showTotals": True,
                                                "sortOrder": "ASCENDING"
                                            }
                                        ],
                                        "columns": [
                                            {
                                                "sourceColumnOffset": 22,  # Column for 'Date-Month'
                                                "showTotals": True,
                                                "sortOrder": "ASCENDING"
                                            }
                                        ],
                                        "values": [
                                            {
                                                "summarizeFunction": "SUM",
                                                "sourceColumnOffset": 23,  # Column for 'Quantity'
                                                "name": "Quantity"
                                            },
                                            {
                                                "summarizeFunction": "SUM",
                                                "sourceColumnOffset": 5,  # Column for 'Total Amount'
                                                "name": "Total Revenue"
                                            }
                                        ],
                                        "criteria": {
                                            "21": {
                                                "visibleByDefault": True  # Filter for 'Date' should show all items
                                            }
                                        }
                                    }
                                }
                            ]
                        },
                        "start": {
                            "sheetId": pivot_sheet.id,
                            "rowIndex": 0,
                            "columnIndex": 0
                        },
                        "fields": "pivotTable"
                    }
                },
                # Add a freeze for the first column
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": pivot_sheet.id,
                            "gridProperties": {
                                "frozenColumnCount": 1
                            }
                        },
                        "fields": "gridProperties.frozenColumnCount"
                    }
                }
            ]
        }

        # Send the request to the Google Sheets API
        spreadsheet.batch_update(body)
        return "Pivot table updated successfully"
    except Exception as e:
        return f"Error: {str(e)}"