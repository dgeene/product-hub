# Product Hub - UI Layout Reference

## Visual Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    ADB Device Monitor                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DEVICE LIST                                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │ █ Serial: ba0b86d                                   │    │
│  │   Status: device                                    │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ █ Serial: emulator-5554          ← SELECTED        │    │
│  │   Status: device                 (blue highlight)   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  CONTROLS (shown when device selected)                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Selected Device: emulator-5554                      │    │
│  │                                                      │    │
│  │  [  Reboot Device  ]  [  Toggle Shell  ]            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  ADB SHELL (shown when Toggle Shell clicked)                │
│  ┌────────────────────────────────────────────────────┐    │
│  │ ADB Shell Terminal                                  │    │
│  │ Type commands and press Enter to execute            │    │
│  │                                                      │    │
│  │ $ getprop ro.build.version.release                  │    │
│  │ 11                                                   │    │
│  │ $ ls /sdcard/Download                               │    │
│  │ file1.pdf                                            │    │
│  │ photo.jpg                                            │    │
│  │ $ _                                   ← cursor       │    │
│  │                                                      │    │
│  │                                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Color Scheme

### Device List
- **Online Device**: Green left border (#4CAF50)
- **Offline Device**: Red left border (#f44336)
- **Selected Device**: Blue border and background (#2196F3, #e3f2fd)
- **Hover**: Light gray background (#f0f0f0)

### Buttons
- **Reboot**: Orange (#ff9800) → Darker on hover (#f57c00)
- **Shell**: Blue (#2196F3) → Darker on hover (#1976D2)

### Terminal
- **Background**: Dark (#1e1e1e)
- **Text**: Light gray (#d4d4d4)
- **Cursor**: White (#ffffff)

## Interaction Flow

### Device Selection Flow
```
1. User clicks on device
   ↓
2. Device gets 'selected' class (blue highlight)
   ↓
3. Controls panel slides in (becomes visible)
   ↓
4. Selected device info displayed
```

### Reboot Flow
```
1. User clicks "Reboot Device"
   ↓
2. Confirmation dialog appears
   ↓
3. If confirmed:
   - Send 'reboot_device' event to server
   ↓
4. Server executes: adb -s <serial> reboot
   ↓
5. Success/error alert shown to user
```

### Shell Flow
```
1. User clicks "Toggle Shell"
   ↓
2. Terminal container slides in
   ↓
3. xterm.js terminal initializes
   ↓
4. User types command + Enter
   ↓
5. Command sent via Socket.IO to server
   ↓
6. Server executes: adb -s <serial> shell <command>
   ↓
7. Output sent back via Socket.IO
   ↓
8. Terminal displays output
   ↓
9. New prompt shown, ready for next command
```

## Keyboard Shortcuts in Terminal

| Key | Action |
|-----|--------|
| Enter | Execute command |
| Backspace | Delete character |
| Ctrl+C | Cancel (shows ^C and new prompt) |
| Any character | Type in command |

## Real-time Updates

### Device Connection
```
USB device plugged in
   ↓
System detects device (pyudev/system_profiler)
   ↓
monitor_devices() detects change
   ↓
get_adb_devices() called
   ↓
'device_update' event emitted
   ↓
Browser receives update
   ↓
Device list refreshes automatically
```

### Device Disconnection
```
USB device unplugged
   ↓
System detects removal
   ↓
monitor_devices() detects change
   ↓
'device_update' event with updated list
   ↓
Browser receives update
   ↓
Device list refreshes
   ↓
If selected device was removed:
  - Selection cleared
  - Controls hidden
  - Terminal hidden
```

## Responsive Behavior

- Container max-width: 1200px (centered)
- Terminal auto-fits to container width
- Terminal height: 400px (scrollable if output exceeds)
- Works on desktop, tablets, and mobile browsers

## Browser Compatibility

Tested and working with:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

Requires:
- JavaScript enabled
- WebSocket support (all modern browsers)
