import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, PatternFill

def exportToXlsx(data, file_name, sliders, events):
    # Split the file path into the base name and extension
    base_name, ext = file_name.rsplit('.', 1)

    # Create the new file path with '_analysis' appended to the base name
    new_file_name = f"{base_name}_analysis.xlsx"
    
    # Write the DataFrame to an Excel file
    try:
        data.to_excel(new_file_name, index=False)
        insertEmptyRows(new_file_name, 7)
        mergeAndColorCells(new_file_name, sliders)
        event_names = []
        for time, event_name in events.items():
            print('tijd: ', time)
            print('event: ', event_name)
            event_names.append(event_name)
            total_seconds = time // 10  # Convert deciseconds to seconds
            hour, remainder = divmod(total_seconds, 3600)  # Calculate hours
            minute, second = divmod(remainder, 60)  # Calculate minutes and seconds
            addEventNameAtGivenTime(new_file_name, hour, minute, second, event_name)
        hey = assignSectionsBasedOnStartSection(new_file_name, sliders, event_names)
        print(f"Data successfully exported to {new_file_name}")
    except Exception as e:
        print(f"Error exporting data to Excel: {e}")

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

def mergeAndColorCells(file_name, sliders):
    # Load the workbook and select the active sheet
    wb = load_workbook(file_name)
    ws = wb.active
    
    # Define the sections and their corresponding colors
    sections = ["Ascending", "Transverse", "Descending", "Sigmoid", "Rectum"]
    colors = {
        "Ascending": "A9D08E",
        "Transverse": "BDD7EE",
        "Descending": "F8CBAD",
        "Sigmoid": "D9D9D9",
        "Rectum": "B1A0C7"
    }

    # Merge cells and color them for each section
    sliders = getSliderValues(sliders)
    for i, (start, end) in enumerate(sliders):
        start_col = get_column_letter(start + 11)
        end_col = get_column_letter(end + 11)
        ws.merge_cells(f'{start_col}20:{end_col}20')
        cell = ws[f'{start_col}20']
        cell.value = sections[i]
        cell.alignment = Alignment(horizontal='center', vertical='center')
        fill = PatternFill(start_color=colors[sections[i]], end_color=colors[sections[i]], fill_type="solid")
        cell.fill = fill
        for col in range(start + 11, end + 12):
            ws[f'{get_column_letter(col)}20'].fill = fill

    # Save the workbook
    wb.save(file_name)

def addEventNameAtGivenTime(file_name, hour, minute, second, event_name):
    # Load the workbook and select the active sheet
    wb = load_workbook(file_name)
    ws = wb.active
    
    # Find the insertion row based on the specified hour, minute, and second
    insertion_row = None
    for row in range(22, ws.max_row + 1):
        cell_hour = ws.cell(row=row, column=2).value
        cell_minute = ws.cell(row=row, column=3).value
        cell_second = ws.cell(row=row, column=4).value
        
        if (int(cell_hour) > int(hour)) or (int(cell_hour) == int(hour) and int(cell_minute) > int(minute)) or (int(cell_hour) == int(hour) and int(cell_minute) == int(minute) and int(cell_second) >= int(second)):
            insertion_row = row
            break
    

    if insertion_row is None:
        insertion_row = ws.max_row + 1
    
    # Insert a new row at the identified position
    ws.insert_rows(insertion_row)
    
    for col in range(1, 11):
        ws.cell(row=insertion_row, column=col, value=event_name)
        ws.cell(row=insertion_row, column=col).fill = PatternFill(start_color="92D050", end_color="92D050", fill_type="solid")
    # Fill in the event details
    # ws.cell(row=insertion_row, column=1, value=insertion_row - 1)
    ws.cell(row=insertion_row, column=2, value=hour)
    ws.cell(row=insertion_row, column=3, value=minute)
    ws.cell(row=insertion_row, column=4, value=second)

    
    # Save the workbook
    wb.save(file_name)

def insertEmptyRows(file_name, amount):
    wb = load_workbook(file_name)
    ws = wb.active

    for i in range (amount):
        ws.insert_rows(13 + i)
    
    wb.save(file_name)

def assignSectionsBasedOnStartSection(file_name, sliders, event_names):
    # Load the workbook and select the active sheet
    wb = load_workbook(file_name)
    ws = wb.active

    # Define the sections and their corresponding colors
    sections = ["Ascending", "Transverse", "Descending", "Sigmoid", "Rectum"]
    colors = {
        "Ascending": "A9D08E",
        "Transverse": "BDD7EE",
        "Descending": "F8CBAD",
        "Sigmoid": "D9D9D9",
        "Rectum": "B1A0C7"
    }

    # Get the slider values
    sliders = getSliderValues(sliders)

    counters = {}

    counters.update({"Post-Wake": {}})
    for event_name in event_names:
        counters.update({event_name: {}})

    counter = {
        "Ascending": 0,
        "Transverse": 0,
        "Descending": 0,
        "Sigmoid": 0,
        "Rectum": 0,
        "Sigmoid tot in Rectum": 0
    }

    # Iterate over each row starting from row 22
    for row in range(22, ws.max_row + 1):
        for col in range(12, ws.max_column + 1):  # Adjust the starting column index if needed
            cell_value = ws.cell(row=row, column=col).value
            if isinstance(cell_value, (int, float)) and cell_value > 0:
                # Determine the section based on the column index and slider ranges
                for i, (start, end) in enumerate(sliders):
                    #if end of sigmoid AND start of rectum have a value, color the 11th column grey like the sigmoid section
                    if i == 3 and ws.cell(row=row, column=end+11).value != None and ws.cell(row=row, column=end+12).value != None:
                        fill = PatternFill(start_color=colors["Sigmoid"], end_color=colors["Sigmoid"], fill_type="solid")
                        ws.cell(row=row, column=11).fill = fill
                        counter.update({"Sigmoid tot in Rectum": counter["Sigmoid tot in Rectum"] + 1})

                    if start + 11 <= col <= end + 11:
                        section = sections[i]
                        counter.update({section: counter[section] + 1})
                        length_cell = ws.cell(row=row, column=10)  #column 10 has the length data
                        fill = PatternFill(start_color=colors[section], end_color=colors[section], fill_type="solid")
                        length_cell.fill = fill
                        break
                break
        #check if the cell value is a string instead of an int, if so add counter to counters (event name as key and counter as value) and reset each value to 0
        next_row = ws.cell(row=row + 1, column=1).value
        if isinstance(ws.cell(row=row, column=1).value, str) or next_row == None:
            # add the counter to the first empty value from a key in the counters dictionary
            for key in counters.keys():
                if counters[key] == {}:
                    counters[key] = counter
                    break
            counter = {
                "Ascending": 0,
                "Transverse": 0,
                "Descending": 0,
                "Sigmoid": 0,
                "Rectum": 0,
                "Sigmoid tot in Rectum": 0
            }

    #start at column 19 row 3 and add the keys going down
    row = 3
    for key in counter.keys():
        ws.cell(row=row, column=19, value=key)
        row += 1
    column = 20
    for (key,value) in counters.items():
        row = 2
        ws.cell(row=row, column=column, value=key)
        fill = PatternFill(start_color="92D050", end_color="92D050", fill_type="solid")
        ws.cell(row=row, column=column).fill = fill
        row += 1
        print("value: ", value)
        for element in value.values():
            print('element: ', element)
            ws.cell(row=row, column=column, value=element)
            row += 1
        column += 1
    # Save the workbook
    wb.save(file_name)
    print(counters)
    return counters