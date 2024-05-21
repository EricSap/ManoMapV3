import customtkinter as ctk
from utils import display_excel_filename


def export_to_excel_screen(root, go_back_func, create_main_screen_func):
    # Close the current window
    root.destroy()

    # Create a new window for Screen B
    screen_b = ctk.CTk()
    screen_b.title("ManoMap")
    screen_b.geometry("1000x700")

    label_b = ctk.CTkLabel(screen_b, text="Export To Excel screen", font=("Arial", 16))
    label_b.pack(pady=20)

    # Button to select input file
    select_file_button = ctk.CTkButton(screen_b, text="Select Input File", command=lambda: display_excel_filename(screen_b))
    select_file_button.pack(pady=10)

    # Button to return to main screen
    back_button = ctk.CTkButton(screen_b, text="Back", command=lambda: go_back_func(screen_b, create_main_screen_func))
    back_button.pack(pady=10)

    screen_b.mainloop()
