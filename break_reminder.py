#!/usr/bin/env python3
"""
Async Break Reminder Script for Work Hours

This script sends a desktop notification to remind you to take a break,
but only during work hours as defined in a configuration file.
It starts counting time from when the user signs in (so if you log in at 09:30,
the first notification is sent after the specified interval).
The notification interval (in seconds) and work hours are read from the config file.
The title and message remain fixed.

Configuration file locations:
  - System-wide (default): /etc/break_reminder.conf
  - User override: ${XDG_CONFIG_HOME:-$HOME/.config}/break_reminder.conf

Usage:
    $ python3 /usr/local/bin/break_reminder_work_async.py
"""

import configparser
import datetime
import os
import asyncio
import notify2
from typing import Dict

# Fixed notification title and message
NOTIFICATION_TITLE = "Break Reminder"
NOTIFICATION_MESSAGE = "It's time to take a break and stretch!"

# Default values for configuration
DEFAULT_INTERVAL = 3600 # seconds
DEFAULT_START = "09:00"
DEFAULT_END = "17:00"

# Define configuration file paths:
SYSTEM_CONFIG_PATH = "/etc/xdg/break-reminder.conf"
USER_CONFIG_PATH = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
    "break-reminder.conf"
)


def get_config_path() -> str:
    """Returns the configuration file path.

    If a user-level config exists, it is used; otherwise, the system-wide config is returned.
    """
    return USER_CONFIG_PATH if os.path.exists(USER_CONFIG_PATH) else SYSTEM_CONFIG_PATH


def load_config(config_path: str) -> Dict[str, str]:
    """Loads configuration from an INI file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        A dictionary with keys 'interval', 'start', and 'end'.
    """
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        interval = config.getint("schedule", "interval", fallback=DEFAULT_INTERVAL)
        start_time = config.get("workhours", "start", fallback=DEFAULT_START)
        end_time = config.get("workhours", "end", fallback=DEFAULT_END)
    else:
        interval, start_time, end_time = DEFAULT_INTERVAL, DEFAULT_START, DEFAULT_END
    return {"interval": interval, "start": start_time, "end": end_time}


def parse_time(time_str: str) -> datetime.time:
    """Parses a time string in HH:MM format.

    Args:
        time_str: Time string in HH:MM format.

    Returns:
        A datetime.time object.
    """
    return datetime.datetime.strptime(time_str, "%H:%M").time()


def time_until(target: datetime.datetime) -> float:
    """Returns the number of seconds until the target datetime.

    Args:
        target: The target datetime.

    Returns:
        Seconds until target.
    """
    now = datetime.datetime.now()
    delta = target - now
    return max(delta.total_seconds(), 0)


def send_notification(title: str, message: str, timeout: int = 10) -> None:
    """Sends a desktop notification using notify2.

    Args:
        title: Notification title.
        message: Notification message.
        timeout: Duration (in seconds) for which the notification is displayed.
    """
    notify2.init("BreakNotifier")
    n = notify2.Notification(title, message)
    n.set_timeout(timeout * 1000)  # notify2 expects milliseconds
    n.show()


def within_work_hours(start: datetime.time, end: datetime.time) -> bool:
    """Checks if the current time is within the defined work hours.

    Args:
        start: Work start time.
        end: Work end time.

    Returns:
        True if current time is between start and end, else False.
    """
    now = datetime.datetime.now().time()
    return start <= now <= end


async def sleep_until_work_start(start: datetime.time) -> None:
    """Asynchronously sleeps until the next occurrence of work start time.

    Args:
        start: Work start time.
    """
    now = datetime.datetime.now()
    today_start = datetime.datetime.combine(now.date(), start)
    if now >= today_start:
        tomorrow = now.date() + datetime.timedelta(days=1)
        next_start = datetime.datetime.combine(tomorrow, start)
    else:
        next_start = today_start
    sleep_duration = time_until(next_start)
    print(f"Outside work hours. Sleeping for {sleep_duration:.0f} seconds until work starts at {start}.")
    await asyncio.sleep(sleep_duration)


async def main() -> None:
    """Main async function for the break reminder daemon."""
    config_path = get_config_path()
    config = load_config(config_path)
    interval = config["interval"]
    work_start = parse_time(config["start"])
    work_end = parse_time(config["end"])

    print(f"Using config file: {config_path}")
    print(f"Work hours: {work_start} - {work_end}, Notification interval: {interval} seconds")

    first_run = True
    while True:
        if within_work_hours(work_start, work_end):
            if first_run:
                send_notification(NOTIFICATION_TITLE, "Starting work.", timeout=10)
                print(f"Delaying first notification for {interval} seconds.")
                await asyncio.sleep(interval)
                first_run = False
            else:
                send_notification(NOTIFICATION_TITLE, NOTIFICATION_MESSAGE, timeout=10)
                print(f"Notification sent at {datetime.datetime.now().time()}")
                await asyncio.sleep(interval)
        else:
            first_run = True
            await sleep_until_work_start(work_start)


if __name__ == "__main__":
    asyncio.run(main())
