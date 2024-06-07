# Define the input and output file paths
input_file_path = 'Nalox1_11_07_2018.txt'
output_file_path = 'output.txt'

# Initialize a set to keep track of unique seconds
unique_seconds = set()

# Open the input file for reading and output file for writing
with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    # Read each line from the input file
    for line in infile:
        # Split the line into columns based on white spaces
        columns = line.split()
        # Extract the time value from the first column
        time_value = columns[0]
        # Check if the time value is an integer (no decimal point)
        if '.' not in time_value:
            # Convert the time value to an integer
            time_int = int(time_value)
            # Check if this second is greater than 7800 and has not already been written
            if time_int > 7800 and time_int not in unique_seconds:
                # Add the time to the set of unique seconds
                unique_seconds.add(time_int)
                # Join the columns back into a single string with spaces
                new_line = ' '.join(columns)
                # Write the new line to the output file
                outfile.write(new_line + '\n')

print(f'Processed data has been written to {output_file_path}')