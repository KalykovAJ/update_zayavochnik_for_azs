# run_munay_prom.py
from drive_uploader import run_sync

# НАСТРОЙКИ КОНКРЕТНОЙ СЕТИ АЗС
NETWORK_NAME = "Партнер Нефть"
FOLDER_ID = "11qDmmyMzouE8vFVGdT3aXGHEJJDa1Zu8"  # ID папки этой сети
LOCAL_FILE = r"C:\Users\ajkal\OneDrive\Desktop\Заявочники АЗС\Заявочник ПН.xlsx"
CREDENTIALS = "credentials.json"  # Можно использовать общие ключи или свои для сети

if __name__ == "__main__":
    run_sync(
        network_name=NETWORK_NAME,
        local_file=LOCAL_FILE,
        folder_id=FOLDER_ID,
        credentials_path=CREDENTIALS
    )