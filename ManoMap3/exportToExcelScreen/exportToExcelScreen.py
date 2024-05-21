import customtkinter as ctk
from utils import display_excel_filename, clear_screen, create_button, create_label
from exportToExcelScreen.events import create_event_frame
from exportToExcelScreen.sensors import create_sensors_frame

def export_to_excel_screen(root, go_back_func, create_main_screen_func):
    clear_screen(root)

    create_label(root, "Export to Excel")

    create_button(root, "Select Input File", command=lambda: display_excel_filename(root))
    create_button(root, "Plot Data", command=None)

    create_sensors_frame(root)
    create_event_frame(root)

    create_button(root, "Export", command=None)
    create_button(root, "Back", command=lambda: go_back_func(root, create_main_screen_func))
