# backup_configs.py – Cisco IOS Configuration Backup Script

## Purpose
`backup_configs.py` is a Python script that automates the backup of **running configurations** from Cisco IOS routers.

The script connects to routers over SSH, executes operational commands, and saves the full running configuration to local files.

This script is **read-only**. It does not modify device configuration.

---

## What This Script Solves
In many environments, configuration backups are performed manually by logging into devices and copying configurations. This process is:

- Time-consuming
- Error-prone
- Difficult to repeat consistently

This script automates configuration backups so they can be performed **reliably and repeatedly** across multiple devices.

---

## Files Used by the Script

### `backup_configs.py`
The main Python script that performs the configuration backup.

### `devices.yaml`
Inventory file containing device connection details:
- Device name
- Management IP address
- SSH username and password
- Enable secret

The script reads this file to determine **which devices to back up**.

---

## What the Script Does

For each router in the inventory, the script:

- Establishes an SSH connection
- Enters enable mode
- Executes `show running-config`
- Saves the output to a local file
- Names the file using the device name

Each router is processed independently.

---

## How the Script Works (Step-by-Step)

1. Load device inventory from `devices.yaml`
2. Loop through each device
3. Establish SSH connection using Netmiko
4. Enter enable mode
5. Run `show running-config`
6. Capture command output
7. Write configuration to a local text file
8. Close SSH connection
9. Repeat for next device

---

## Script Output

The script creates one file per device.

### Example Output Files

```text
R1_running_config.txt
R2_running_config.txt
