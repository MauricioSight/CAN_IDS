import csv
import re

# Open the log file and the output CSV file
with open('dos_benigno.log', 'r') as log_file, open('dos_benigno.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header to the CSV file
    csv_writer.writerow(['Timestamp', 'Interface', 'ID', 'Data'])

    # Regular expression to match candump log lines
    log_pattern = re.compile(r'\((\d+\.\d+)\) (\w+) (\w+)\#([\w]*)')

    # Process each line in the log file
    for line in log_file:
        match = log_pattern.match(line.strip())
        if match:
            timestamp, interface, can_id, data = match.groups()
            if not can_id.startswith('0x'):
                can_id = '0x' + can_id
            csv_writer.writerow([timestamp, interface, can_id, data])

print("Conversion to CSV completed successfully.")
