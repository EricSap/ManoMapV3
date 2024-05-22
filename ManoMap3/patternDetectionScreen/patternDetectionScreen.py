import customtkinter as ctk
from utils import display_txt_filename, clear_screen
from patternDetectionScreen.patternDetectionSettings import create_settings_frame

def open_screen_for_pattern_detection(root, go_back_func, create_main_screen_func):
    clear_screen(root)

    # Create main frame for layout
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title 
    title_label = ctk.CTkLabel(main_frame, text="Pattern Detection", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    # Top Buttons
    button_select_input = ctk.CTkButton(main_frame, text="Select Input File", command=lambda: display_txt_filename(root))
    button_select_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    button_plot_data = ctk.CTkButton(main_frame, text="Plot Data", command=None)
    button_plot_data.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    #Settings Frame
    settings_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray")
    settings_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
    create_settings_frame(settings_frame)

    # Label for Settings frame
    sensors_label = ctk.CTkLabel(settings_frame, text="Settings", font=("Arial", 14, "bold"))
    sensors_label.pack(pady=10)

    # Advanced Settings Frame
    advanced_settings_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray")
    advanced_settings_frame.grid(row=2, column=1, columnspan=3, pady=20, padx=20, sticky="nsew")

    # Placeholder for Advanced Settings
    settings_label = ctk.CTkLabel(advanced_settings_frame, text="Advanced Settings", font=("Arial", 14, "bold"))
    settings_label.pack(pady=10)

    # Bottom Buttons
    button_detect_events = ctk.CTkButton(main_frame, text="Detect Events", command=None)
    button_detect_events.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    button_plot_signals = ctk.CTkButton(main_frame, text="Plot Signals", command=None)
    button_plot_signals.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    button_export = ctk.CTkButton(main_frame, text="Export", command=None)
    button_export.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

    button_back = ctk.CTkButton(main_frame, text="Back", command=lambda: go_back_func(root, create_main_screen_func))
    button_back.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

    # Buttons for plotting and detecting
    def showPlotPressed():
        try:
            global commentsDict
            slidervals = visibleSensorSlider.getValues()
            first_sensor = int(slidervals[0])
            last_sensor = int(slidervals[1])
            thresholdVals = thresholdSlider.getValues()
            minThreshold = int(thresholdVals[0])
            maxThreshold = int(thresholdVals[1])
            colormap = clicked.get()
            heatplot.showPlot(first_sensor, last_sensor, minThreshold, maxThreshold, differentialMode, valuesDict, commentsDict, colormap=colormap)
        except NameError:
            messagebox.showinfo("Error", "Please select a file.")

    # Configure grid weights for responsiveness
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)

