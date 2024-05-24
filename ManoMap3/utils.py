import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
from manoutilsv2 import data_preperation, CSVToDict
from patternDetectionScreen.detectionv2 import find_contractions_from_patterns, find_patterns_from_values_dict
from patternDetectionScreen import heatplot

global valuesDict

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

def import_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    return file_path

def import_txt_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path

def display_excel_filename(root):
    global valuesDict
    file_path = import_excel_file()
    if file_path and os.path.isfile(file_path):  # Check if file_path is not empty and is a valid file
        filename = os.path.basename(file_path)
        label = ctk.CTkLabel(root, text="Selected Excel File: " + filename, font=("Arial", 12))
        label.pack(pady=10)
        try:
            valuesDict = CSVToDict(file_path)
        except:
            print("Error converting to Dict")
    else:
        print("No file selected.")

def display_txt_filename(root):
    global valuesDict
    file_path = import_txt_file()
    if file_path and os.path.isfile(file_path):  
        filename = os.path.basename(file_path)
        label = ctk.CTkLabel(root, text="Selected Text File: " + filename, font=("Arial", 12))
        label.pack(pady=10)
        valuesDict = CSVToDict(file_path)
        #print(valuesDict)
        # try:
        # except:
        #     print("Error converting to Dict")
    else:
        print("No file selected.")

def detectEventsPressed(sliders, advanced_sliders):
    try: 
        global valuesDict
        global contractions

        #return threshold values
        thresholdVals = list(sliders[0].get())
        detectionThreshold = int(advanced_sliders[4].get())
        amountofSensors = int(advanced_sliders[2].get())
        amountofOverlapped = int(advanced_sliders[1].get())

        #data preperation
        filedata = data_preperation(valuesDict)

        #return sensor values
        slidervals = list(sliders[1].get())
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])

        #pattern detedction
        results = find_patterns_from_values_dict(filedata, first_sensor, last_sensor, detectionThreshold,amount_of_sensors=amountofSensors, amount_overlapped=amountofOverlapped)

        #contraction detection
        contractions = find_contractions_from_patterns(results, 2)
        print("contractions", contractions)
        messagebox.showinfo("detection", "detection completed!")
        print("detection worked!!!")
    except NameError:
        messagebox.showinfo("hahahha")
        print("detection didn't work...")

def clearEvents():
        global contractions
        contractions = []

def showPlotPressed(sliders):
    try:
        global commentsDict
        thresholdVals = list(sliders[0].get())
        visible_sensors = list(sliders[1].get())
        first_sensor = int(visible_sensors[0])
        last_sensor = int(visible_sensors[1])
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        colormap = "inferno"
        heatplot.showPlot(first_sensor, last_sensor, minThreshold, maxThreshold, differentialMode, valuesDict, commentsDict, colormap=colormap)
    except NameError:
        # messagebox.showinfo("Error", "Please select a file.")
        print("Please select a file.")