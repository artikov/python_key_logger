import subprocess
import os

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
    # Assuming your daily_upload.bat file is located in the same directory as the script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(base_dir, "daily_upload.bat")

    create_task("UploadLogsOnLogon", bat_path)
