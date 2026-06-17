# run_munay_prom.py
import os
from drive_uploader import run_sync

# НАСТРОЙКИ КОНКРЕТНОЙ СЕТИ АЗС
NETWORK_NAME = "Bishkek Petroleum"
FOLDER_ID = "12pQUXu34SaCVS7mwUBCkBIeI4699iV_z"  # ID папки этой сети
LOCAL_FILE = r"C:\Users\Пользователь\Desktop\Заявочники АЗС\Заявочник БП.xlsx"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS = os.path.join(BASE_DIR, "credentials.json")

if __name__ == "__main__":
    run_sync(
        network_name=NETWORK_NAME,
        local_file=LOCAL_FILE,
        folder_id=FOLDER_ID,
        credentials_path=CREDENTIALS
    )