import json
import re


def split_fields(line):
    # Split so each field label (ending with ':') starts a new line
    return re.sub(r' (?=[\w]+:)', r'\n', line).split('\n')

def flat_parse_inxi(filename):
    result = {}
    idx = 1  # Numbering for keys
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            # If it's a section header (ends with ':')
            if re.match(r'^\s*\w+:$', line):
                section = line.strip().rstrip(':')
                result[f"{idx}. {section}"] = ""
                idx += 1
            else:
                # Split multi-field lines into separate fields
                split_lines = split_fields(line.strip())
                for field in split_lines:
                    parts = field.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        result[f"{idx}. {key}"] = value
                        idx += 1
                    elif field.strip():  # For lines without ':' but not empty
                        result[f"{idx}. {field.strip()}"] = ""
                        idx += 1
    return result


system = flat_parse_inxi('/tmp/hardn_test_system.txt')
memory = flat_parse_inxi('/tmp/hardn_test_memory.txt')
network = flat_parse_inxi('/tmp/hardn_test_network.txt')
cpu = flat_parse_inxi('/tmp/hardn_test_cpu.txt')
graphics = flat_parse_inxi('/tmp/hardn_test_graphics.txt')
machine = flat_parse_inxi('/tmp/hardn_test_machine.txt')
drives = flat_parse_inxi('/tmp/hardn_test_drives.txt')

data = {
        "system": system,
        "memory": memory,
        "network": network,
        "cpu": cpu,
        "graphics": graphics,
        "machine": machine,
        "drives": drives,
}

with open('inxi_data.json', 'w') as f:
    json.dump(data, f, indent=2)

