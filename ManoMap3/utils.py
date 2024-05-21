import os
from tkinter import filedialog
import customtkinter as ctk
import pandas as pd

def create_button(root, text, command, pady=10):
    button = ctk.CTkButton(root, text=text, command=command)
    button.pack(pady=pady)
    return button

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

def go_back(current_screen, create_main_screen_func):
    current_screen.destroy()
    create_main_screen_func()

def create_label(root, text, font=("Arial", 16), pady=20):
    label = ctk.CTkLabel(root, text=text, font=font)
    label.pack(pady=pady)
    return label

def import_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    return file_path

def display_excel_filename(root):
    file_path = import_excel_file()
    if file_path and os.path.isfile(file_path):  # Check if file_path is not empty and is a valid file
        filename = os.path.basename(file_path)
        label = ctk.CTkLabel(root, text="Selected Excel File: " + filename, font=("Arial", 12))
        label.pack(pady=10)
    else:
        print("No file selected.")