import customtkinter as ctk
from CTkRangeSlider import *
import tkinter

def create_settings_frame(root):
    settings_frame = ctk.CTkFrame(root)
    settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

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