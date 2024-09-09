import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ui.woocommerce_ui import WooCommerceUI
from ui.restrict_ui import RestrictUI


def run_main_ui():
    """
    Creates and runs the main Tkinter window with tabbed WooCommerce and Restrict functionality.
    """
    root = tk.Tk()
    root.title("Website Revenue Calculator")
    root.geometry("500x300")

    # Set the background color of the window
    background_color = "#FFA500"  # You can choose any color you like
    root.configure(bg=background_color)

    # Load and set the window icon
    try:
        logo_image = Image.open("logo/logo.jpg")
        logo_photo = ImageTk.PhotoImage(logo_image)
        root.iconphoto(True, logo_photo)
    except FileNotFoundError:
        print("Error: The file 'logo/logo.jpg' was not found.")



    # Create a Notebook and set its background color
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    notebook.configure(style='TNotebook')

    # Create a style for the Notebook to set its background color
    style = ttk.Style()
    style.configure('TNotebook', background=background_color)
    style.configure('TNotebook.Tab', background=background_color, foreground='black')

    # Add the WooCommerce and Restrict tabs
    notebook.add(WooCommerceUI(notebook), text="WooCommerce")
    notebook.add(RestrictUI(notebook), text="Restrict")

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    run_main_ui()
