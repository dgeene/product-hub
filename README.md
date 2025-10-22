# Product Hub

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
