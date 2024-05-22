import csv


def exportToCsv(data, filename):
    with open(filename + '_detected' + '.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow(row)