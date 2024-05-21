import customtkinter as ctk
from exportToExcelScreen.exportToExcelScreen import export_to_excel_screen
from patternDetectionScreen.patternDetectionScreen import open_screen_for_pattern_detection

from utils import go_back

def create_main_screen():
    app = ctk.CTk()
    app.title("CustomTkinter Application")
    app.geometry("500x300")

    title_label = ctk.CTkLabel(app, text="What do you like to do?", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Frame to hold buttons
    button_frame = ctk.CTkFrame(app)
    button_frame.pack()

    button_a = ctk.CTkButton(button_frame, text="Automatic Pattern Detection", command=lambda: open_screen_for_pattern_detection(app, go_back, create_main_screen), width=25)
    button_a.grid(row=0, column=0, padx=5, pady=10)

    button_b = ctk.CTkButton(button_frame, text="Export file to Excel", command=lambda: export_to_excel_screen(app, go_back, create_main_screen), width=25)
    button_b.grid(row=0, column=1, padx=5, pady=10)

    # main loop
    app.mainloop()

# Run the main screen
if __name__ == "__main__":
    create_main_screen()
