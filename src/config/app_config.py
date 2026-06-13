import os

class AppConfig:
    APP_NAME = "极简库存管理系统"
    APP_VERSION = "1.0.0"
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    BACKUP_DIR = os.path.join(BASE_DIR, "backup")
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    CONFIG_DIR = os.path.join(BASE_DIR, "config")
    
    DB_NAME = "simple_stock.db"
    DB_PATH = os.path.join(DATA_DIR, DB_NAME)
    
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_LEVEL = "INFO"
    
    BACKUP_PATH = BACKUP_DIR
    
    @staticmethod
    def init_directories():
        os.makedirs(AppConfig.DATA_DIR, exist_ok=True)
        os.makedirs(AppConfig.BACKUP_DIR, exist_ok=True)
        os.makedirs(AppConfig.LOG_DIR, exist_ok=True)
        os.makedirs(AppConfig.CONFIG_DIR, exist_ok=True)
