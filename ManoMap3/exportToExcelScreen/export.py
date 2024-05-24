import pandas as pd

def exportToXlsx(data, file_path):
    # Split the file path into the base name and extension

    base_name, ext = file_path.rsplit('.', 1)
    
    # Create the new file path with '_analysis' appended to the base name
    new_file_path = f"{base_name}_analysis.xlsx"
    
    # Write the DataFrame to an Excel file
    try:
        data.to_excel(new_file_path, index=False)
        print(f"Data successfully exported to {new_file_path}")
    except Exception as e:
        print(f"Error exporting data to Excel: {e}")