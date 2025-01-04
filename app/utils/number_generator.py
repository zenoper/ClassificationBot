import json
import os
from pathlib import Path

class UniqueNumberGenerator:
    def __init__(self):
        self.file_path = Path("data/last_number.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            with open(self.file_path, 'w') as f:
                json.dump({"last_number": 9999}, f)  # Start from 9999 so next number will be 10000

    def get_next_number(self) -> str:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            current = data["last_number"]
        
        next_number = current + 1
        
        with open(self.file_path, 'w') as f:
            json.dump({"last_number": next_number}, f)
        
        return str(next_number) 