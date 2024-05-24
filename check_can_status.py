import subprocess

def check_can0_status():
    """Check the status of can0 interface."""
    try:
        # Run 'ip link show can0' and check for 'UP' status
        result = subprocess.run(['ip', 'link', 'show', 'can0'], capture_output=True, text=True)
        if 'state UP' in result.stdout:
            return True
        else:
            print("can0 is down.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Failed to check can0 status: {e}")
        return False

def restart_can0():
    """Restart the can0 interface."""
    try:
        print("Restarting can0 interface...")
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'down'], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'up'], check=True)
        print("can0 interface restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart can0: {e}")
