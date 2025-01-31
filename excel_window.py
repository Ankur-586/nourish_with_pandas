import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import shutil
import os
from pathlib import Path
import datetime
import numpy as np
from utils import apply_gst_and_save


class GSTUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Updater Tool")
        self.root.geometry("500x300")

        # Set up GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="GST Updater Tool", font=("Helvetica", 16))
        self.title_label.pack(pady=20)

        # File Selection Button
        self.select_file_button = tk.Button(self.root, text="Select Excel File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # File Path Label
        self.file_path_label = tk.Label(self.root, text="No file selected", font=("Helvetica", 10))
        self.file_path_label.pack(pady=10)

        # Update GST Button
        self.update_button = tk.Button(self.root, text="Update GST", command=self.update_gst, state=tk.DISABLED)
        self.update_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 10))
        self.status_label.pack(pady=10)
        
        # Close Button (Initially hidden)
        self.close_button = tk.Button(self.root, text="Close", command=self.close_window, state=tk.DISABLED)
        self.close_button.pack(pady=10)

    def select_file(self):
        """File selection dialog"""
        selected_file = filedialog.askopenfilename(title="Select an Excel File", filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if selected_file:
            self.file_path_label.config(text=selected_file)
            self.selected_file = selected_file
            self.update_button.config(state=tk.NORMAL)
            self.status_label.config(text="File selected successfully. Ready to update GST.")

    def update_gst(self):
        """Update GST logic"""
        # Read the file path and perform the necessary operations
        try:
            selected_file = self.selected_file
            output_file_path = apply_gst_and_save(selected_file)
            # Show success message
            self.status_label.config(text=f"GST Update completed! File saved as {output_file_path}")
            messagebox.showinfo("Success", f"File saved successfully!\n{output_file_path}")
            
            # Enable Close button after successful operation
            self.close_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.DISABLED)
            
        except Exception as e:
            self.status_label.config(text="An error occurred during the update.")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def close_window(self):
        """Close the application window"""
        self.root.quit()  # Close the window

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = GSTUpdaterApp(root)
    root.mainloop()