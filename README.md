# SSH Log Monitor

A lightweight Python script to monitor SSH authentication failures on Linux systems using `journalctl`.  
It logs repeated failed login attempts within a configurable time window and can be extended for alerting or automated blocking.

---

## Features

- Monitors SSH failed authentication logs in real-time using systemd journal (`journalctl`).
- Configurable threshold and time window for alerting on repeated failures.
- Logs detected suspicious activity to a file.
- Minimal dependencies and easy to run on most modern Linux distros with systemd.

---

## Requirements

- Linux system with `systemd` and `journalctl`.
- Python 3.6+
- `argparse` (standard library)
- `subprocess` (standard library)

---

## Usage

1. Clone the repository:

	git clone https://github.com/abhinash-404/ssh-log-monitor.git
	cd ssh-log-monitor

2. Make Sure SSH is Installed and Running:
	
	sudo apt update
	sudo apt install openssh-server -y
	sudo systemctl start ssh

3. Run the Monitor:

	sudo python3 ssh_log_monitor.py

4. Trigger an SSH Failure (for testing)
Open another terminal and run:

	ssh fakeuser@localhost

5. Check Alerts:

	cat /tmp/ssh_alerts.log

📝 Sample Log Output:

[2025-05-25 08:30:13] Failed SSH login from ::1 (user: kali)


🛠 How It Works
- Uses subprocess to run a journalctl command.

- Searches for "authentication failure" messages in SSH logs.

- Logs events to a file.


📁 File Structure
ssh-log-monitor/
├── ssh_log_monitor.py
└── README.md

🧑‍💻 Author
abhinash-404

📜 License
This project is licensed under the MIT License.
