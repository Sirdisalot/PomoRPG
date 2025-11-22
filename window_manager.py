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