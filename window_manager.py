import platform
import ctypes

def minimize_terminal():
    """Minimizes the terminal window (Windows only)."""
    if platform.system() == "Windows":
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                # SW MINIMIZE = 6
                ctypes.windll.user32.ShowWindow(hwnd, 6)  # 6 = Minimize
        except Exception:
            pass

    elif platform.system() == "Darwin":
        try:
            # Uses AppleScript to tell the default Terminal app to minimize window 1.
            # This send a command to the OS scripting bridge.
            cmd = "tell application \"Terminal\" to set miniaturized of window 1 to true"
            os.system(f"osascript -e '{cmd}'")
        except Exception:
            pass

def restore_terminal():
    """Restores the terminal window (Windows only)."""
    if platform.system() == "Windows":
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                # SW RESTORE = 9
                ctypes.windll.user32.ShowWindow(hwnd, 9)  # 9 = Restore
                ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception:
            pass
    
    elif platform.system() == "Darwin":
        try:
            # Tells the Terminal app to un-minimize window and bring it to front.
            cmd = """
            tell application "Terminal
                set miniaturized of window 1 to false
                activate
            end tell
            """
            # We execute this as a single AppleScript command
            os.system(f"osascript -e '{cmd}'")
        except Exception:
            pass
        