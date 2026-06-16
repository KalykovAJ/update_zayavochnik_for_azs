import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Область доступа (запись и обновление файлов, к которым разрешен доступ)
SCOPES = ["https://www.googleapis.com/auth/drive"]


def update_zayavka_on_google_drive(
        local_path: str,
        folder_id: str,
        credentials_json_path: str = "credentials.json",
) -> str:
    """Находит существующий файл на Google Диске по имени локального файла

    и обновляет его содержимое. Возвращает вечную ссылку на прямое скачивание.

    :param local_path: Путь к файлу на вашем ПК (откуда берем имя и данные)
    :param folder_id: Чистый ID папки на Google Диске
    :param credentials_json_path: Путь к файлу ключей сервисного аккаунта
    :return: Строка с вечной ссылкой на ПРЯМОЕ скачивание сотрудниками АЗС
    """
    if not os.path.exists(local_path):
        raise FileNotFoundError(
            f"Локальный файл не найден по пути: {local_path}"
        )

    # Имя файла в облаке всегда строго соответствует локальному имени
    filename_in_cloud = os.path.basename(local_path)

    # 1. Авторизация через сервисный аккаунт
    creds = service_account.Credentials.from_service_account_file(
        credentials_json_path, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    print(f"Поиск файла '{filename_in_cloud}' в папке на Google Диске...")

    # 2. Ищем файл с таким именем конкретно в целевой папке
    query = f"name = '{filename_in_cloud}' and '{folder_id}' in parents and trashed = false"
    results = (
        service.files()
        .list(q=query, fields="files(id)")
        .execute()
    )
    files = results.get("files", [])

    if not files:
        raise FileNotFoundError(
            f"Ошибка: Файл '{filename_in_cloud}' не найден в облачной папке!\n"
            f"Пожалуйста, создайте его один раз вручную через браузер."
        )

    file_id = files[0]["id"]
    print(f"Файл найден (ID: {file_id}). Подготовка к перезаписи...")

    # 3. Подготавливаем новые бинарные данные для загрузки
    media = MediaFileUpload(
        local_path,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        resumable=True,
    )

    # 4. Обновляем «начинку» файла (ID, имя и ссылка при этом не меняются)
    service.files().update(
        fileId=file_id,
        media_body=media,
        fields="id"
    ).execute()

    print("Данные в облаке успешно обновлены!")

    # 5. Формируем неизменяемую ссылку на ПРЯМОЕ скачивание
    direct_download_url = (
        f"https://drive.google.com/uc?export=download&id={file_id}"
    )

    return direct_download_url


# =====================================================================
# ЗАПУСК СКРИПТА:
# =====================================================================
if __name__ == "__main__":
    # Сюда вставляйте только чистый ID папки (набор букв и цифр)
    FOLDER_ID = "1YAPLQ3UDZldk_244REmhhDj6sQuT2Q6j"

    # Путь к вашему локальному файлу, который генерирует openpyxl
    LOCAL_FILE = r"C:\Users\ajkal\OneDrive\Desktop\Заявочники АЗС\Заявочник БП.xlsx"

    try:
        final_link = update_zayavka_on_google_drive(
            local_path=LOCAL_FILE,
            folder_id=FOLDER_ID,
            credentials_json_path="credentials.json",
        )

        print("\n" + "=" * 50)
        print(" СИНХРОНИЗАЦИЯ С GOOGLE DRIVE ЗАВЕРШЕНА!")
        print("=" * 50)
        print("Эту ссылку отдайте на АЗС (прямое скачивание):")
        print(final_link)
        print("=" * 50)

    except Exception as error:
        print(f"\n❌ Ошибка: {error}")