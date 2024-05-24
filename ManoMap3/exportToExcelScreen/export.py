import pandas as pd
import numpy as np

def exportToXlsx(data, file_name, sliders):
    # Split the file path into the base name and extension

    base_name, ext = file_name.rsplit('.', 1)
    
    # Create the new file path with '_analysis' appended to the base name
    new_file_name = f"{base_name}_analysis.xlsx"

    data = addHeaderBasedOnSliders(sliders, data)
    
    # Write the DataFrame to an Excel file
    try:
        data.to_excel(new_file_name, index=False)
        print(f"Data successfully exported to {new_file_name}")
    except Exception as e:
        print(f"Error exporting data to Excel: {e}")

def addHeaderBasedOnSliders(sliders, data):
    # Get the Slider values
    sliders = getSliderValues(sliders)

    # sliders = getSliderValues(sliders)
    print(sliders)

    # Define the sections
    sections = ["Ascending", "Transverse", "Descending", "Sigmoid", "Rectum"]
    
    # Create a new header row with merged labels
    new_header = [''] * len(data.columns)
    
    # Fill the new header with section labels based on slider values
    for i, (start, end) in enumerate(sliders):
        for j in range(start - 1, end):
            new_header[j+11] = sections[i]

    # Insert the new header row into the DataFrame
    new_header_df = pd.DataFrame([new_header], columns=data.columns)
    data_with_header = pd.concat([data.iloc[:12], new_header_df, data.iloc[12:]], ignore_index=True)

    # data_with_header = pd.concat([pd.DataFrame([new_header], columns=data.columns), data], ignore_index=True)
    
    return data_with_header

def getSliderValues(sliders):
    list_with_slider_tuples = []
    for i in range(len(sliders)):
        value1 = -1
        value2 = -1
        for element in sliders[i].get():
            if value1 == -1:
                value1 = round(element)
            else:
                value2 = round(element)
        slider_tuple = (value1,value2)
        list_with_slider_tuples.append(slider_tuple)
    return list_with_slider_tuples

