import logging
import os
from src.config.app_config import AppConfig

class Logger:
    _logger = None
    
    @staticmethod
    def get_logger():
        if Logger._logger is None:
            AppConfig.init_directories()
            
            Logger._logger = logging.getLogger('SimpleStock')
            Logger._logger.setLevel(getattr(logging, AppConfig.LOG_LEVEL))
            
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(module)s | %(message)s'
            )
            
            file_handler = logging.FileHandler(AppConfig.LOG_FILE, encoding='utf-8')
            file_handler.setFormatter(formatter)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            Logger._logger.addHandler(file_handler)
            Logger._logger.addHandler(console_handler)
        
        return Logger._logger
    
    @staticmethod
    def debug(message):
        Logger.get_logger().debug(message)
    
    @staticmethod
    def info(message):
        Logger.get_logger().info(message)
    
    @staticmethod
    def warning(message):
        Logger.get_logger().warning(message)
    
    @staticmethod
    def error(message):
        Logger.get_logger().error(message)
