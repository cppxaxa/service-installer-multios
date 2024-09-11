import subprocess
import platform

SERVICE_NAME = "ican-machine-identity"
LINUX_SERVICE_EXECUTABLE_PATH = "ican-machine-identity"
WINDOWS_SERVICE_EXECUTABLE_PATH = "ican-machine-identity.exe"

# Check if systemd is available.
def is_systemd_available():
    """Checks if systemd is available."""

    return subprocess.run(["systemctl", "status"], capture_output=True, text=True).returncode == 0

# Create a systemd service file.
def create_systemd_service(service_name, description, exec_start, user="root"):
    """Creates a systemd service file."""

    service_file = f"""
[Unit]
Description={description}

[Service]
Type=simple
User={user}
ExecStart={exec_start}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

    service_file_path = f"/etc/systemd/system/{service_name}.service"

    with open(service_file_path, "w") as f:
        f.write(service_file)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", service_name])
    subprocess.run(["systemctl", "start", service_name])

# Uninstall a systemd service.
def uninstall_systemd_service(service_name):
    """Uninstalls a systemd service."""

    subprocess.run(["systemctl", "stop", service_name])
    subprocess.run(["systemctl", "disable", service_name])
    subprocess.run(["rm", f"/etc/systemd/system/{service_name}.service"])
    subprocess.run(["systemctl", "daemon-reload"])

# Check status of a systemd service.
def check_systemd_service_status(service_name):
    """Checks the status of a systemd service."""

    return subprocess.run(["systemctl", "status", service_name], capture_output=True, text=True).returncode

# Install a systemd service for Linux.
def install_linux_service():
    """Installs a systemd service for Linux."""

    # Copy the executable to the /usr/bin directory.
    subprocess.run(["sudo", "cp", LINUX_SERVICE_EXECUTABLE_PATH, "/usr/bin/"])

    create_systemd_service(
        service_name=SERVICE_NAME,
        description=SERVICE_NAME,
        exec_start=LINUX_SERVICE_EXECUTABLE_PATH,
        user="root",
    )

    print(f"Service {SERVICE_NAME} installed successfully.")

# Uninstall a linux service.
def uninstall_linux_service():
    """Uninstalls a systemd service for Linux."""

    uninstall_systemd_service(SERVICE_NAME)

    subprocess.run(["sudo", "rm", f"/usr/bin/{LINUX_SERVICE_EXECUTABLE_PATH}"])

    print(f"Service {SERVICE_NAME} uninstalled successfully.")

# Check status of a linux service.
def check_linux_service_status():
    """Checks the status of a systemd service."""

    return check_systemd_service_status(SERVICE_NAME)

# Install a windows service.
def install_windows_service():
    """Installs a windows service."""

    # Create a folder in the program files directory.
    subprocess.run(["mkdir", f"C:\\Program Files\\{SERVICE_NAME}"])

    # Copy the executable to the program files directory using copy.
    subprocess.run(["copy", WINDOWS_SERVICE_EXECUTABLE_PATH, f"C:\\Program Files\\{SERVICE_NAME}\\"])

    # Create a service using nssm.
    subprocess.run(["nssm", "install", SERVICE_NAME, f"C:\\Program Files\\{SERVICE_NAME}\\ican-machine-identity.exe"])

    print(f"Service {SERVICE_NAME} installed successfully.")

# Uninstall a windows service.
def uninstall_windows_service():
    """Uninstalls a windows service."""

    subprocess.run(["nssm", "remove", SERVICE_NAME])

    subprocess.run(["rmdir", f"C:\\Program Files\\{SERVICE_NAME}", "/s", "/q"])

    print(f"Service {SERVICE_NAME} uninstalled successfully.")

# Check status of a windows service.
def check_windows_service_status():
    """Checks the status of a windows service."""

    return subprocess.run(["nssm", "status", SERVICE_NAME], capture_output=True, text=True).returncode

# Main.
print("Welcome to the Service Installer Multi OS")
print("1. Install service")
print("2. Uninstall service")
print("3. Check service status")
ch = input("Enter your choice: ")

if ch == "1":
    print("Installing service...")
    # Use platform.system() to determine the OS and install the service accordingly.
    if platform.system() == "Linux":
        if is_systemd_available():
            install_linux_service()
        else:
            print("Systemd is not available. Aborting installation.")
    elif platform.system() == "Windows":
        install_windows_service()
    else:
        print("Unsupported OS.")
elif ch == "2":
    print("Uninstalling service...")
    if platform.system() == "Linux":
        if is_systemd_available():
            uninstall_linux_service()
        else:
            print("Systemd is not available. Aborting uninstallation.")
    elif platform.system() == "Windows":
        uninstall_windows_service()
    else:
        print("Unsupported OS.")
elif ch == "3":
    print("Checking service status...")
    if platform.system() == "Linux":
        if is_systemd_available():
            status = check_linux_service_status()
            if status == 0:
                print(f"Service {SERVICE_NAME} is running.")
            else:
                print(f"Service {SERVICE_NAME} is not running.")
        else:
            print("Systemd is not available. Aborting status check.")
    elif platform.system() == "Windows":
        status = check_windows_service_status()
        if status == 0:
            print(f"Service {SERVICE_NAME} is running.")
        else:
            print(f"Service {SERVICE_NAME} is not running.")
    else:
        print("Unsupported OS.")
