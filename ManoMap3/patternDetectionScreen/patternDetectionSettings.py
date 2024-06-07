import customtkinter as ctk
from CTkRangeSlider import *

def create_settings_frame(root):
    settings_frame = ctk.CTkFrame(root)
    settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Format for each setting: (label_text, from_, to)
    settings = [
        ("Visible sensors:", 1, 40)
    ]

    sliders = []

    for i, (label_text, from_, to) in enumerate(settings):
        value1 = ctk.IntVar()
        value2 = ctk.IntVar()
        value1.set(from_)
        value2.set(to)

        slider = CTkRangeSlider(settings_frame, from_=from_, to=to, variables=(value1, value2)) 
        slider.grid(row=i, column=2, padx=3, pady=5, sticky="ew")

        label = ctk.CTkLabel(settings_frame, text=label_text)
        label.grid(row=i, column=0, padx=3, pady=5)

        value_label1 = ctk.CTkEntry(settings_frame, width=40, textvariable=value1)
        value_label1.grid(row=i, column=1, padx=3, pady=5)

        value_label2 = ctk.CTkEntry(settings_frame, width=40, textvariable=value2)
        value_label2.grid(row=i, column=3, padx=3, pady=5)
        sliders.append(slider)

    # Create an input field for broken sensors
    broken_sensor_label = ctk.CTkLabel(settings_frame, text="Broken sensor:")
    broken_sensor_label.grid(row=len(settings), column=0, padx=3, pady=5)

    broken_sensor_entry1 = ctk.CTkEntry(settings_frame, width=40)
    broken_sensor_entry1.grid(row=len(settings), column=1, columnspan=1, padx=5, pady=5, sticky="w")

    broken_sensor_entry2 = ctk.CTkEntry(settings_frame, width=40)
    broken_sensor_entry2.grid(row=len(settings), column=2, columnspan=1, padx=5, pady=5, sticky="w")

    broken_sensor_entries = [broken_sensor_entry1, broken_sensor_entry2]

    return settings_frame, sliders, broken_sensor_entries 


def create_advanced_settings_frame(root):
    advanced_settings_frame = ctk.CTkFrame(root)
    advanced_settings_frame.pack(pady=10, padx=10, fill="both", expand=True)


    # Format for each setting: (label_text, from_, to, default_value)
    settings = [
        ("Detection threshold", 1, 20, 10),
        ("Minimum pattern length", 1, 10, 3),
        ("Maximum chunk size (s)", 1, 100, 50),
        ("Distance between sensors (mm)", 1, 50, 25),
    ]

    sliders = []

    for i, (label_text, from_, to, default_value) in enumerate(settings):
        label = ctk.CTkLabel(advanced_settings_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        value = ctk.IntVar()
        value.set(default_value)
        slider = ctk.CTkSlider(advanced_settings_frame, from_=from_, to=to, variable=value)
        slider.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        
        sliders.append(slider)

        value_label = ctk.CTkEntry(advanced_settings_frame, width=40, textvariable=value)
        value_label.grid(row=i, column=2, padx=5, pady=5)

    return advanced_settings_frame, sliders