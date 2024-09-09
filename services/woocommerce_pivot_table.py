from utils.google_sheets_auth import authorize_google_sheets

def update_woocommerce_pivot_table(spreadsheet_id):

    try:
        client, error = authorize_google_sheets()
        if client is None:
            return f"Authorization Failed: {error}"

        spreadsheet = client.open_by_key(spreadsheet_id)
        data_sheet = spreadsheet.worksheet('Raw data (Woocommerce)')
        pivot_sheet = spreadsheet.worksheet('Woocommerce Pivot table')

        num_rows = len(data_sheet.get_all_values())

        body = {
            "requests": [
                {
                    "updateCells": {
                        "range": {"sheetId": pivot_sheet.id},
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
                                            "endColumnIndex": 49
                                        },
                                        "rows": [
                                            {"sourceColumnOffset": 31, "showTotals": True, "sortOrder": "ASCENDING"}
                                        ],
                                        "columns": [
                                            {"sourceColumnOffset": 42, "showTotals": True, "sortOrder": "ASCENDING"}
                                        ],
                                        "values": [
                                            {"summarizeFunction": "SUM", "sourceColumnOffset": 40, "name": "Revenue"},
                                            {"summarizeFunction": "SUM", "sourceColumnOffset": 41, "name": "Shipping Price"},
                                            {"summarizeFunction": "SUM", "sourceColumnOffset": 32, "name": "Quantity"}
                                        ],
                                        "criteria": {
                                            "2": {"visibleByDefault": True}
                                        }
                                    }
                                }
                            ]
                        },
                        "start": {"sheetId": pivot_sheet.id, "rowIndex": 0, "columnIndex": 0},
                        "fields": "pivotTable"
                    }
                },
                {"updateSheetProperties": {
                    "properties": {"sheetId": pivot_sheet.id, "gridProperties": {"frozenColumnCount": 1}},
                    "fields": "gridProperties.frozenColumnCount"
                }}
            ]
        }

        spreadsheet.batch_update(body)
        return "Pivot table updated successfully"
    except Exception as e:
        return f"Error: {str(e)}"
