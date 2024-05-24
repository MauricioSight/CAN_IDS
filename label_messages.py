import csv
import re

class AVLTreeNode:
    def __init__(self, key, can_id, data):
        self.key = key
        self.can_id = can_id
        self.data = data
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def insert(self, root, key, can_id, data):
        if not root:
            return AVLTreeNode(key, can_id, data)
        elif key < root.key:
            root.left = self.insert(root.left, key, can_id, data)
        else:
            root.right = self.insert(root.right, key, can_id, data)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        # Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        # Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def search_range(self, root, key, margin):
        if not root:
            return []
        results = []
        if abs(root.key - key) <= margin:
            results.append((root.key, root.can_id, root.data))
        if key - margin < root.key:
            results.extend(self.search_range(root.left, key, margin))
        if key + margin > root.key:
            results.extend(self.search_range(root.right, key, margin))
        return results



# Files with CAN messages and attack messages
can_log_file = 'dos_benigno.log'
can_csv_file = 'dos_benigno.csv'
attack_log_file = 'dos_attack_log.csv'
output_csv_file = 'dos_attack_labeled.csv'

# Time margin for considering a match (in seconds)
time_margin = 0.001

# Load attack messages into a list for range verification
avl_tree = AVLTree()
root = None

# Open the log file and the output CSV file
with open(can_log_file, 'r') as log_file, open(can_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header to the CSV file
    csv_writer.writerow(['Timestamp', 'ID', 'Data'])

    # Regular expression to match candump log lines
    log_pattern = re.compile(r'\((\d+\.\d+)\) (\w+) (\w+)\#([\w]*)')

    # Process each line in the log file
    for line in log_file:
        match = log_pattern.match(line.strip())
        if match:
            timestamp, interface, can_id, data = match.groups()
            if not can_id.startswith('0x'):
                can_id = '0x' + can_id
            csv_writer.writerow([timestamp, can_id, data])

print("Conversion to CSV completed successfully.")

with open(attack_log_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    for row in reader:
        timestamp, can_id, data = row
        root = avl_tree.insert(root, float(timestamp), can_id, data)

print("Load attack messages completed successfully.")

# Label CAN messages based on attack messages with range verification
with open(can_csv_file, 'r') as can_file, open(output_csv_file, 'w', newline='') as output_file:
    can_reader = csv.reader(can_file)
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(['Timestamp', 'ID', 'Data', 'Label'])

    next(can_reader)  # Skip the header
    for row in can_reader:
        timestamp, can_id, data = row
        timestamp = float(timestamp)
        can_id_int = int(can_id, 16)  # Convert CAN ID to integer
        label = 'benign'
        
        matching_attacks = avl_tree.search_range(root, timestamp, time_margin)
        for attack_time, attack_id, attack_data in matching_attacks:
            if int(can_id, 16) == int(attack_id, 16) and data == attack_data:
                label = 'attack'
                break

        csv_writer.writerow([timestamp, can_id, data, label])

print("Messages labeled successfully.")
