import customtkinter as ctk
from CTkRangeSlider import *

def create_sensors_frame(root):
    sensors_frame = ctk.CTkFrame(root)
    sensors_frame.pack(pady=10, padx=10, fill="both", expand=True)

    colonregions = [
        ("Ascending:", 1, 40),
        ("Transverse:", 1, 40),
        ("Descending:", 1, 40),
        ("Sigmoid:", 1, 40),
        ("Rectum:", 1, 40)
    ]

    sliders = []

    for i, (label_text, from_, to) in enumerate(colonregions):
        label = ctk.CTkLabel(sensors_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        value_label = ctk.CTkLabel(sensors_frame, text="")
        value_label.grid(row=i, column=2, padx=5, pady=5)

        def update_value_label(value, label=value_label):
            label.configure(text=tuple(int(round(x, 0)) for x in value))

        slider = CTkRangeSlider(sensors_frame, from_=from_, to=to, command=update_value_label)
        slider.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        
        # Call the update_value_label function with the initial values of the slider
        update_value_label((from_, to))

        sliders.append(slider)

    return sliders
