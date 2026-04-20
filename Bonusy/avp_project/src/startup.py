"""Windows startup registration helpers."""

import os
import sys

try:
    import winreg
except ImportError:  # pragma: no cover
    winreg = None

from .constants import APP_ID, AUTOSTART_REGISTRY_RUN_KEY


class StartupManager:
    """Manage the application's Run entry in the Windows registry."""

    def is_supported(self):
        """Return True when the current environment provides winreg."""
        return winreg is not None

    def is_enabled(self):
        """Return True when the autostart registry entry is present and non-empty."""
        if not self.is_supported():
            return False

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REGISTRY_RUN_KEY, 0, winreg.KEY_READ) as registry_key:
                registry_value, _ = winreg.QueryValueEx(registry_key, APP_ID)
                return bool(registry_value)
        except FileNotFoundError:
            return False
        except OSError:
            return False

    def set_enabled(self, enabled):
        """Enable or disable autostart for the current user.

        The application is registered in HKCU so that administrator rights are
        not required for this specific feature.
        """
        if not self.is_supported():
            raise RuntimeError("Windows autostart is not available on this platform.")

        executable_command = self._build_launch_command()

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            AUTOSTART_REGISTRY_RUN_KEY,
            0,
            winreg.KEY_SET_VALUE,
        ) as registry_key:
            if enabled:
                winreg.SetValueEx(registry_key, APP_ID, 0, winreg.REG_SZ, executable_command)
            else:
                try:
                    winreg.DeleteValue(registry_key, APP_ID)
                except FileNotFoundError:
                    pass

    def _build_launch_command(self):
        """Return the exact command string stored in the Run registry key."""
        executable_path = os.path.abspath(sys.argv[0])
        file_extension = os.path.splitext(executable_path)[1].lower()

        if file_extension == ".pyw":
            pythonw_path = sys.executable
            return f'"{pythonw_path}" "{executable_path}"'

        return f'"{executable_path}"'
