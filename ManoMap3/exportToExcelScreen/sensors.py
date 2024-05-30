import customtkinter as ctk
from CTkRangeSlider import *

def create_sensors_frame(root):
    sensors_frame = ctk.CTkFrame(root)
    sensors_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Format for each setting: (label_text, from_, to, start_value, end_value)
    colonregions = [
        ("Ascending:", 1, 40, 1, 32),
        ("Transverse:", 1, 40, 33, 34),
        ("Descending:", 1, 40, 35, 36),
        ("Sigmoid:", 1, 40, 37, 38),
        ("Rectum:", 1, 40, 39, 40)
    ]
    sliders = []
    value_labels = []

    # Format for each setting: (label_text, from_, to, default_value)
    settings = [
        ("Distance between sensors (mm)", 1, 200, 25),
    ]

    for i, (label_text, from_, to, start_value, end_value) in enumerate(colonregions):
        label = ctk.CTkLabel(sensors_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        value_label = ctk.CTkLabel(sensors_frame, text="")
        value_label.grid(row=i, column=2, padx=5, pady=5)

        value_labels.append(value_label)

        def update_value_label(value, label=value_label, i=i):
            if(value[0] < value[1]):
                start, end = int(round(value[0], 0)), int(round(value[1], 0))
                label.configure(text=(start, end))

                # Update the next slider's start value
                if i < len(sliders) - 1 and end < sliders[i + 1].get()[1]:
                    sliders[i + 1].set([end + 1, sliders[i + 1].get()[1]])
                    value_labels[i + 1].configure(text=(int(end + 1), int(sliders[i + 1].get()[1])))

                # Update the previous slider's end value
                if i > 0:
                    prev_start, prev_end = sliders[i - 1].get()
                    if start <= prev_end:
                        sliders[i - 1].set([prev_start, start - 1])
                        value_labels[i - 1].configure(text=(int(prev_start), int(start - 1)))

        slider = CTkRangeSlider(sensors_frame, from_=from_, to=to, command=update_value_label)
        slider.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        slider.set([start_value, end_value])
        
        # Call the update_value_label function with the initial values of the slider
        update_value_label((slider.get()[0], slider.get()[1]))
        sliders.append(slider)


    settings_sliders = []
    for i, (label_text, from_, to, default_value) in enumerate(settings):
        row_index = i + len(colonregions)
        label = ctk.CTkLabel(sensors_frame, text=label_text)
        label.grid(row=row_index, column=0, padx=5, pady=5)

        value = ctk.IntVar()
        value.set(default_value)
        slider = ctk.CTkSlider(sensors_frame, from_=from_, to=to, variable=value)
        slider.grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")
        
        settings_sliders.append(slider)

        value_label = ctk.CTkLabel(sensors_frame, textvariable=value)
        value_label.grid(row=row_index, column=2, padx=5, pady=5)

    return sliders, settings_sliders
