#!/usr/bin/env python3
"""
Quick test script to verify the application can start and basic functionality works
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from product_hub import device_monitor

        print("✓ device_monitor imported successfully")

        from flask import Flask

        print("✓ Flask imported")

        from flask_socketio import SocketIO

        print("✓ Flask-SocketIO imported")

        import platform

        print(f"✓ Platform detected: {platform.system()}")

        if platform.system() == "Linux":
            import pyudev

            print("✓ pyudev imported (Linux)")

        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_adb_available():
    """Test if ADB is available in PATH"""
    print("\nTesting ADB availability...")
    import subprocess

    try:
        result = subprocess.run(
            ["adb", "version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            print(f"✓ ADB is available: {version_line}")
            return True
        else:
            print("✗ ADB command failed")
            return False
    except FileNotFoundError:
        print("✗ ADB not found in PATH")
        print("  Install ADB to use device monitoring features")
        return False
    except Exception as e:
        print(f"✗ Error checking ADB: {e}")
        return False


def test_device_monitor_functions():
    """Test that device_monitor functions are accessible"""
    print("\nTesting device_monitor functions...")
    try:
        from product_hub import device_monitor

        # Test platform detection
        platform = device_monitor.PLATFORM
        print(f"✓ Platform detection: {platform}")

        # Test get_adb_devices function exists
        assert hasattr(device_monitor, "get_adb_devices")
        print("✓ get_adb_devices function exists")

        # Test monitor_devices function exists
        assert hasattr(device_monitor, "monitor_devices")
        print("✓ monitor_devices function exists")

        # Test socket handlers exist
        assert hasattr(device_monitor, "handle_reboot")
        print("✓ handle_reboot handler exists")

        assert hasattr(device_monitor, "handle_shell_command")
        print("✓ handle_shell_command handler exists")

        return True
    except Exception as e:
        print(f"✗ Function test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Product Hub - Quick Test Suite")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("ADB", test_adb_available()))
    results.append(("Functions", test_device_monitor_functions()))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✓ All tests passed! Application is ready to run.")
        print("\nStart the server with:")
        print("  poetry run python -m src.product_hub.device_monitor")
        print("\nThen open: http://localhost:5000")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
