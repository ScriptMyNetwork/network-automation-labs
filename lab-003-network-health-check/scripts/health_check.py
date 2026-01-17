from netmiko import ConnectHandler
import yaml
import re
import json
from datetime import datetime

CPU_WARNING = 70
CPU_CRITICAL = 85

MEM_WARNING = 75
MEM_CRITICAL = 90

MIN_UPTIME_MINUTES = 10


def load_devices():
    with open("devices.yaml") as f:
        return yaml.safe_load(f)["devices"]


def check_cpu(output):
    match = re.search(r"five seconds:\s+(\d+)%", output)
    if not match:
        return {"status": "UNKNOWN", "value": None}

    cpu = int(match.group(1))

    if cpu >= CPU_CRITICAL:
        status = "CRITICAL"
    elif cpu >= CPU_WARNING:
        status = "WARNING"
    else:
        status = "PASS"

    return {"status": status, "value": cpu}


def check_memory(output):
    """
    Uses Processor Pool statistics
    """
    match = re.search(
        r"Processor Pool Total:\s+(\d+)\s+Used:\s+(\d+)\s+Free:\s+(\d+)",
        output
    )

    if not match:
        return {"status": "UNKNOWN", "value": None}

    total = int(match.group(1))
    used = int(match.group(2))
    percent_used = int((used / total) * 100)

    if percent_used >= MEM_CRITICAL:
        status = "CRITICAL"
    elif percent_used >= MEM_WARNING:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "status": status,
        "used_percent": percent_used
    }


def check_uptime(output):
    """
    Detect recent reloads
    """
    match = re.search(r"uptime is (.+)", output)
    if not match:
        return {"status": "UNKNOWN"}

    uptime_text = match.group(1)

    minutes = 0
    days = re.search(r"(\d+) day", uptime_text)
    hours = re.search(r"(\d+) hour", uptime_text)
    mins = re.search(r"(\d+) minute", uptime_text)

    if days:
        minutes += int(days.group(1)) * 1440
    if hours:
        minutes += int(hours.group(1)) * 60
    if mins:
        minutes += int(mins.group(1))

    if minutes < MIN_UPTIME_MINUTES:
        return {
            "status": "CRITICAL",
            "uptime": uptime_text
        }

    return {
        "status": "PASS",
        "uptime": uptime_text
    }


def check_routing(output):
    """
    Fail if no usable routes are present in the routing table
    Excludes headers and legend lines
    """

    route_lines = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue
        if line.startswith("Codes:"):
            continue
        if line.startswith("Gateway of last resort"):
            continue
        if re.match(r"^[A-Z\*]+ ", line):
            route_lines.append(line)

    route_count = len(route_lines)

    if route_count == 0:
        return {
            "status": "CRITICAL",
            "routes": 0
        }

    return {
        "status": "PASS",
        "routes": route_count
    }



def run_health_checks(device):
    result = {
        "device": device["name"],
        "host": device["host"],
        "checks": {}
    }

    print(f"\nConnecting to {device['name']} ({device['host']})")

    try:
        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["host"],
            username=device["username"],
            password=device["password"],
        )

        cpu_output = conn.send_command("show processes cpu")
        mem_output = conn.send_command("show processes memory")
        ver_output = conn.send_command("show version")
        route_output = conn.send_command("show ip route summary")

        result["checks"]["cpu"] = check_cpu(cpu_output)
        result["checks"]["memory"] = check_memory(mem_output)
        result["checks"]["uptime"] = check_uptime(ver_output)
        result["checks"]["routing"] = check_routing(route_output)

        conn.disconnect()

    except Exception as e:
        result["error"] = str(e)

    return result


def generate_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n========== NETWORK HEALTH REPORT ==========")
    print(f"Generated at: {timestamp}\n")

    for device in results:
        print(f"Device: {device['device']} ({device['host']})")

        if "error" in device:
            print(f"  ERROR: {device['error']}")
            continue

        for check, data in device["checks"].items():
            status = data.get("status", "UNKNOWN")
            print(f"  {check.upper():10}: {status}  {data}")

        print("")

    with open("health_report.json", "w") as f:
        json.dump(results, f, indent=2)


def main():
    devices = load_devices()
    results = []

    for device in devices:
        results.append(run_health_checks(device))

    generate_report(results)


if __name__ == "__main__":
    main()
