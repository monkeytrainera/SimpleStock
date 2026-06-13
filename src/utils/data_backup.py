import datetime
import os
import zipfile

from src.config.app_config import AppConfig


class DataBackup:
    @staticmethod
    def backup():
        AppConfig.init_directories()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.zip"
        backup_path = os.path.join(AppConfig.BACKUP_DIR, backup_filename)

        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(AppConfig.DB_PATH):
                zipf.write(AppConfig.DB_PATH, os.path.basename(AppConfig.DB_PATH))

            config_dir = AppConfig.CONFIG_DIR
            if os.path.exists(config_dir):
                for root, dirs, files in os.walk(config_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, AppConfig.BASE_DIR)
                        zipf.write(file_path, arcname)

        return backup_path

    @staticmethod
    def restore(backup_path):
        if not os.path.exists(backup_path):
            raise FileNotFoundError("备份文件不存在")

        AppConfig.init_directories()

        with zipfile.ZipFile(backup_path, "r") as zipf:
            zipf.extractall(AppConfig.BASE_DIR)

        return True

    @staticmethod
    def get_backup_list():
        backups = []
        if os.path.exists(AppConfig.BACKUP_DIR):
            for filename in os.listdir(AppConfig.BACKUP_DIR):
                if filename.endswith(".zip"):
                    filepath = os.path.join(AppConfig.BACKUP_DIR, filename)
                    mtime = os.path.getmtime(filepath)
                    backups.append(
                        {
                            "filename": filename,
                            "path": filepath,
                            "size": os.path.getsize(filepath),
                            "date": datetime.datetime.fromtimestamp(mtime).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    )

        backups.sort(key=lambda x: x["date"], reverse=True)
        return backups
