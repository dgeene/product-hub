# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Browser                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      index.html                           │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │  │
│  │  │ Device     │  │   Control    │  │   xterm.js      │  │  │
│  │  │ List UI    │  │   Buttons    │  │   Terminal      │  │  │
│  │  └────────────┘  └──────────────┘  └─────────────────┘  │  │
│  │         │                │                    │           │  │
│  │         └────────────────┴────────────────────┘           │  │
│  │                          │                                 │  │
│  │                   Socket.IO Client                        │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ WebSocket
                               │ (bidirectional)
┌──────────────────────────────┴──────────────────────────────────┐
│                    Flask Server (Python)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  device_monitor.py                        │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              Flask-SocketIO Server                  │  │  │
│  │  │  ┌──────────────┐  ┌──────────────────────────┐    │  │  │
│  │  │  │   Event      │  │    Event Handlers:       │    │  │  │
│  │  │  │   Emitter    │  │  - handle_connect()      │    │  │  │
│  │  │  │              │  │  - handle_reboot()       │    │  │  │
│  │  │  │              │  │  - handle_shell_command()│    │  │  │
│  │  │  └──────────────┘  └──────────────────────────┘    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │          Background Monitor Thread                  │  │  │
│  │  │  ┌──────────────────┐  ┌──────────────────┐        │  │  │
│  │  │  │ Linux:           │  │ macOS:           │        │  │  │
│  │  │  │ pyudev           │  │ system_profiler  │        │  │  │
│  │  │  │ event monitor    │  │ polling          │        │  │  │
│  │  │  └──────────────────┘  └──────────────────┘        │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ subprocess calls
┌──────────────────────────────┴──────────────────────────────────┐
│                    ADB (Android Debug Bridge)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Commands:                                                │  │
│  │  - adb devices                                            │  │
│  │  - adb -s <serial> reboot                                 │  │
│  │  - adb -s <serial> shell <command>                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ USB/Network
┌──────────────────────────────┴──────────────────────────────────┐
│                      Android Devices                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │  Device 1  │  │  Device 2  │  │  Device 3  │    ...        │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Device Detection Flow

```
USB Device Connected
        │
        ▼
┌───────────────────┐
│  OS Layer         │
│  - Linux: udev    │
│  - macOS: IOKit   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Monitor Thread   │
│  - Linux: pyudev  │
│  - macOS: poll    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  get_adb_devices()│
│  subprocess call  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  emit event       │
│  'device_update'  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Socket.IO        │
│  broadcasts       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  All connected    │
│  browsers update  │
└───────────────────┘
```

### Shell Command Execution Flow

```
User types command in terminal
        │
        ▼
┌───────────────────┐
│  xterm.js         │
│  onData handler   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Socket.IO emit   │
│  'shell_command'  │
│  {serial, cmd}    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Flask-SocketIO   │
│  @socketio.on()   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  subprocess.run() │
│  adb -s X shell Y │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Capture output   │
│  stdout + stderr  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  emit event       │
│  'shell_response' │
│  or 'shell_error' │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  xterm.js writes  │
│  to terminal      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  User sees output │
│  New prompt shown │
└───────────────────┘
```

### Reboot Flow

```
User clicks "Reboot Device"
        │
        ▼
┌───────────────────┐
│  Confirmation     │
│  dialog shown     │
└────────┬──────────┘
         │ User confirms
         ▼
┌───────────────────┐
│  Socket.IO emit   │
│  'reboot_device'  │
│  {serial}         │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Flask-SocketIO   │
│  @socketio.on()   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  subprocess.run() │
│  adb -s X reboot  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Check result     │
│  returncode == 0? │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  emit event       │
│  'reboot_response'│
│  {success, ...}   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Alert shown to   │
│  user with result │
└───────────────────┘
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────┐
│              Presentation Layer              │
│  - HTML5                                     │
│  - CSS3 (responsive design)                  │
│  - Vanilla JavaScript                        │
│  - xterm.js (terminal emulator)              │
│  - Socket.IO client                          │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│            Communication Layer               │
│  - WebSocket (Socket.IO protocol)            │
│  - JSON data format                          │
│  - Event-based messaging                     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│            Application Layer                 │
│  - Flask (web framework)                     │
│  - Flask-SocketIO (WebSocket server)         │
│  - Python 3.13                               │
│  - Threading (background monitor)            │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│              System Layer                    │
│  - subprocess (command execution)            │
│  - pyudev (Linux USB monitoring)             │
│  - system_profiler (macOS USB monitoring)    │
│  - ADB (Android Debug Bridge)                │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│              Hardware Layer                  │
│  - USB devices                               │
│  - Android devices                           │
└─────────────────────────────────────────────┘
```

## Threading Model

```
┌─────────────────────────────────────────────┐
│               Main Thread                    │
│  - Flask application                         │
│  - HTTP request handling                     │
│  - Socket.IO event handling                  │
│  - Route serving (/index)                    │
└────────────────┬────────────────────────────┘
                 │
                 │ spawns on first connect
                 │
┌────────────────┴────────────────────────────┐
│          Background Monitor Thread           │
│  - Runs monitor_devices()                   │
│  - Platform-specific monitoring:             │
│    * Linux: pyudev event loop                │
│    * macOS: system_profiler polling          │
│  - Emits device_update events                │
│  - Runs continuously                         │
└─────────────────────────────────────────────┘

Thread Safety:
- thread_lock ensures single monitor thread
- Socket.IO handles concurrent client connections
- Each subprocess call is isolated
```

## Platform-Specific Implementations

### Linux

```
pyudev.Context()
    │
    ▼
pyudev.Monitor.from_netlink()
    │
    ▼
monitor.filter_by(subsystem='usb')
    │
    ▼
Event loop: iter(monitor.poll, None)
    │
    ▼
On 'add' or 'remove' action
    │
    ▼
Emit device_update
```

### macOS

```
system_profiler SPUSBDataType -json
    │
    ▼
Parse JSON output
    │
    ▼
Extract device list
    │
    ▼
Compare with previous list
    │
    ▼
If changed, emit device_update
    │
    ▼
Sleep 1 second
    │
    ▼
Repeat (polling loop)
```

## Security Considerations

```
┌─────────────────────────────────────────────┐
│            Security Boundaries               │
│                                              │
│  Browser ←→ WebSocket (unencrypted)          │
│             ⚠️ Use HTTPS in production       │
│                                              │
│  Flask ←→ ADB (local subprocess)             │
│          ⚠️ Command injection risk           │
│                                              │
│  ADB ←→ Device (USB/network)                 │
│        ✓ Device must have USB debugging on   │
│                                              │
└─────────────────────────────────────────────┘

Mitigations:
- Commands run with server user permissions
- 10-second timeout on all commands
- No persistent shell sessions
- Serial number validation
- Confirmation for destructive operations
```
