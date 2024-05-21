import customtkinter as ctk

def create_sensors_frame(root):
    sensors_frame = ctk.CTkFrame(root)
    sensors_frame.pack(pady=10, padx=10, fill="both", expand=True)

    sensors = [
        ("Visible sensors:", 1, 40),
        ("Colon/Regions:", 1, 40),
        ("Transverse:", 1, 20),
        ("Descending:", 1, 30),
        ("Sigmoid:", 1, 35),
        ("Rectum:", 1, 40)
    ]

    for i, (label_text, from_, to) in enumerate(sensors):
        label = ctk.CTkLabel(sensors_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)
        slider = ctk.CTkSlider(sensors_frame, from_=from_, to=to)
        slider.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

    return sensors_frame