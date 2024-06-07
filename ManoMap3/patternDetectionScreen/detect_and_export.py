import os
from utils import process_sequences
import pandas as pd
from utils import sequences_to_xml, write_xml_to_file, convertTime, validateTime
from tkinter import filedialog

global result
result = []

# Read the input file into a DataFrame
global input_file_path
input_file_path = ''

visible_sensors = 40
detection_threshold = 100
min_pattern_length = 3
maximum_chunk_size = 30
distance_between_sensors = 25


def import_txt_file_detection(button_export, file_label):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path and os.path.isfile(file_path):
        global filename
        filename = os.path.basename(file_path)
        file_label.configure(text="Selected Text File: " + filename, font=("Arial", 12))
        button_export.configure(state='normal')
        global input_file_path
        input_file_path = file_path
    else:
        file_label.configure(text="No file selected")
        print("No file selected.")
    return input_file_path

def read_data():
    # Read the data into a DataFrame
    global data

    global result
    result = []

    data = pd.read_csv(input_file_path, delim_whitespace=True, header=None)

    # Rename the columns: time and sensors
    data.columns = ['time'] + [f'sensor_{i}' for i in range(1, 42)]

    # Keep rows where the time has a decimal part of .0
    data = data[data['time'] == data['time'].astype(int)]

    # Filter out rows where the time is 7800 seconds or below
    data = data[data['time'] > total_seconds]

    # Remove the decimal part from the time
    data['time'] = data['time'].astype(int)

def find_patterns(chunk):
    patterns = []
    max_sensor_values = chunk.drop(columns=['time']).max(axis=0)
    #filter the series to only include sensors that exceed the threshold
    max_sensor_values = max_sensor_values[max_sensor_values > detection_threshold]

    #if there are 3 or more following (eg. sensor_23, sensor_24, sensor_25) sensors that exceed the threshold, create a list of these sensors until the next sensor is not right beside the previous one
    for sensor in max_sensor_values.index:
        start = int(sensor.split('_')[1])
        pattern = []
        stop_loop = False

        for i in range(start, 41):
            for mini_pattern in patterns:
                if sensor in [val[1] for val in mini_pattern]:
                    stop_loop = True
            if stop_loop:
                break
            sensor_name = f'sensor_{i}'
            if sensor_name not in max_sensor_values.index:
                break
            pattern.append((chunk[chunk[sensor_name] == max_sensor_values[sensor_name]]['time'].values[0], sensor_name, max_sensor_values[sensor_name]))

        if len(pattern) >= min_pattern_length:
            patterns.append(pattern)
    return patterns

def define_chunks_and_get_patterns(data):
    start_time = data['time'].min()
    end_time = data['time'].max()

    chunks = []

    chunk_start_time = start_time
    chunk_end_time = 1

    blob_found = False

    for start in range(int(start_time), int(end_time)):
        #get the max value of the sensor at the start time
        max_value = data[data['time'] == start].drop(columns=['time']).max(axis=0).max()
        if max_value > detection_threshold and not blob_found:
            blob_found = True
            chunk_start_time = start

        chunk_end_time = start
        #if the max value is below the threshold, create a chunk from chunk_start_time to time_of_max_value
        if (max_value < detection_threshold and blob_found) or chunk_end_time - chunk_start_time > maximum_chunk_size:
            chunk = data[(data['time'] >= chunk_start_time) & (data['time'] < chunk_end_time)]
            if not chunk.empty:
                # print("CHUNK",chunk)
                chunks.append(chunk)
            blob_found = False

    for chunk in chunks:
        patterns = find_patterns(chunk)
        if not patterns:
            continue
        for pattern in patterns:
            if pattern not in result:
                result.append(pattern)
    return result

def compute_patterns(sliders, advanced_sliders, time_entries):
    global visible_sensors
    visible_sensors = (int(round(sliders[0].get()[0])), int(round(sliders[0].get()[1])))

    global detection_threshold
    detection_threshold = int(round(advanced_sliders[0].get())) * 10

    global min_pattern_length
    min_pattern_length = int(round(advanced_sliders[1].get()))

    global maximum_chunk_size
    maximum_chunk_size = int(round(advanced_sliders[2].get()))
    
    global distance_between_sensors
    distance_between_sensors = int(round(advanced_sliders[3].get()))

    # Extract time from entries
    hour = time_entries[0].get()
    minute = time_entries[1].get()
    second = time_entries[2].get()
    time_string = f"{hour}:{minute}:{second}"

    # Validate and convert time
    if validateTime(time_string):
        total_seconds = round(convertTime(time_string) / 10)
        print("Total seconds:", total_seconds)
    else:
        print("Invalid time format")
    
    read_data()

    global result
    result = define_chunks_and_get_patterns(data)
    print("Finished computing patterns!")

def exportToXML_2():
    sequences = process_sequences(result)
    xml_output = sequences_to_xml(sequences)
    write_xml_to_file(xml_output, filename)