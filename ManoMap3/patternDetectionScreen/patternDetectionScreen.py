import customtkinter as ctk
from utils import display_txt_filename, clear_screen, detectEvents, clearEvents, showPlotPressed
from patternDetectionScreen.patternDetectionSettings import create_settings_frame, create_advanced_settings_frame
import patternDetectionScreen.heatplot as heatplot

# global valuesDict

# commentsDict = dict()
# contractions = []
# exportDataXml = []
# differentialMode = False

# def showPlotPressed(sliders):
#     try:
#         global commentsDict
#         thresholdVals = list(sliders[0].get())
#         visible_sensors = list(sliders[1].get())
#         print("visible sensors: ",visible_sensors)
#         print("type; ",type(visible_sensors))
#         first_sensor = visible_sensors[0]
#         last_sensor = visible_sensors[1]
#         minThreshold = thresholdVals[0]
#         maxThreshold = thresholdVals[1]
#         colormap = "inferno"
#         heatplot.showPlot(first_sensor, last_sensor, minThreshold, maxThreshold, differentialMode, valuesDict, commentsDict, colormap=colormap)
#     except NameError:
#         # messagebox.showinfo("Error", "Please select a file.")
#         print("Please select a file.")

def test_advanced_sliders(sliders):
    for slider in sliders:
        print(int(slider.get()))

def open_screen_for_pattern_detection(root, go_back_func, create_main_screen_func):
    clear_screen(root)

    # Create main frame for layout
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title 
    title_label = ctk.CTkLabel(main_frame, text="Pattern Detection", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    #Settings Frame
    settings_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray")
    settings_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
    settings_frame_2, sliders = create_settings_frame(settings_frame)

    # Label for Settings frame
    settings_label = ctk.CTkLabel(settings_frame, text="Settings", font=("Arial", 14, "bold"))
    settings_label.pack(pady=10)
    
    # Top Buttons
    button_select_input = ctk.CTkButton(main_frame, text="Select Input File", command=lambda: display_txt_filename(root))
    button_select_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    button_plot_data = ctk.CTkButton(main_frame, text="Plot Data", command= lambda: showPlotPressed(sliders))
    button_plot_data.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    # Advanced Settings Frame
    advanced_settings_frame = ctk.CTkFrame(main_frame, border_width=1, border_color="gray")
    advanced_settings_frame.grid(row=2, column=1, columnspan=3, pady=20, padx=20, sticky="nsew")
    advanced_settings_frame_2, advanced_sliders = create_advanced_settings_frame(advanced_settings_frame)

    # Placeholder for Advanced Settings
    settings_label = ctk.CTkLabel(advanced_settings_frame, text="Advanced Settings", font=("Arial", 14, "bold"))
    settings_label.pack(pady=10)

    # Bottom Buttons
    button_detect_events = ctk.CTkButton(main_frame, text="Detect Events", command=detectEvents)

    button_detect_events.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    button_detect_events = ctk.CTkButton(main_frame, text="Clear events", command=clearEvents)
    button_detect_events.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    button_plot_signals = ctk.CTkButton(main_frame, text="Plot Signals", command=None)
    button_plot_signals.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

    button_export = ctk.CTkButton(main_frame, text="Export", command=None)
    button_export.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

    button_back = ctk.CTkButton(main_frame, text="Back", command=lambda: go_back_func(root, create_main_screen_func))
    button_back.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    # Configure grid weights for responsiveness
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)