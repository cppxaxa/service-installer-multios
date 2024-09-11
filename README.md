# Service Installer Multi OS

This script allows you to install, uninstall, and check the status of a service on both Linux (using systemd) and Windows operating systems.

## Usage

1. **Install the service:**
   - The script will detect the operating system and install the service accordingly.

2. **Uninstall the service:**
   - The script will detect the operating system and uninstall the service accordingly.

3. **Check service status:**
   - The script will detect the operating system and display the service status.

## Requirements

- Windows x64, Linux x64

## Example Usage

**Install the service on Linux:**

```bash
chmod +x python-multios.exe
./python-multios.exe service-installer-multios.py
```

**Uninstall the service on Windows:**

```bash
python-multios.exe service-installer-multios.py
```

**Check service status on Linux:**

```bash
python-multios.exe service-installer-multios.py
```

## Notes

- The service name is defined in the `SERVICE_NAME` variable in the script.
- The script assumes that the service is configured correctly for the respective operating system.
- For Linux, the script uses `systemd` to manage the service. If `systemd` is not available, the installation and uninstallation will fail.
- For Windows, the script uses the built-in Windows service management tools.

## License

This script is licensed under the MIT License or Apache License 2.0
