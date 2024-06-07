import os
from utils import process_sequences
import pandas as pd
from utils import sequences_to_xml, write_xml_to_file
from tkinter import filedialog

global result
result = []

# Read the input file into a DataFrame
global input_file_path
input_file_path = ''

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

# Define the threshold for sensor values
threshold = 100

# Define the minimum number of sensors exceeding the threshold to form a pattern
min_pattern_length = 3

# Define the time window for chunks (900 seconds)
time_window = 50

def read_data():
    # Read the data into a DataFrame
    global data

    data = pd.read_csv(input_file_path, delim_whitespace=True, header=None)

    # Rename the columns: time and sensors
    data.columns = ['time'] + [f'sensor_{i}' for i in range(1, 42)]

    # Keep rows where the time has a decimal part of .0
    data = data[data['time'] == data['time'].astype(int)]

    # Filter out rows where the time is 7800 seconds or below
    data = data[data['time'] > 7800]

    # Remove the decimal part from the time
    data['time'] = data['time'].astype(int)

def find_patterns(chunk):
    patterns = []
    max_sensor_values = chunk.drop(columns=['time']).max(axis=0)
    #filter the series to only include sensors that exceed the threshold
    max_sensor_values = max_sensor_values[max_sensor_values > threshold]

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

    last_chunk_size = 1

    chunks = []

    chunk_start_time = start_time
    chunk_end_time = 1

    blob_found = False
    max_chunk_time = time_window

    for start in range(int(start_time), int(end_time)):
        #get the max value of the sensor at the start time
        max_value = data[data['time'] == start].drop(columns=['time']).max(axis=0).max()
        sensor_of_max_value = data[data['time'] == start].drop(columns=['time']).max(axis=0).idxmax()
        if max_value > threshold and not blob_found:
            blob_found = True
            chunk_start_time = start


        chunk_end_time = start
        #if the max value is below the threshold, create a chunk from chunk_start_time to time_of_max_value
        if (max_value < threshold and blob_found) or chunk_end_time - chunk_start_time > max_chunk_time:
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
            result.append(pattern)
    return result

def compute_patterns():
    read_data()
    global result
    result = define_chunks_and_get_patterns(data)
    print("Finished computing patterns!")

def exportToXML_2():
    sequences = process_sequences(result)
    xml_output = sequences_to_xml(sequences)
    write_xml_to_file(xml_output, filename)