from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
import json
import platform
from threading import Lock

# Platform-specific imports
PLATFORM = platform.system()

if PLATFORM == "Linux":
    import pyudev

app = Flask(__name__)
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


def get_adb_devices():
    """Get list of connected ADB devices"""
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Skip the first line (header)
        devices = []
        for line in lines:
            if line.strip():
                serial, status = line.split()
                devices.append({"serial": serial, "status": status})
        return devices
    except Exception as e:
        print(f"Error getting ADB devices: {e}")
        return []


def monitor_devices():
    """Background task that monitors for USB device changes"""
    if PLATFORM == "Linux":
        monitor_devices_linux()
    elif PLATFORM == "Darwin":  # macOS
        monitor_devices_macos()
    else:
        print(f"USB monitoring not supported on {PLATFORM}")


def monitor_devices_linux():
    """Monitor USB devices on Linux using pyudev"""
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="usb")

    for device in iter(monitor.poll, None):
        if device.action in ("add", "remove"):
            # Give ADB a moment to recognize the device
            socketio.sleep(1)
            devices = get_adb_devices()
            socketio.emit("device_update", {"devices": devices})


def monitor_devices_macos():
    """Monitor USB devices on macOS using system_profiler polling"""
    import time

    def get_usb_devices():
        """Get current USB device list on macOS"""
        try:
            result = subprocess.run(
                ["system_profiler", "SPUSBDataType", "-json"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            data = json.loads(result.stdout)
            # Extract USB device identifiers
            devices = []

            def extract_devices(items):
                for item in items:
                    if "_name" in item:
                        devices.append(
                            {
                                "name": item.get("_name", "Unknown"),
                                "vendor_id": item.get("vendor_id", ""),
                                "product_id": item.get("product_id", ""),
                            }
                        )
                    if "_items" in item:
                        extract_devices(item["_items"])

            if "SPUSBDataType" in data:
                extract_devices(data["SPUSBDataType"])

            return devices
        except Exception as e:
            print(f"Error getting USB devices on macOS: {e}")
            return []

    previous_devices = get_usb_devices()

    while True:
        time.sleep(1)  # Poll every second
        current_devices = get_usb_devices()

        # Check if device list changed
        if len(current_devices) != len(previous_devices):
            # Give ADB a moment to recognize the device
            socketio.sleep(1)
            devices = get_adb_devices()
            socketio.emit("device_update", {"devices": devices})
            previous_devices = current_devices
        else:
            previous_devices = current_devices


@app.route("/")
def index():
    """Serve the main page"""
    return render_template("index.html")


def background_thread():
    """Start the device monitoring thread"""
    with thread_lock:
        monitor_devices()


@socketio.on("connect")
def handle_connect():
    """Handle client connection"""
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    # Send initial device list
    devices = get_adb_devices()
    socketio.emit("device_update", {"devices": devices})


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
