import subprocess
import platform
import os
import shutil
import time

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

# Check if the systemd service files is present or not.
def check_linux_service_installation_status():
    """Checks the systemd service files is present or not."""

    service_file_path = f"/etc/systemd/system/{SERVICE_NAME}.service"
    return os.path.exists(service_file_path)

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

    folder_path = f"C:\\Program Files\\{SERVICE_NAME}"

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        time.sleep(0.6)

    # Create a folder in the program files directory.
    os.makedirs(folder_path)

    # Copy the executable to the program files directory using copy.
    shutil.copy2(WINDOWS_SERVICE_EXECUTABLE_PATH, f"C:\\Program Files\\{SERVICE_NAME}\\")

    # Get pwd.
    pwd = os.getcwd()

    # Append with nssm.exe.
    nssm_path = os.path.join(pwd, "nssm.exe")

    # Create a service using nssm.
    subprocess.run([nssm_path, "install", SERVICE_NAME, f"C:\\Program Files\\{SERVICE_NAME}\\ican-machine-identity.exe"])

    # Start the service.
    ret = subprocess.run([nssm_path, "start", SERVICE_NAME])

    status = False
    for _ in range(10):
        time.sleep(0.5)
        status = check_windows_service_status()
        if status:
            break

    if status:
        print(f"Service {SERVICE_NAME} started successfully.")
    else:
        print(f"Service {SERVICE_NAME} failed to start.")

# Uninstall a windows service.
def uninstall_windows_service():
    """Uninstalls a windows service."""

    # Get pwd.
    pwd = os.getcwd()

    # Append with nssm.exe.
    nssm_path = os.path.join(pwd, "nssm.exe")

    subprocess.run([nssm_path, "stop", SERVICE_NAME])

    for _ in range(10):
        if not check_windows_service_status():
            break
        time.sleep(0.5)
        subprocess.run([nssm_path, "stop", SERVICE_NAME])

    subprocess.run([nssm_path, "remove", SERVICE_NAME, "confirm"])

    shutil.rmtree(f"C:\\Program Files\\{SERVICE_NAME}")

    print(f"Service {SERVICE_NAME} uninstalled successfully.")

# Check installation status of a windows service.
def check_windows_service_installation_status():
    """Checks the status of a windows service."""

    # Get pwd.
    pwd = os.getcwd()

    # Append with nssm.exe.
    nssm_path = os.path.join(pwd, "nssm.exe")

    return subprocess.run([nssm_path, "status", SERVICE_NAME]).returncode == 0

# Check if string matches with nssm output.
def nssm_contains(nssm_output, string_value):
    if string_value in nssm_output:
        return True
    
    nssm_format = ''.join([el for (idx, el) in enumerate(nssm_output) if idx % 2 == 1])

    if string_value in nssm_format:
        return True
    
    nssm_format = ''.join([el for (idx, el) in enumerate(nssm_output) if idx % 2 == 0])

    return string_value in nssm_format

# Check installation status of a windows service.
def check_windows_service_status():
    """Check installation status of a windows service"""
    
    # Get pwd.
    pwd = os.getcwd()

    # Append with nssm.exe.
    nssm_path = os.path.join(pwd, "nssm.exe")

    ret = subprocess.run([nssm_path, "status", SERVICE_NAME], capture_output=True, text=True)
    return nssm_contains(ret.stdout, "SERVICE_RUNNING")


# Main.
print("Welcome to the Service Installer Multi OS")
print("1. Install service")
print("2. Uninstall service")
print("3. Check service installation status")
print("4. Check service running status")
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
            status = check_linux_service_installation_status()
            if status:
                print(f"Service {SERVICE_NAME} is available.")
            else:
                print(f"Service {SERVICE_NAME} is not available.")
        else:
            print("Systemd is not available. Aborting status check.")
    elif platform.system() == "Windows":
        status = check_windows_service_installation_status()
        if status:
            print(f"Service {SERVICE_NAME} is available.")
        else:
            print(f"Service {SERVICE_NAME} is not available.")
    else:
        print("Unsupported OS.")
elif ch == "4":
    print("Checking service running status...")
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
        if status:
            print(f"Service {SERVICE_NAME} is running.")
        else:
            print(f"Service {SERVICE_NAME} is not running.")
    else:
        print("Unsupported OS.")
