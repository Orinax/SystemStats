#!/bin/bash

# Check to see if inxi is installed or not
if ! command -v inxi >/dev/null 2>&1; then
    echo "Error: inxi is not installed."
    echo "Please install inxi with 'sudo apt install inxi' and try again."
    exit 1
fi

# Run inxi and push to server
if ! inxi -Fz > /tmp/sysinfo.txt; then
    echo "Error: Failed to run 'inxi -Fz'."
    exit 2
fi

echo "System info collected successfully in /tmp/sysinfo.txt."
curl -X POST -H "Content-Type: application/json" --data @/tmp/sysinfo.json http://localhost:5000/submit
