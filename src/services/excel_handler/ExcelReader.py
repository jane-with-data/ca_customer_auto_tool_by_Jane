import pandas as pd
from typing import List, Tuple, Optional
import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent  # Go up 3 levels to project root
sys.path.insert(0, str(project_root))
from src.services.logger_service.Logger import log_info, log_error, log_warning

class ExcelReader:
    def __init__(self, file_path: str, required_cols_lst: Optional[List[str]] = None):
        self.file_path = file_path
        self.required_cols_lst = required_cols_lst or []
        
    def read_excel(self) -> pd.DataFrame:
        """Read Excel file and return DataFrame with validation.
        Returns:
            pd.DataFrame: Loaded DataFrame if successful, None if failed
        """
        
        # Read the Excel file
        log_info(f"Reading Excel file from: {self.file_path}")
        try:
            df = pd.read_excel(self.file_path)
            log_info(f"Reading Excel successful from: {self.file_path}")
        except FileNotFoundError:
            log_error(f"File not found. Please check the file path: {self.file_path}")
            return None
        except Exception as e:
            log_error(f"An error occurred while reading the Excel file: {e}. File path: {self.file_path}")
            return None
        
        # Validate required columns
        is_valid, missing_cols, current_cols = self.validate_required_columns(df, self.required_cols_lst)
        if not is_valid:
            log_error(f"DataFrame is missing required columns: {missing_cols}. Current columns: {current_cols}, file path: {self.file_path}")
            return None
        else:
            log_info(f"Successfully read Excel file, enough required cols, file size: {df.shape}")
            return df
        
    def validate_required_columns(self, df, required_cols_lst):
        """Validate if DataFrame contains all required columns."""
         # Check từng column một
        missing_cols = [col for col in required_cols_lst if col not in df.columns]
        is_valid = len(missing_cols) == 0

        if is_valid:
            return True, [], []
        else:
            return False, missing_cols, df.columns.tolist()
        
# TESTING
if __name__ == "__main__":
    file_path = Path(__file__).parent.parent.parent.parent / "data" / "input" / "phone_check.xlsx"
    print("=== Testing ExcelReader with File Logging ===")
    
    # Test case 1: Successful read
    print("\n--- Test 1: Valid file with required columns ---")
    reader1 = ExcelReader(
        file_path,
        required_cols_lst=["phone"])
    df1 = reader1.read_excel()
    
    # Test case 2: Missing required column
    print("\n--- Test 2: Missing required column ---")
    reader2 = ExcelReader(
        file_path, 
        required_cols_lst=["phone", "nonexistent_column"]
    )
    df2 = reader2.read_excel()
    
    # Test case 3: File not found
    print("\n--- Test 3: File not found ---")
    reader3 = ExcelReader("nonexistent_file.xlsx")
    df3 = reader3.read_excel()
    
    print(f"\n=== Check log files in: data/logs/ ===")