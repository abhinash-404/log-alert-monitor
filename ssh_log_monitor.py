#!/usr/bin/env python3

import subprocess
import re
import time
from collections import defaultdict

# --- Settings ---
THRESHOLD = 3           # Max allowed failed attempts
WINDOW = 30             # Time window in seconds
ALERT_LOG = "/tmp/ssh_alerts.log"

# Track failed attempts
failures = defaultdict(list)

print("[*] Monitoring SSH failures from journalctl...")

# Run journalctl in follow mode
proc = subprocess.Popen(
    ["journalctl", "-f", "-u", "ssh", "--output", "short"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    for line in proc.stdout:
        if "authentication failure" in line.lower():
            # Extract IP or host (localhost shows as "::1")
            match = re.search(r"rhost=([^\s]+)", line)
            if not match:
                continue

            ip = match.group(1)
            now = time.time()

            # Clean old entries
            failures[ip] = [t for t in failures[ip] if now - t <= WINDOW]

            # Add current time
            failures[ip].append(now)

            print(f"[!] Failed SSH login from {ip} ({len(failures[ip])}x in {WINDOW}s)")

            if len(failures[ip]) >= THRESHOLD:
                with open(ALERT_LOG, "a") as f:
                    f.write(f"[ALERT] {ip} has {len(failures[ip])} failed SSH logins in {WINDOW} seconds\n")
                print(f"[!!] ALERT: {ip} exceeded threshold — logged to {ALERT_LOG}")
                failures[ip] = []  # Reset after alert

except KeyboardInterrupt:
    print("\n[+] Monitoring stopped.")
    proc.terminate()
