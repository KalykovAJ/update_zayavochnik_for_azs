# text_uploader.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def upload_or_update_txt_on_drive(
        local_excel_path: str,
        folder_id: str,
        credentials_json_path: str = "credentials.json",
) -> str:
    """ Находит txt файл в папке с Excel-заявочником, обновляет его на Google Drive
    (или создает, если его нет) и возвращает прямую ссылку на просмотр/скачивание текста.
    """
    # 1. Поиск txt файла в той же папке
    folder_dir = os.path.dirname(local_excel_path)
    txt_files = [f for f in os.listdir(folder_dir) if f.endswith('.txt')]

    if not txt_files:
        raise FileNotFoundError(f"В папке {folder_dir} не найдено ни одного .txt файла!")

    # Берем первый попавшийся txt файл (или вы можете передавать точное имя)
    local_txt_path = os.path.join(folder_dir, txt_files[0])
    filename_in_cloud = os.path.basename(local_txt_path)

    # 2. Авторизация
    creds = service_account.Credentials.from_service_account_file(
        credentials_json_path, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    print(f"Шаг 1 [TXT]: Поиск файла '{filename_in_cloud}' в папке Google Drive...")

    # 3. Поиск файла в облаке
    query = f"name = '{filename_in_cloud}' and '{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get("files", [])

    media = MediaFileUpload(
        local_txt_path,
        mimetype="text/plain",
        resumable=True
    )

    if files:
        # Если файл есть — обновляем
        file_id = files[0]["id"]
        print(f"Шаг 2 [TXT]: Файл найден (ID: {file_id}). Обновление содержимого...")
        service.files().update(
            fileId=file_id,
            media_body=media,
            fields="id"
        ).execute()
        print("Шаг 3 [TXT]: Текстовый файл успешно обновлен!")
    else:
        # Если файла нет — создаем новый в этой же папке
        print(f"Шаг 2 [TXT]: Файл не найден. Создание нового файла '{filename_in_cloud}'...")
        file_metadata = {
            'name': filename_in_cloud,
            'parents': [folder_id]
        }
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        file_id = file.get('id')
        print(f"Шаг 3 [TXT]: Текстовый файл успешно создан (ID: {file_id})!")

    # 4. Формирование ссылки на просмотр чистого текста
    return f"https://drive.google.com/uc?export=view&id={file_id}"


def run_text_sync(network_name: str, local_excel_file: str, folder_id: str, credentials_path: str = "credentials.json"):
    """Универсальная обертка для синхронизации TXT файла"""
    try:
        print(f"\n--- Начало синхронизации TXT для сети: {network_name} ---")

        txt_link = upload_or_update_txt_on_drive(
            local_excel_path=local_excel_file,
            folder_id=folder_id,
            credentials_json_path=credentials_path
        )

        print(f"Шаг 4 [TXT]: СИНХРОНИЗАЦИЯ ТЕКСТА ЗАВЕРШЕНА ({network_name})!")
        print("=" * 50)
        print("Ссылка на текстовое содержимое:")
        print(txt_link)
        print("=" * 50)
        return txt_link

    except Exception as error:
        print(f"\n❌ Ошибка при обработке TXT для сети {network_name}: {error}")
        return None