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

    def update_value_label(value, i):
        start, end = int(round(value[0], 0)), int(round(value[1], 0))
        value_labels[i][0].configure(text=f"{start}")
        value_labels[i][1].configure(text=f"{end}")

        # Update the next slider's start value
        if i < len(sliders) - 1 and end < sliders[i + 1].get()[1]:
            sliders[i + 1].set([end + 1, sliders[i + 1].get()[1]])
            value_labels[i + 1][0].configure(text=f"{end + 1}")
            value_labels[i + 1][1].configure(text=f"{int(sliders[i + 1].get()[1])}")

        # Update the previous slider's end value
        if i > 0:
            prev_start, prev_end = sliders[i - 1].get()
            if start <= prev_end:
                sliders[i - 1].set([prev_start, start - 1])
                value_labels[i - 1][0].configure(text=f"{int(prev_start)}")
                value_labels[i - 1][1].configure(text=f"{start - 1}")

    for i, (label_text, from_, to, start_value, end_value) in enumerate(colonregions):
        label = ctk.CTkLabel(sensors_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        # Value label to the left of the slider
        value_label1 = ctk.CTkLabel(sensors_frame, text="")
        value_label1.grid(row=i, column=1, padx=5, pady=5)

        # Slider
        slider = CTkRangeSlider(sensors_frame, from_=from_, to=to, command=lambda value, i=i: update_value_label(value, i))
        slider.grid(row=i, column=2, padx=5, pady=5, sticky="ew")
        slider.set([start_value, end_value])
        sliders.append(slider)

        # Value label to the right of the slider
        value_label2 = ctk.CTkLabel(sensors_frame, text="")
        value_label2.grid(row=i, column=3, padx=5, pady=5)

        # Append the tuple of value labels
        value_labels.append((value_label1, value_label2))

        # Call the update_value_label function with the initial values of the slider
        update_value_label((slider.get()[0], slider.get()[1]), i)

    return sliders
