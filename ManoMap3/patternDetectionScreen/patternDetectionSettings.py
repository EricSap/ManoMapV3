import customtkinter as ctk

def create_settings_frame(root):
    sensors_frame = ctk.CTkFrame(root)
    sensors_frame.pack(pady=10, padx=10, fill="both", expand=True)

    settings = [
        ("Threshhold:", 0, 500),
        ("Visible sensors:", 1, 40)
    ]

    for i, (label_text, from_, to) in enumerate(settings):
        label = ctk.CTkLabel(sensors_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)
        slider = ctk.CTkSlider(sensors_frame, from_=from_, to=to)
        slider.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

    return sensors_frame