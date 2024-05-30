import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
from manoutilsv2 import data_preparation, CSVToDict, get_granularity_factor
from patternDetectionScreen.detectionv2 import find_contractions_from_patterns, find_patterns_from_values_dict
from patternDetectionScreen import heatplot
from patternDetectionScreen import signalplot

global valuesDict
global filename
global file_selected 

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

def display_excel_filename(root, button_export):
    global valuesDict
    global file_selected
    file_path = import_excel_file()
    if file_path and os.path.isfile(file_path):  # Check if file_path is not empty and is a valid file
        filename = os.path.basename(file_path)
        label = ctk.CTkLabel(root, text="Selected Excel File: " + filename, font=("Arial", 12))
        label.pack(pady=10)
        try:
            valuesDict = CSVToDict(file_path)
            file_selected = True
            button_export.configure(state='normal')
        except:
            print("Error converting to Dict")
    else:
        print("No file selected.")

def display_txt_filename(root, button_export):
    global valuesDict
    global file_selected 
    file_path = import_txt_file()
    if file_path and os.path.isfile(file_path):
        global filename
        filename = os.path.basename(file_path)
        label = ctk.CTkLabel(root, text="Selected Text File: " + filename, font=("Arial", 12))
        label.pack(pady=10)
        valuesDict = CSVToDict(file_path)
        file_selected = True
        button_export.configure(state='normal')
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
        filedata = data_preparation(valuesDict)

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
        messagebox.showinfo("detection", "Events cleared!")

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

def showSignalsPressed(sliders):
    try:
        global commentsDict
        visible_sensors = list(sliders[1].get())
        first_sensor = int(visible_sensors[0])
        last_sensor = int(visible_sensors[1])
        thresholdVals = list(sliders[0].get())
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        colormap = "inferno"
        global contractions
        #opacity hardcoded for now
        signalplot.show_combined_plot(data_preparation(valuesDict), commentsDict, first_sensor, last_sensor, minThreshold, maxThreshold, colormap=colormap, opacity=1, detected_events=contractions, exportDataXml = exportDataXml)
    except NameError:
        messagebox.showinfo("Error", "Please select a file.")

def exportToXML(advanced_sliders):
        # also_export_a_txt()
        try:
            exportTitle = str(filename).split('.')[0] + "_sequences_data.txt"
            print(exportTitle)
        except NameError:
            messagebox.showinfo("Error", "Please select a file.")

        global exportDataXml
        print("exportDataXml: ", exportDataXml)

        XML = data_to_XML(exportDataXml, advanced_sliders)

        with open(exportTitle, 'w') as outputfile:
            outputfile.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
            outputfile.write("\n")
            outputfile.write('<sequences>')
            outputfile.write("\n")
            outputfile.write(XML)
            outputfile.write("\n")
            outputfile.write('</sequences>')
        print("succesful export to XML")

def data_to_XML(data, advanced_sliders):
    sequencesTXT = ""
    distance = advanced_sliders[0].get() # in mm (?)
    print("distance", distance)
    with open('data.txt', 'w') as outputfile:
        outputfile.write(str(data))
    with open('contractions.txt', 'w') as outputfile:
        outputfile.write(str(contractions))
    index = 0
    for contraction in data:
        channelValues= list(contraction.keys())
        maxSampleValues = []
        for sensor in contraction.values():
            maxSampleValues.append(sensor['maxSample'])

        startSample = str(int(min(maxSampleValues) * 10))
        endSample = str(int(max(maxSampleValues) * 10))
        startChannel = str(min(channelValues))
        endChannel = str(max(channelValues))
        gran = get_granularity_factor()
        time = gran * len(contractions[index]['sequences'])
        startSensor = contractions[index]['sequences'][0][0][0]
        endSensor = contractions[index]['sequences'][-1][-1][0]
        # last sensor - first * distance between each sensor = total distance, time is in decaseconds => *10, distance in mm => *10
        velocity = (endSensor - startSensor) * distance / time * 100
        dir = 'Antegrade'
        if velocity < 0:
            dir = 'Retrograde'

        sequenceHeader = '<sequence dir="' + dir + '" vel="' + str(velocity) + '" startSample="'+ startSample + '" endSample="' + endSample+ '" startChannel="' + startChannel + '" endChannel="' + endChannel + '">'
        sequencesTXT+= sequenceHeader
        for item in contraction:
            point = '<range channel="' + str(item) + '" maxSample="'+  str(int(contraction[item]['maxSample'] * 10))+ '"/>'
            sequencesTXT += "\n"
            sequencesTXT += "\t" + point
        sequencesTXT += "\n"+'</sequence>'
        index += 1

    return sequencesTXT