import subprocess
import re

def get_device_list():
    """
    Retrieves the list of devices from Device Manager using WMIC.
    Returns a list of (DeviceID, Name) tuples.
    """
    result = subprocess.run(
        ["wmic", "path", "Win32_PnPEntity", "get", "DeviceID,Name"],
        capture_output=True, text=True, check=True
    )
    devices = []
    lines = result.stdout.splitlines()
    for line in lines[1:]:
        # Skip header
        if not line.strip():
            continue
        # Try to split DeviceID and Name
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) == 2:
            devices.append((parts[0], parts[1]))
    return devices

def count_ch341_ch347(devices):
    """
    Counts the CH341 and CH347 devices and determines their type.
    Returns dicts mapping type to count.
    """
    ch347_count = {"CH347F": 0, "CH347T": 0}
    ch341_count = {"CH341A": 0, "CH341T": 0, "CH341": 0}
    for device_id, name in devices:
        # CH347 detection
        if device_id.startswith("USB\\VID_1A86&PID_55DE&MI_04"):
            if "CH347F" in name:
                ch347_count["CH347F"] += 1
            elif "CH347T" in name:
                ch347_count["CH347T"] += 1
        # CH341 detection
        elif device_id.startswith("USB\\VID_1A86&PID_5512"):
            if "CH341A" in name:
                ch341_count["CH341A"] += 1
            elif "CH341T" in name:
                ch341_count["CH341T"] += 1
            elif "CH341" in name:
                ch341_count["CH341"] += 1
    return ch347_count, ch341_count

if __name__ == "__main__":
    devices = get_device_list()
    ch347_count, ch341_count = count_ch341_ch347(devices)
    print("CH347 devices:")
    for chip, count in ch347_count.items():
        print(f"  {chip}: {count}")

    print("CH341 devices:")
    for chip, count in ch341_count.items():
        print(f"  {chip}: {count}")
