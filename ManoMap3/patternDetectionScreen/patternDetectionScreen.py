import customtkinter as ctk
from utils import display_txt_filename, clear_screen, detectEventsPressed, clearEvents, showPlotPressed, showSignalsPressed, exportToXML, approximate_broken_sensor
from patternDetectionScreen.patternDetectionSettings import create_settings_frame, create_advanced_settings_frame
import patternDetectionScreen.heatplot as heatplot
from patternDetectionScreen.detect_and_export import import_txt_file_detection, compute_patterns, exportToXML_2

def open_screen_for_pattern_detection(root, go_back_func, create_main_screen_func):
    clear_screen(root)

    # Create main frame for layout
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title 
    title_label = ctk.CTkLabel(main_frame, text="Pattern Detection", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    # Top Buttons
    button_select_input = ctk.CTkButton(main_frame, text="Select Input File", command=lambda: import_txt_file_detection(button_export, file_label))
    button_select_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    file_label = ctk.CTkLabel(main_frame, text="No file selected", font=("Arial", 12))
    file_label.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

    # button_plot_data = ctk.CTkButton(main_frame, text="Plot Data", command= lambda: showPlotPressed(sliders))
    # button_plot_data.grid(row=1, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

    #Settings Frame
    settings_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray", width=400)
    settings_frame.grid(row=2, column=0, columnspan=1, pady=20, padx=20, sticky="nsew")
    settings_frame_2, sliders, broken_sensor_entries = create_settings_frame(settings_frame)

    # Label for Settings frame
    settings_label = ctk.CTkLabel(settings_frame, text="Settings", font=("Arial", 14, "bold"))
    settings_label.pack(pady=10)

    # Advanced Settings Frame
    advanced_settings_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray", width=400)
    advanced_settings_frame.grid(row=2, column=1, columnspan=3, pady=20, padx=20, sticky="nsew")
    advanced_settings_frame_2, advanced_sliders = create_advanced_settings_frame(advanced_settings_frame)

    # Placeholder for Advanced Settings
    settings_label = ctk.CTkLabel(advanced_settings_frame, text="Advanced Settings", font=("Arial", 14, "bold"))
    settings_label.pack(pady=10)

    # Bottom Buttons
    button_detect_events = ctk.CTkButton(main_frame, text="Detect Events", command=lambda: compute_patterns())
    button_detect_events.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    button_detect_events = ctk.CTkButton(main_frame, text="Clear events", command=clearEvents)
    button_detect_events.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    button_plot_signals = ctk.CTkButton(main_frame, text="Plot Signals", command=lambda: showSignalsPressed(sliders))
    button_plot_signals.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

    button_export = ctk.CTkButton(main_frame, text="Export", command=lambda: exportToXML_2(), state='disabled')
    button_export.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

    button_back = ctk.CTkButton(main_frame, text="Back", command=lambda: go_back_func(root, create_main_screen_func))
    button_back.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    button_approximate = ctk.CTkButton(main_frame, text="Approximate broken sensors", command=lambda: approximate_broken_sensor(broken_sensor_entries))
    button_approximate.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Configure grid weights for responsiveness
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
