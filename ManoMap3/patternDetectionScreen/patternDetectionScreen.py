import customtkinter as ctk

def open_screen_for_pattern_detection(root, go_back_func, create_main_screen_func):
    # Close the current window
    root.destroy()

    # Create a new window
    patternDetectionScreen = ctk.CTk()
    patternDetectionScreen.title("ManoMap")
    patternDetectionScreen.geometry("1000x700")

    label_a = ctk.CTkLabel(patternDetectionScreen, text="Pattern Detection Screen", font=("Arial", 16))
    label_a.pack(pady=20)

    # Button to return to main screen
    back_button = ctk.CTkButton(patternDetectionScreen, text="Back", command=lambda: go_back_func(patternDetectionScreen, create_main_screen_func))
    back_button.pack(pady=10)

    patternDetectionScreen.mainloop()
