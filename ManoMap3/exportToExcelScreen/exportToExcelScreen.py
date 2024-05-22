import customtkinter as ctk
from utils import display_excel_filename, clear_screen
from exportToExcelScreen.events import create_event_frame
from exportToExcelScreen.sensors import create_sensors_frame
from exportToExcelScreen.plotData import plot_topographic_data

def export_to_excel_screen(root, go_back_func, create_main_screen_func):
    clear_screen(root)

    # Create main frame for layout
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title Label
    title_label = ctk.CTkLabel(main_frame, text="Export to Excel", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    # Top Buttons
    button_select_input = ctk.CTkButton(main_frame, text="Select Input File", command=lambda: display_excel_filename(root))
    button_select_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    button_plot_data = ctk.CTkButton(main_frame, text="Plot Data", command=lambda:plot_topographic_data())
    button_plot_data.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

    # Sensors Frame
    sensors_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray")
    sensors_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
    create_sensors_frame(sensors_frame)

    # Placeholder for Sensor frame
    sensors_label = ctk.CTkLabel(sensors_frame, text="Sensors", font=("Arial", 14, "bold"))
    sensors_label.pack(pady=10)

    # Events Frame
    events_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray")
    events_frame.grid(row=2, column=1, columnspan=3, pady=20, padx=20, sticky="nsew")
    create_event_frame(events_frame)

    # Placeholder for Events frame
    events_label = ctk.CTkLabel(events_frame, text="Events", font=("Arial", 14, "bold"))
    events_label.pack(pady=10)

    # Bottom Buttons
    button_export = ctk.CTkButton(main_frame, text="Export", command=None)
    button_export.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

    button_back = ctk.CTkButton(main_frame, text="Back", command=lambda: go_back_func(root, create_main_screen_func))
    button_back.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

    # Configure grid weights for responsiveness
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
