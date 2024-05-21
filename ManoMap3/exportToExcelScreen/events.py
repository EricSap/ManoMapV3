import customtkinter as ctk

def create_event_frame(root):
    event_frame = ctk.CTkFrame(root)
    event_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Event Label and Entry
    event_label = ctk.CTkLabel(event_frame, text="Event")
    event_label.grid(row=0, column=0, padx=5, pady=5)
    event_entry = ctk.CTkEntry(event_frame)
    event_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    # Time Label and Entry
    time_label = ctk.CTkLabel(event_frame, text="Time")
    time_label.grid(row=0, column=1, padx=5, pady=5)
    time_entry = ctk.CTkEntry(event_frame, placeholder_text="HH:MM:SS")
    time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # Add Event Button
    add_event_button = ctk.CTkButton(event_frame, text="Add event")
    add_event_button.grid(row=1, column=2, padx=5, pady=5)

    return event_frame



