import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, PatternFill

def exportToXlsx(data, file_name, sliders):
    # Split the file path into the base name and extension
    base_name, ext = file_name.rsplit('.', 1)
    
    # Create the new file path with '_analysis' appended to the base name
    new_file_name = f"{base_name}_analysis.xlsx"
    
    # Write the DataFrame to an Excel file
    try:
        data.to_excel(new_file_name, index=False)
        mergeAndColorCells(new_file_name, sliders)
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
