import tkinter as tk
from tkinter import filedialog
import threading
from services.woocommerce_pivot_table import update_woocommerce_pivot_table
from services.woocommerce_upload_data import upload_woocommerce_data

class WooCommerceUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="WooCommerce Operations", wraplength=300, justify="left")
        self.status_label.pack(pady=10)

        self.processing_label = tk.Label(self, text="", wraplength=300, justify="left", fg="blue")
        self.processing_label.pack(pady=10)

        # Create the buttons
        tk.Button(self, text="Update Pivot Table", command=self.on_update_button_click).pack(pady=10)
        tk.Button(self, text="Upload Data", command=self.on_upload_button_click).pack(pady=10)

    def on_update_button_click(self):
        """
        Handles the event when the 'Update Pivot Table' button is clicked.
        Updates the pivot table in Google Sheets.
        """
        def update_pivot_table():
            self.status_label.config(text="Updating Pivot Table...")
            try:
                spreadsheet_id = '1WvHJWyuSa2LUqZrY7yDijsj0g0L3oTGvp8Tr6hAa0lE'  # Replace with your spreadsheet ID
                result = update_woocommerce_pivot_table(spreadsheet_id)
                self.status_label.config(text=result)
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
            self.processing_label.config(text="")

        self.status_label.config(text="Processing...")
        self.processing_label.config(text="Please wait...")
        threading.Thread(target=update_pivot_table).start()

    def on_upload_button_click(self):
        """
        Handles the event when the 'Upload Data' button is clicked.
        Prompts the user to select a file and uploads the data.
        """
        def upload_data(file_path):
            self.status_label.config(text="Uploading Data...")
            try:
                upload_woocommerce_data(file_path)
                self.status_label.config(text="Data uploaded and formulas added successfully.")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
            self.processing_label.config(text="")

        file_path = filedialog.askopenfilename(
            title="Select the file to upload",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            self.status_label.config(text="Processing...")
            self.processing_label.config(text="Please wait...")
            threading.Thread(target=upload_data, args=(file_path,)).start()
        else:
            self.status_label.config(text="No file selected.")
