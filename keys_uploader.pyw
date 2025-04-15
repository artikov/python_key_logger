import os
import zipfile
import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def authenticate():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    return GoogleDrive(gauth)

def zip_log_folder(date_str):
    folder = os.path.join("logs", date_str)
    zip_path = os.path.join("logs_archive", f"{date_str}.zip")
    
    if not os.path.exists(folder):
        print(f"[!] Log folder not found: {folder}")
        return None

    os.makedirs("logs_archive", exist_ok=True)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=folder)
                zipf.write(full_path, arcname=rel_path)

    print(f"[✓] Zipped folder: {zip_path}")
    return zip_path

def upload_zip_to_drive(filepath, folder_id='1mAbhRjT-ELqCsmvhQSSvBpcYDpYzEsqE'):
    drive = authenticate()
    file = drive.CreateFile({
        'title': os.path.basename(filepath),
        'parents': [{"id": folder_id}] if folder_id else []
    })
    file.SetContentFile(filepath)
    file.Upload()
    print(f"[✓] Uploaded: {filepath}")

def main():
    date_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    zip_path = os.path.join("logs_archive", f"{date_str}.zip")

    if not os.path.exists(zip_path):
        zip_path = zip_log_folder(date_str)

    if zip_path and os.path.exists(zip_path):
        upload_zip_to_drive(zip_path)
    else:
        print("[!] No zip to upload.")

if __name__ == "__main__":
    main()
