#!/bin/bash

# Check to see that this script is not run with sudo. Exit if sudo is used.
if [ "$EUID" -eq 0 ]; then
    echo "Error: Please do not run this script with sudo or as root."
    echo "inxi can collect private information like serial numbers if sudo is used."
    echo "We do not want to collect any information like that. Please run as a regular user."
    exit 1
fi

# Check to see if inxi is installed or not
if ! command -v inxi >/dev/null 2>&1; then
    echo "Error: inxi is not installed."
    echo "Please install inxi with 'sudo apt install inxi' and try again."
    exit 1
fi

# Run inxi and push to server
if ! (inxi -Sz > /tmp/hardn_test_system.txt &&
      inxi -mz > /tmp/hardn_test_memory.txt &&
      inxi -nz > /tmp/hardn_test_network.txt &&
      inxi -Cz > /tmp/hardn_test_cpu.txt &&
      inxi -Gz > /tmp/hardn_test_graphics.txt &&
      inxi -Mz > /tmp/hardn_test_machine.txt &&
      inxi -Dz > /tmp/hardn_test_drives.txt); then
    echo "Error: One or more inxi commands failed."
    exit 2
fi

echo "System info collected successfully."

python3 parse_inxi_files.py
curl -X POST -H "Content-Type: application/json" --data @inxi_data.json http://localhost:5000/submit
