# Cross-Platform USB Device Monitoring

This application now supports USB device monitoring on both Linux and macOS.

## Platform-Specific Implementations

### Linux
- Uses `pyudev` library to monitor USB devices via netlink
- Real-time event-based monitoring (no polling)
- Efficient and low-resource usage

### macOS
- Uses `system_profiler SPUSBDataType` command polling
- Polls every 1 second to detect USB device changes
- No external dependencies required (uses built-in macOS tools)

## How It Works

The `monitor_devices()` function automatically detects the operating system and uses the appropriate monitoring method:

```python
PLATFORM = platform.system()

if PLATFORM == "Linux":
    # Use pyudev for event-based monitoring
    monitor_devices_linux()
elif PLATFORM == "Darwin":  # macOS
    # Use system_profiler polling
    monitor_devices_macos()
```

## Dependencies

Dependencies are platform-specific:
- **Linux only**: `pyudev` (specified with `sys_platform == 'linux'` in pyproject.toml)
- **macOS**: No additional dependencies (uses built-in `system_profiler`)

## Limitations

### macOS
- Polling-based (1-second interval) vs event-based on Linux
- Slightly higher latency in detecting device changes
- Uses subprocess to call system_profiler (slightly more overhead)

### Linux
- Requires udev library to be installed on the system

## Testing

To test USB device detection:
1. Start the application: `poetry run python src/product_hub/device_monitor.py`
2. Connect or disconnect a USB device
3. The web interface should update within 1-2 seconds
