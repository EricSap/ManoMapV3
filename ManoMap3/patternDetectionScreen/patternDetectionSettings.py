import customtkinter as ctk
from CTkRangeSlider import *
import tkinter

def create_settings_frame(root):
    settings_frame = ctk.CTkFrame(root)
    settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Format for each setting: (label_text, from_, to)
    settings = [
        ("Threshhold:", 0, 500),
        ("Visible sensors:", 1, 40)
    ]

    sliders = []

    for i, (label_text, from_, to) in enumerate(settings):
        label = ctk.CTkLabel(settings_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        value_label = ctk.CTkLabel(settings_frame, text="")
        value_label.grid(row=i, column=2, padx=5, pady=5)

        def update_value_label(value, label=value_label):
            label.configure(text=tuple(int(round(x, 0)) for x in value))
        
        slider = CTkRangeSlider(settings_frame, from_=from_, to=to, command=update_value_label)
        slider.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                
        sliders.append(slider)

        # Call the update_value_label function with the initial values of the slider
        update_value_label((from_, to))
    return settings_frame, sliders

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