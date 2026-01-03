import datetime
import inspect
import os
from pathlib import Path
from typing import Optional

class Logger:
    """Centralized logger for all classes."""
    
    _instance = None
    _log_base_dir = None
    
    def __new__(cls, log_base_dir: str = "data/logs"):
        """Singleton pattern - chỉ tạo 1 instance duy nhất."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._log_base_dir = Path(log_base_dir)
        return cls._instance
    
    def log(self, level: str, message: str, class_name: Optional[str] = None, func_name: Optional[str] = None):
        """Central logging method."""
        # Auto-detect class and function if not provided
        if class_name is None or func_name is None:
            frame = inspect.currentframe().f_back
            
            # 🔥 FIX: Skip convenience functions to get to the real caller
            convenience_functions = ['log_info', 'log_error', 'log_warning', 'log_debug']
            while frame and frame.f_code.co_name in convenience_functions:
                frame = frame.f_back
            
            if frame is None:
                class_name = class_name or "Unknown"
                func_name = func_name or "Unknown"
            else:
                if class_name is None:
                    # Try to get class name from frame
                    if 'self' in frame.f_locals:
                        class_name = frame.f_locals['self'].__class__.__name__
                    else:
                        class_name = "Unknown"
                if func_name is None:
                    func_name = frame.f_code.co_name
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}][{level}][{class_name}][{func_name}] {message}"
        
        # Print to console
        print(log_message)
        
        # Write to file
        self._write_to_file(level, log_message)
    
    def _write_to_file(self, level: str, log_message: str):
        """Write log to file."""
        try:
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            log_dir = self._log_base_dir / level.lower()
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"{current_date}.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"[ERROR] Failed to write log: {e}")

# Global logger instance
logger = Logger()

# Convenience functions
def log_info(message: str):
    """Log INFO level message."""
    logger.log("INFO", message)

def log_error(message: str):
    """Log ERROR level message."""
    logger.log("ERROR", message)

def log_warning(message: str):
    """Log WARNING level message."""
    logger.log("WARNING", message)

def log_debug(message: str):
    """Log DEBUG level message."""
    logger.log("DEBUG", message)
