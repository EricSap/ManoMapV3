import customtkinter as ctk
from CTkRangeSlider import *
import tkinter

def create_settings_frame(root):
    settings_frame = ctk.CTkFrame(root)
    settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Format for each setting: (label_text, from_, to)
    settings = [
        ("Threshold:", 0, 500),
        ("Visible sensors:", 1, 40)
    ]

    sliders = []

    for i, (label_text, from_, to) in enumerate(settings):
        label = ctk.CTkLabel(settings_frame, text=label_text)
        label.grid(row=i, column=0, padx=3, pady=5)

        value_label1 = ctk.CTkLabel(settings_frame, text="")
        value_label1.grid(row=i, column=1, padx=3, pady=5)

        value_label2 = ctk.CTkLabel(settings_frame, text="")
        value_label2.grid(row=i, column=3, padx=5, pady=5)

        def update_value_label(value, label1=value_label1, label2=value_label2):
            label1.configure(text=f"{int(round(value[0]))}")
            label2.configure(text=f"{int(round(value[1]))}")
        
        slider = CTkRangeSlider(settings_frame, from_=from_, to=to, command=update_value_label) 
        slider.grid(row=i, column=2, padx=5, pady=5, sticky="ew")
                
        sliders.append(slider)

        # Call the update_value_labels function with the initial values of the slider
        update_value_label((from_, to))

    # Create an input field for broken sensors
    broken_sensor_label = ctk.CTkLabel(settings_frame, text="Broken sensor:")
    broken_sensor_label.grid(row=len(settings), column=0, padx=3, pady=5)

    broken_sensor_entry = ctk.CTkEntry(settings_frame)
    broken_sensor_entry.grid(row=len(settings), column=1, columnspan=3, padx=5, pady=5, sticky="ew")
    return settings_frame, sliders, broken_sensor_entry


def create_advanced_settings_frame(root):
    advanced_settings_frame = ctk.CTkFrame(root)
    advanced_settings_frame.pack(pady=10, padx=10, fill="both", expand=True)


    # Format for each setting: (label_text, from_, to, default_value)
    settings = [
        ("Distance between sensors (mm)", 1, 200, 25),
        ("Amount of overlapped sensors", 1, 7, 2),
        ("Amount of sensors", 1 , 7, 2),
        ("Granularity", 1, 100, 10),
        ("Detection threshold", 1, 50, 10),
        ("Line opacity (%)", 20, 100, 100)
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

        value_label = ctk.CTkLabel(advanced_settings_frame, textvariable=value)
        value_label.grid(row=i, column=2, padx=5, pady=5)

    return advanced_settings_frame, sliders