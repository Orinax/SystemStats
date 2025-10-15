#!/bin/bash

# Check to see if inxi is installed or not
if ! command -v inxi >/dev/null 2>&1; then
    echo "Error: inxi is not installed."
    echo "Please install inxi with 'sudo apt install inxi' and try again."
    exit 1
fi

# Run inxi and push to server
if ! inxi --output json -Fz > /tmp/sysinfo.json; then
    echo "Error: Failed to run 'inxi --output json -Fz'."
    exit 2
fi

echo "System info collected successfully in /tmp/sysinfo.json."
curl -X POST -H "Content-Type: application/json" --data @/tmp/sysinfo.json https://localhost:5000/submit
