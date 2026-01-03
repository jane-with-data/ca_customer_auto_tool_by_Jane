# config.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql
import logging

load_dotenv()

class Config:
    # YouTube API
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER','root')
    DB_PASSWORD = os.getenv('DB_PASSWORD',123456789)
    DB_NAME = os.getenv('DB_NAME', 'dev_etl')
    
    # Storage
    STORAGE_PATH = os.getenv('STORAGE_PATH', './data')
    
    # Channels to track
    CHANNEL_IDS = os.getenv('CHANNEL_IDS', 'UCc0jat47dKDF7X104CwNCKQ,UCM9KgI3IytaTL9hr0vhXxuQ').split(',')
    # CHANNEL_IDS = ['UCc0jat47dKDF7X104CwNCKQ', 'UCM9KgI3IytaTL9hr0vhXxuQ']
    # Scheduling
    SCHEDULE_HOUR = int(os.getenv('SCHEDULE_HOUR', 6))  # 6 AM
    SCHEDULE_MINUTE = int(os.getenv('SCHEDULE_MINUTE', 0))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'pipeline.log')
    
    @property
    def db_engine(self):
        """Create database engine"""
        db_url = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return create_engine(db_url, echo=False, pool_recycle=3600)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
