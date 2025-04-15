from pynput import keyboard
import datetime
import json
import pygetwindow as gw
import psutil
import threading
import os

TYPING_TIMEOUT = 1.2  # seconds between keys to consider a new session
exit_key = keyboard.Key.f12

modifier_keys = {
    keyboard.Key.ctrl_l: False,
    keyboard.Key.ctrl_r: False,
    keyboard.Key.alt_l: False,
    keyboard.Key.alt_r: False,
    keyboard.Key.shift_l: False,
    keyboard.Key.shift_r: False,
    keyboard.Key.caps_lock: False
}

# Session storage
current_session = {
    "start_time": None,
    "end_time": None,
    "keys": "",
    "modifiers": [],
    "active_window": "",
    "process": ""
}

last_key_time = None
lock = threading.Lock()

# Get the active window title
def get_active_window_title():
    try:
        window = gw.getActiveWindow()
        return window.title if window else "No active window"
    except:
        return "Unknown window"

# Get the process name for the active window
def get_window_process(title):
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            for window in gw.getWindowsWithTitle(title):
                if hasattr(window, '_getPid'):
                    pid = window._getPid()
                    if proc.info['pid'] == pid:
                        return proc.info['name']
        return "Unknown"
    except:
        return "Unknown"

# Create dynamic log file path based on day/hour
def get_log_file_path():
    now = datetime.datetime.now()
    log_dir = os.path.join("logs", now.strftime("%Y-%m-%d"), now.strftime("%H"))
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "log.jsonl")

# Write session to file and reset
def flush_session():
    global current_session
    if current_session["keys"]:
        current_session["end_time"] = datetime.datetime.now().isoformat(timespec='seconds')
        log_path = get_log_file_path()
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(current_session, ensure_ascii=False) + "\n")
        current_session = {
            "start_time": None,
            "end_time": None,
            "keys": "",
            "modifiers": [],
            "active_window": "",
            "process": ""
        }

# Background watcher to check for typing pause
def check_typing_pause():
    global last_key_time
    while True:
        if last_key_time:
            diff = (datetime.datetime.now() - last_key_time).total_seconds()
            if diff > TYPING_TIMEOUT:
                with lock:
                    flush_session()
                    last_key_time = None
        threading.Event().wait(0.5)

# On key press
def on_press(key):
    global last_key_time, current_session

    with lock:
        now = datetime.datetime.now()

        try:
            key_str = key.char
        except AttributeError:
            key_str = f"[{key.name}]"

        if key == exit_key:
            flush_session()
            print("Exiting...")
            return False

        if current_session["start_time"] is None:
            current_session["start_time"] = now.isoformat(timespec='seconds')
            current_session["active_window"] = get_active_window_title()
            current_session["process"] = get_window_process(current_session["active_window"])

        current_session["keys"] += key_str
        current_session["modifiers"] = [str(k) for k, v in modifier_keys.items() if v]

        last_key_time = now

        if key in modifier_keys:
            modifier_keys[key] = True

# On key release
def on_release(key):
    if key in modifier_keys:
        modifier_keys[key] = False

# Start background typing session watcher
threading.Thread(target=check_typing_pause, daemon=True).start()

# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
