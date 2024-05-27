import customtkinter as ctk
from manoutilsv2 import *

commentsDict = {}

def show_info_popup(title, message, root):
    # Create a popup window
    popup = ctk.CTkToplevel()
    popup.title(title)

    # Make the popup transient, so it stays on top of the root window
    popup.transient(root)

    # Create a label to display the message
    message_label = ctk.CTkLabel(popup, text=message)
    message_label.pack(padx=20, pady=10)

    # Create a button to close the popup
    close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

def placeComment(settings_frame):
    global commentsDict, hourText, minText, secText, commentText  # Add hourText, minText, secText, commentText as globals
    time = get_time_text()
    print(time)
    comment = commentText.get()
    if validateTime(time):
        commentsDict[convertTime(time)] = comment
        show_info_popup("Event", f"Event placed at {time}", settings_frame)
    else:
        show_info_popup("Error", "You must enter the right format of time (HH:MM:SS)", settings_frame)
    commentText.delete(0, ctk.END)

def create_event_interface(settings_frame):
    global hourText, minText, secText, commentText  # Declare globals

    # Time and Comment Frame
    timecommentBundle = ctk.CTkFrame(settings_frame)
    timecommentBundle.pack(padx=20, pady=20)

    # Create a frame to contain comments
    settings_frame.comments_frame = ctk.CTkFrame(settings_frame)
    settings_frame.comments_frame.pack(padx=1, pady=1)
    
    # Event Label
    commentText = ctk.StringVar()
    event_label = ctk.CTkLabel(timecommentBundle, textvariable=commentText)
    commentText.set("Event")
    event_label.pack()

    # Comment Entry
    commentText = ctk.CTkEntry(timecommentBundle, width=300, placeholder_text="Event")
    commentText.pack(padx=2)

    # Time Label
    timeText = ctk.StringVar()
    time_label = ctk.CTkLabel(timecommentBundle, textvariable=timeText)
    timeText.set("Time")
    time_label.pack()

    # Hour Entry
    hourText = ctk.CTkEntry(timecommentBundle, width=40, placeholder_text="HH")
    hourText.pack(side=ctk.LEFT, padx=2)

    # Separator
    colon1 = ctk.CTkLabel(timecommentBundle, text=":")
    colon1.pack(side=ctk.LEFT, padx=2)

    # Minute Entry
    minText = ctk.CTkEntry(timecommentBundle, width=40, placeholder_text="MM")
    minText.pack(side=ctk.LEFT, padx=2)

    # Separator
    colon2 = ctk.CTkLabel(timecommentBundle, text=":")
    colon2.pack(side=ctk.LEFT, padx=2)

    # Second Entry
    secText = ctk.CTkEntry(timecommentBundle, width=40, placeholder_text="SS")
    secText.pack(side=ctk.LEFT, padx=2)

    # Place Event Button
    placeCommentButton = ctk.CTkButton(settings_frame, text="Place Event", command=lambda: (placeComment(settings_frame), show_comments(settings_frame)))
    placeCommentButton.pack(pady=10, padx=10)
    return hourText, minText, secText, commentText

def get_time_text():
    # Get the content of each Entry widget and strip any extra whitespace
    hour = hourText.get().strip()
    minute = minText.get().strip()
    second = secText.get().strip()
    
    # Combine the time components
    time_text = f"{hour}:{minute}:{second}"
    return time_text

def delete_comment(key, label, settings_frame):
    del commentsDict[key]
    label.destroy()
    # Refresh comments frame
    show_comments(settings_frame)

def show_comments(settings_frame):
    # Clear existing comments frame
    for widget in settings_frame.comments_frame.winfo_children():
        widget.destroy()

    # Show comments
    for key, value in commentsDict.items():
        comment_frame = ctk.CTkFrame(settings_frame.comments_frame)
        comment_frame.pack(pady=5, fill='x')

        timeAndCommentText = ctk.CTkLabel(comment_frame, text=f"Time: {convertTimeToText(key)} - Comment: {value}")
        timeAndCommentText.pack(side='left')

        delete_button = ctk.CTkButton(comment_frame, text="Delete", command=lambda k=key, lbl=timeAndCommentText, sf=settings_frame: delete_comment(k, lbl, sf))
        delete_button.pack(side='right')
    return commentsDict
