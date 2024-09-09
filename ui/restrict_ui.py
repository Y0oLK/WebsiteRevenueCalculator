# ui/restrict_ui.py

import tkinter as tk
from tkinter import filedialog
from services.restrict_upload_data import upload_restrict_data  # Correct import
from services.restrict_pivot_table import update_pivot_table

class RestrictUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="Restrict Operations", wraplength=300, justify="left")
        self.status_label.pack(pady=10)

        self.processing_label = tk.Label(self, text="", wraplength=300, justify="left", fg="blue")
        self.processing_label.pack(pady=10)

        # Create the update pivot table button
        update_button = tk.Button(self, text="Update Pivot Table", command=self.on_update_button_click)
        update_button.pack(pady=10)

        # Create the upload data button
        upload_button = tk.Button(self, text="Upload Data", command=self.on_upload_button_click)
        upload_button.pack(pady=10)

    def on_update_button_click(self):
        """
        Handles the event when the 'Update Pivot Table' button is clicked.
        Updates the pivot table in Google Sheets.
        """
        def update_pivot():
            self.status_label.config(text="Updating Pivot Table...")
            try:
                spreadsheet_id = '1WvHJWyuSa2LUqZrY7yDijsj0g0L3oTGvp8Tr6hAa0lE'
                result = update_pivot_table(spreadsheet_id)
                self.status_label.config(text=result)
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
            self.processing_label.config(text="")

        self.status_label.config(text="Processing...")
        self.processing_label.config(text="Please wait...")
        self.after(100, update_pivot)

    def on_upload_button_click(self):
        """
        Handles the event when the 'Upload Data' button is clicked.
        Opens a file dialog to select a CSV file and uploads its data to Google Sheets.
        """
        def upload_data(file_path):
            self.status_label.config(text="Uploading Data...")
            try:
                upload_restrict_data(file_path)
                self.status_label.config(text="Data uploaded successfully.")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
            self.processing_label.config(text="")

        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Select a CSV file"
        )
        if file_path:
            self.status_label.config(text="Processing...")
            self.processing_label.config(text="Please wait...")
            self.after(100, upload_data, file_path)
