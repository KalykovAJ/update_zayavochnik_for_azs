# run_munay_prom.py
import os
from drive_uploader import run_sync

# НАСТРОЙКИ КОНКРЕТНОЙ СЕТИ АЗС
NETWORK_NAME = "SKY MARKET"
FOLDER_ID = "1xL7KPPcEAV3ydvEkc8brkZ9oNNErJyvH"  # ID папки этой сети
LOCAL_FILE = r"C:\Users\Пользователь\Desktop\Заявочники АЗС\Заявочник SKY MARKET.xlsx"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS = os.path.join(BASE_DIR, "credentials.json")

if __name__ == "__main__":
    run_sync(
        network_name=NETWORK_NAME,
        local_file=LOCAL_FILE,
        folder_id=FOLDER_ID,
        credentials_path=CREDENTIALS
    )