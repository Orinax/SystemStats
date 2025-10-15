#!/bin/bash
inxi --output json -Fz > /tmp/sysinfo.json
curl -X POST -H "Content-Type: application/json" --data @/tmp/sysinfo.json https://localhost
