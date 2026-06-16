# run_munay_prom.py
from drive_uploader import run_sync

# НАСТРОЙКИ КОНКРЕТНОЙ СЕТИ АЗС
NETWORK_NAME = "Бишкек Петролеум"
FOLDER_ID = "12pQUXu34SaCVS7mwUBCkBIeI4699iV_z"  # ID папки этой сети
LOCAL_FILE = r"C:\Users\ajkal\OneDrive\Desktop\Заявочники АЗС\Заявочник БП.xlsx"
CREDENTIALS = "credentials.json"  # Можно использовать общие ключи или свои для сети

if __name__ == "__main__":
    run_sync(
        network_name=NETWORK_NAME,
        local_file=LOCAL_FILE,
        folder_id=FOLDER_ID,
        credentials_path=CREDENTIALS
    )