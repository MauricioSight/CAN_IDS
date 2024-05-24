import csv

# Define the input CSV file
input_csv_file = 'benigno.csv'

# Create a set to store unique CAN IDs
unique_can_ids = set()

# Open the CSV file and read its contents
with open(input_csv_file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    
    # Process each row in the CSV file
    for row in csv_reader:
        if len(row) >= 3:
            can_id = row[2]
            unique_can_ids.add(can_id)

# Print the unique CAN IDs
print("Unique CAN IDs:")
for can_id in unique_can_ids:
    print(can_id)