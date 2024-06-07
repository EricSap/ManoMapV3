import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom


global filename
global file_path

commentsDict = dict()
contractions = []
exportDataXml = []
differentialMode = False

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

def go_back(current_screen, create_main_screen_func):
    current_screen.destroy()
    create_main_screen_func()

def toggle_mode():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Light":
        new_mode = "dark"
    else:
        new_mode = "Light"
    ctk.set_appearance_mode(new_mode)

# valideer time fields
def validateTime(input):
    try:
        parts = input.split(":")
    except:
        return False
    if len(parts) != 3:
        return False
    try:
        hours, minutes, seconds = map(int, parts)
        if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
            return True
    except ValueError:
        pass
    return False

#convert HH:MM:SS naar  x deciseconden
def convertTime(input):
    parts = input.split(":")
    total = 0
    try:
        total = int(parts[0])*60
        total = (total + int(parts[1])) * 60
        total = (total + int(parts[2])) * 10
    except:
        print("fout in omzetten")
    return total

def convertTimeToText(input):
    total_seconds = input // 10  # Convert deciseconds to seconds
    hours, remainder = divmod(total_seconds, 3600)  # Calculate hours
    minutes, seconds = divmod(remainder, 60)  # Calculate minutes and seconds

    # Format the time as 'HH:MM:SS'
    time_format = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

    return time_format

def clearEvents():
        global contractions
        contractions = []
        messagebox.showinfo("detection", "Events cleared!")

def approximate_broken_sensor(broken_sensor_entries):
     # Read the data from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize an empty list to hold the processed data
    data = []
    
    # Process each line in the file
    for line in lines:
        if line.strip():  # Skip any empty lines
            parts = line.split()
            time = float(parts[0])  # Convert the first column to float for time
            sensors = list(map(int, parts[1:]))  # Convert the rest to integers for sensor values
            data.append([time] + sensors)
    
    # Convert the list to a numpy array for easier manipulation
    data = np.array(data, dtype=object)
    
    for broken_sensor in broken_sensor_entries:
        print(broken_sensor_entries)
        if not broken_sensor.get().strip(' ') == '':
            broken_sensor_index = int(broken_sensor.get())
            # Replace the broken sensor values with the average of the previous and next sensor values
            for row in data:
                if broken_sensor_index == 1:
                    row[broken_sensor_index] = row[broken_sensor_index + 1]
                elif broken_sensor_index == len(row) - 1:
                    row[broken_sensor_index] = row[broken_sensor_index - 1]
                else:
                    row[broken_sensor_index] = int(round((row[broken_sensor_index-1] + row[broken_sensor_index + 1]) / 2))

    # Prompt the user to select where to save the new file
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile = f"{filename.split('.txt')[0]}_approximated.txt")
    
    # Save the modified data back to the file or return it
    with open(save_path, 'w') as file:
        for row in data:
            file.write(f"{row[0]:.1f} " + ' '.join(map(str, map(int, row[1:]))) + '\n')

    print(f"File saved as: {save_path}")

def process_sequences(data):
    sequences = []

    for sequence in data:
        # Extract start and end samples
        start_sample = sequence[0][0]
        end_sample = sequence[-1][0]

        # Extract start and end sensors (channels)
        start_sensor = sequence[0][1]
        end_sensor = sequence[-1][1]

        # Create a new sequence dictionary
        seq_dict = {
            "startSample": start_sample * 10,
            "endSample": end_sample * 10,
            "startChannel": int(start_sensor.split('_')[1]) - 2,
            "endChannel": int(end_sensor.split('_')[1]) - 2,
            "ranges": []
        }

        # Add range data
        for entry in sequence:
            sample, sensor, _ = entry
            channel = int(sensor.split('_')[1]) -2
            seq_dict["ranges"].append({
                "channel": channel,
                "maxSample": sample * 10
            })

        sequences.append(seq_dict)

    return sequences

def sequences_to_xml(sequences):
    root = ET.Element("sequences")

    for seq in sequences:
        # print("sequences: ", seq)
        time = int((seq["endSample"]) - int(seq["startSample"]))
        if (time == 0):
            velocity = "INF"
            dir = 'Synchronous'
        else:
            velocity = ((int(seq["endChannel"]) - int(seq["startChannel"])) * 25 ) / (time / 10)
            if int(velocity) > 0:
                dir = 'Antegrade'
            elif int(velocity) < 0:
                dir = 'Retrograde'

        # print("velocity: ", velocity)
        seq_elem = ET.SubElement(root, "sequence", {
            "dir": dir,
            "vel": str(velocity),
            "startSample": str(seq["startSample"]),
            "endSample": str(seq["endSample"]),
            "startChannel": str(seq["startChannel"]),
            "endChannel": str(seq["endChannel"])
        })

        for r in seq["ranges"]:
            ET.SubElement(seq_elem, "range", {
                "channel": str(r["channel"]),
                "maxSample": str(r["maxSample"])
            })

    xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="    ")
    return xml_str.split('\n', 1)[-1]  # Remove the first line which contains the redundant XML declaration

def write_xml_to_file(xml_output, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        file.write(xml_output)
        print("XML file 'hrm_output' has been created.")
