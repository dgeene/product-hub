# Quick Reference Card

## Starting the Application

```bash
# From project root
poetry run python -m src.product_hub.device_monitor

# Then open browser to:
http://localhost:5000
```

## Common ADB Shell Commands

### Device Information
```bash
# Android version
getprop ro.build.version.release

# Device model
getprop ro.product.model

# Serial number
getprop ro.serialno

# All properties
getprop
```

### Package Management
```bash
# List all packages
pm list packages

# List system packages
pm list packages -s

# List third-party packages
pm list packages -3

# Search for specific package
pm list packages | grep chrome

# Get package info
dumpsys package com.example.app
```

### File Operations
```bash
# List files
ls /sdcard/

# List with details
ls -la /sdcard/Download/

# Create directory
mkdir /sdcard/test

# Remove file
rm /sdcard/test.txt
```

### System Status
```bash
# Battery status
dumpsys battery

# Memory info
dumpsys meminfo

# CPU info
cat /proc/cpuinfo

# Storage info
df -h
```

### Process Management
```bash
# List all processes
ps

# Search for process
ps | grep chrome

# Top processes by memory
top -n 1

# Kill process
kill <pid>
```

### Network
```bash
# Network interfaces
ip addr

# Network stats
netstat

# Ping
ping -c 4 google.com
```

### Logs
```bash
# Last 50 log entries
logcat -d -t 50

# Filter by tag
logcat -d -s TAG:V

# Clear logs
logcat -c

# Continuous logging (will timeout after 10s)
logcat
```

### Screen & Display
```bash
# Screen resolution
wm size

# Screen density
wm density

# Display info
dumpsys display
```

## Socket.IO Events

### Client → Server
| Event | Data | Description |
|-------|------|-------------|
| `connect` | - | Client connects |
| `reboot_device` | `{serial: string}` | Reboot device |
| `shell_command` | `{serial: string, command: string}` | Execute shell command |

### Server → Client
| Event | Data | Description |
|-------|------|-------------|
| `device_update` | `{devices: [{serial, status}]}` | Device list update |
| `shell_response` | `{output: string}` | Command output |
| `shell_error` | `{error: string}` | Command error |
| `reboot_response` | `{success: bool, serial?: string, error?: string}` | Reboot result |

## Troubleshooting

### No devices showing
```bash
# Check ADB can see devices
adb devices

# Restart ADB server
adb kill-server
adb start-server

# Check USB debugging is enabled on device
```

### Terminal not responding
- Check browser console for errors (F12)
- Refresh the page
- Make sure device is still connected
- Verify Socket.IO connection (green indicator)

### Commands timing out
- Reduce command complexity
- Some interactive commands don't work well
- 10-second timeout is enforced

## File Locations

```
product-hub/
├── src/product_hub/
│   ├── device_monitor.py      ← Main server code
│   └── templates/
│       └── index.html          ← Web interface
├── README.md                   ← Quick start guide
├── FEATURES.md                 ← Detailed features
├── IMPLEMENTATION.md           ← Technical details
├── PLATFORM_SUPPORT.md         ← Cross-platform info
├── UI_REFERENCE.md             ← UI layout guide
└── test_setup.py              ← Setup verification
```

## Development

### Running in debug mode
Already enabled by default with `debug=True`

### Viewing logs
Server logs appear in the terminal where you started the application

### Testing changes
1. Edit files
2. Restart server (Ctrl+C then restart)
3. Refresh browser (Ctrl+R or Cmd+R)

## Production Deployment

⚠️ **Security Warning**: This application executes commands on your system. For production:

1. Add authentication
2. Restrict to trusted networks
3. Use HTTPS
4. Consider command whitelisting
5. Set up proper firewall rules

## Support

- Check documentation files for detailed information
- Review browser console for client-side errors
- Check server terminal for backend errors
- Ensure ADB is properly installed and configured
