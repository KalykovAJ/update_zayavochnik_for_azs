# drive_uploader.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def update_zayavka_on_google_drive(
        local_path: str,
        folder_id: str,
        credentials_json_path: str = "credentials.json",
) -> str:
    """Находит существующий файл на Google Диске по имени локального файла
    и обновляет его содержимое. Возвращает прямую ссылку на скачивание.
    """
    if not os.path.exists(local_path):
        raise FileNotFoundError(
            f"Локальный файл не найден по пути: {local_path}"
        )

    filename_in_cloud = os.path.basename(local_path)

    # 1. Авторизация
    creds = service_account.Credentials.from_service_account_file(
        credentials_json_path, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    print(f"Поиск файла '{filename_in_cloud}' в папке Google Drive...")

    # 2. Поиск файла в облаке
    query = f"name = '{filename_in_cloud}' and '{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get("files", [])

    if not files:
        raise FileNotFoundError(
            f"Ошибка: Файл '{filename_in_cloud}' не найден в облачной папке!\n"
            f"Пожалуйста, создайте его один раз вручную через браузер."
        )

    file_id = files[0]["id"]
    print(f"Файл найден (ID: {file_id}). Обновление содержимого...")

    # 3. Загрузка новых данных
    media = MediaFileUpload(
        local_path,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        resumable=True,
    )

    service.files().update(
        fileId=file_id,
        media_body=media,
        fields="id"
    ).execute()

    print("Данные в облаке успешно обновлены!")

    # 4. Формирование прямой ссылки
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def run_sync(network_name: str, local_file: str, folder_id: str, credentials_path: str = "credentials.json"):
    """Универсальная обертка для запуска синхронизации и красивого вывода в консоль"""
    try:
        print(f"\n Начало синхронизации для сети: {network_name}")
        print("-" * 50)

        final_link = update_zayavka_on_google_drive(
            local_path=local_file,
            folder_id=folder_id,
            credentials_json_path=credentials_path,
        )

        print("\n" + "=" * 50)
        print(f" СИНХРОНИЗАЦИЯ С GOOGLE DRIVE ЗАВЕРШЕНА ({network_name})!")
        print("=" * 50)
        print("Ссылка для сотрудников АЗС (прямое скачивание):")
        print(final_link)
        print("=" * 50)

    except Exception as error:
        print(f"\n❌ Ошибка при обработке сети {network_name}: {error}")