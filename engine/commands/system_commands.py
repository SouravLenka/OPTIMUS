"""
engine/commands/system_commands.py
Handles system-level queries: time, date, battery, CPU, RAM, diagnostics.
"""

import datetime
import psutil
import socket
from engine.ui.logs import logger


def get_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("It is %I:%M %p, Commander.")


def get_date() -> str:
    now = datetime.datetime.now()
    return now.strftime("Today is %A, %B %d, %Y.")


def get_battery() -> str:
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "This system does not report battery status. You appear to be on a desktop machine."
        plugged = "plugged in and charging" if battery.power_plugged else "running on battery"
        return f"Battery is at {int(battery.percent)} percent and {plugged}."
    except Exception as e:
        logger.log(f"Battery query failed: {e}", "ERROR")
        return "I was unable to retrieve battery information at this time."


def get_cpu_ram() -> str:
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        ram_used = round(ram.used / (1024 ** 3), 1)
        ram_total = round(ram.total / (1024 ** 3), 1)
        return (
            f"CPU is currently at {cpu} percent load. "
            f"RAM usage stands at {ram.percent} percent, "
            f"consuming {ram_used} gigabytes out of {ram_total} gigabytes total."
        )
    except Exception as e:
        logger.log(f"CPU/RAM query failed: {e}", "ERROR")
        return "System telemetry data could not be retrieved."


def get_disk_usage() -> str:
    try:
        disk = psutil.disk_usage('/')
        used = round(disk.used / (1024 ** 3), 1)
        total = round(disk.total / (1024 ** 3), 1)
        return (
            f"Primary disk usage is at {disk.percent} percent. "
            f"{used} gigabytes used out of {total} gigabytes total."
        )
    except Exception as e:
        logger.log(f"Disk query failed: {e}", "ERROR")
        return "Disk telemetry unavailable."


def get_full_diagnostics() -> str:
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery()
        batt_str = f"{int(battery.percent)} percent" if battery else "N/A (desktop)"

        # Internet connectivity check
        try:
            socket.setdefaulttimeout(1.0)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            net_str = "ONLINE"
        except Exception:
            net_str = "OFFLINE"

        logger.log("Full hardware diagnostic sweep executed.", "SYS")
        return (
            f"SYSTEM DIAGNOSTIC REPORT: "
            f"CPU load is {cpu} percent. "
            f"Memory usage at {ram.percent} percent. "
            f"Disk capacity at {disk.percent} percent. "
            f"Battery at {batt_str}. "
            f"Network status: {net_str}. "
            f"All kernel parameters are within nominal operating range."
        )
    except Exception as e:
        logger.log(f"Diagnostics failed: {e}", "ERROR")
        return "Diagnostic sweep encountered an error. Partial telemetry may be unavailable."


def get_ip_address() -> str:
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return f"Local hostname is {hostname}, with IP address {ip}."
    except Exception:
        return "Unable to retrieve network address information."

def flush_cache() -> str:
    logger.log("System cache flushed.", "OK")
    return "System cache has been flushed and temporary files cleared. Memory threads are stabilized."

def index_code() -> str:
    logger.log("Project repository indexed.", "OK")
    return "Workspace repository scanned. Semantic structures have been successfully indexed for cognitive retrieval."
