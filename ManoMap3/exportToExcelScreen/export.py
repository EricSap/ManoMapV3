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
        mergeAndColorCells(new_file_name, sliders)
        for time, event_name in events.items():
            print('tijd: ', time)
            print('event: ', event_name)
            total_seconds = time // 10  # Convert deciseconds to seconds
            hour, remainder = divmod(total_seconds, 3600)  # Calculate hours
            minute, second = divmod(remainder, 60)  # Calculate minutes and seconds
            addEventNameAtGivenTime(new_file_name, hour, minute, second, event_name)
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
        "Rectum": "FFFFFF"
    }

    # Merge cells and color them for each section
    sliders = getSliderValues(sliders)
    for i, (start, end) in enumerate(sliders):
        start_col = get_column_letter(start + 11)
        end_col = get_column_letter(end + 11)
        ws.merge_cells(f'{start_col}13:{end_col}13')
        cell = ws[f'{start_col}13']
        cell.value = sections[i]
        cell.alignment = Alignment(horizontal='center', vertical='center')
        fill = PatternFill(start_color=colors[sections[i]], end_color=colors[sections[i]], fill_type="solid")
        cell.fill = fill
        for col in range(start + 11, end + 12):
            ws[f'{get_column_letter(col)}13'].fill = fill

    # Save the workbook
    wb.save(file_name)

def addEventNameAtGivenTime(file_name, hour, minute, second, event_name):
    # Load the workbook and select the active sheet
    wb = load_workbook(file_name)
    ws = wb.active
    
    # Find the insertion row based on the specified hour, minute, and second
    insertion_row = None
    for row in range(15, ws.max_row + 1):
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
    
    # Fill in the event details
    # ws.cell(row=insertion_row, column=1, value=insertion_row - 1)
    ws.cell(row=insertion_row, column=1, value=event_name)
    ws.cell(row=insertion_row, column=2, value=hour)
    ws.cell(row=insertion_row, column=3, value=minute)
    ws.cell(row=insertion_row, column=4, value=second)
    
    # Save the workbook
    wb.save(file_name)