import os
import json
from pathlib import Path

class Config:
    RootDirectory = Path(__file__).resolve().parent.parent
    ConfigFile = RootDirectory / "config.json"
    
    @staticmethod
    def load_config():
        try:
            with open(Config.ConfigFile, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {Config.ConfigFile}")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON configuration file: {Config.ConfigFile}")

# Call the load_config method after the class definition
config = Config.load_config()

Config.DEBUG = os.getenv('DEBUG', 'True') == 'True'
Config.PORT = int(os.getenv('PORT', 8000))
Config.BACKEND_API_URL = os.getenv('BACKEND_API_URL', 'http://127.0.0.1:5000/api')