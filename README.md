# Product Hub

A cross-platform web-based ADB device monitor with interactive shell capabilities.

## Features

- 🔍 Real-time USB device detection (Linux & macOS)
- 📱 ADB device monitoring with auto-updates
- 🖥️ Interactive web-based terminal using xterm.js
- 🔄 Device reboot functionality
- 💻 Execute ADB shell commands directly from browser

## Quick Start

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run the server:
   ```bash
   poetry run python -m src.product_hub.device_monitor
   ```

3. Open your browser to `http://localhost:5000`

## Usage

1. **View Devices**: Connected ADB devices appear in the list automatically
2. **Select Device**: Click on any device to select it
3. **Reboot**: Click "Reboot Device" to restart the selected device
4. **Open Shell**: Click "Toggle Shell" to open an interactive terminal
5. **Execute Commands**: Type ADB shell commands and press Enter

### Example Shell Commands
```bash
# Get Android version
getprop ro.build.version.release

# List installed packages
pm list packages

# Check battery status
dumpsys battery

# View recent logs
logcat -d -t 50
```

See [FEATURES.md](FEATURES.md) for detailed feature documentation.

## Setup prep

### Linux

Install ADB the lazy way `sudo apt-get install -y android-tools-adb`

Make sure your user is in the plugdev group: `groups`

Find your device and vendor using `lsusb`

`sudo vi /etc/udev/rules.d/51-android.rules`

```plain
SUBSYSTEM=="usb", ATTR{idVendor}=="<vendor id>", ATTR{idProduct}=="<product id>", MODE="0666", GROUP="plugdev"
```

Reload udev: `sudo udevadm control --reload-rules`


Unplug the device and plug it back in


Add udev rules

Note: You might need to add appropriate udev rules to access USB devices without sudo. You can create a file like /etc/udev/rules.d/51-android.rules with appropriate permissions for Android devices if needed.



This werror ocurrs when no udev is set
```shell
$ adb devices
* daemon not running; starting now at tcp:5037
* daemon started successfully
List of devices attached
ba0b86d	no permissions (missing udev rules? user is in the plugdev group); see [http://developer.android.com/tools/device.html]
```

### Mac OS

No setup steps required. `System_profiler` is used to poll for usb connections.


## Running

Run the server: `python -m src.product_hub.device_monitor`
