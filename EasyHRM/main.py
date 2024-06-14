import customtkinter as ctk
from exportToExcelScreen.exportToExcelScreen import export_to_excel_screen
from patternDetectionScreen.patternDetectionScreen import open_screen_for_pattern_detection
from utils import go_back, toggle_mode
import sys
import os
from PIL import Image

def create_main_screen():
    app = ctk.CTk()
    app.title("EasyHRM")
    app.geometry("1200x800")

    def resource_path(relative_path):
        """ Get the absolute path to the resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("../EasyHRM")

        return os.path.join(base_path, relative_path)

    icon_path = resource_path("EasyHRM_icon.ico")
    app.iconbitmap(icon_path)

    # Center the window on the screen
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 1200
    window_height = 800

    position_top = int(screen_height / 2 - window_height / 2) - 30
    position_right = int(screen_width / 2 - window_width / 2)

    app.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Main Frame
    main_frame = ctk.CTkFrame(app, corner_radius=0)  
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Container frame for title and logo
    title_logo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    title_logo_frame.pack(pady=20)

    # Title label
    title_label = ctk.CTkLabel(title_logo_frame, text="ManoMap", font=("Arial", 30, "bold"))
    title_label.pack(side="left", padx=10)

    # Logo
    logo_path = resource_path("EasyHRM_logo.png")
    logo_image = Image.open(logo_path)
    logo = ctk.CTkImage(logo_image, size=(75, 75))
    logo_label = ctk.CTkLabel(title_logo_frame, image=logo, text="")
    logo_label.pack(side="left", padx=10)

    # Description label
    description_text = (
        "Optimise your colon examination with our application! "
        "Automate the time-consuming process of identifying colon patterns. "
        "Save valuable time for examination and analysis, and improve the accuracy of your data."
    )
    description_label = ctk.CTkLabel(main_frame, text=description_text, font=("Arial", 14), wraplength=600, justify="center")
    description_label.pack(pady=25)

    # Instruction label
    instruction_label = ctk.CTkLabel(main_frame, text="What would you like to do?", font=("Arial", 18, "bold"))
    instruction_label.pack(pady=10)

    # Frame to hold buttons
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent") 
    button_frame.pack(pady=20)

    button_a = ctk.CTkButton(button_frame, text="Pattern Detection", command=lambda: open_screen_for_pattern_detection(app, go_back, create_main_screen), width=240, height=50, font=("Arial", 14, "bold"))
    button_a.pack(pady=10)

    button_b = ctk.CTkButton(button_frame, text="Data Analysis", command=lambda: export_to_excel_screen(app, go_back, create_main_screen), width=240, height=50, font=("Arial", 14, "bold"))
    button_b.pack(pady=10)

    # Mode toggle switch
    mode_toggle_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    mode_toggle_frame.pack(pady=20)
    
    initial_mode = ctk.get_appearance_mode().strip().lower() == "dark"
    mode_toggle = ctk.CTkSwitch(mode_toggle_frame, text="Light / Dark mode", command=toggle_mode, onvalue=1, offvalue=0, font=("Arial", 14, "bold"))
    mode_toggle.pack()
    mode_toggle.select() if initial_mode else mode_toggle.deselect()

    # main loop
    app.mainloop()

# Run the main screen
if __name__ == "__main__":
    create_main_screen()
