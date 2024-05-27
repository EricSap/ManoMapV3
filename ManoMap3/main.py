import customtkinter as ctk
from exportToExcelScreen.exportToExcelScreen import export_to_excel_screen
from patternDetectionScreen.patternDetectionScreen import open_screen_for_pattern_detection

from utils import go_back

def create_main_screen():
    app = ctk.CTk()
    app.title("CustomTkinter Application")
    app.geometry("1200x800")

    title_label = ctk.CTkLabel(app, text="Welcome to ManoMap", font=("Arial", 25, "bold"))
    title_label.pack(pady=20)

    instruction_label = ctk.CTkLabel(app, text="What would you like to do?", font=("Arial", 18))
    instruction_label.pack(pady=10)

    # Frame to hold buttons
    button_frame = ctk.CTkFrame(app)
    button_frame.pack(pady=20)

    button_a = ctk.CTkButton(button_frame, text="Pattern Detection", command=lambda: open_screen_for_pattern_detection(app, go_back, create_main_screen), width=100, height=75, font=("Arial",14, "bold"))
    button_a.grid(row=0, column=0, padx=20, pady=20)

    button_b = ctk.CTkButton(button_frame, text="Data analysis", command=lambda: export_to_excel_screen(app, go_back, create_main_screen), width=110, height=75, font=("Arial", 14, "bold"))
    button_b.grid(row=0, column=1, padx=20, pady=20)

    # main loop
    app.mainloop()

# Run the main screen
if __name__ == "__main__":
    create_main_screen()
