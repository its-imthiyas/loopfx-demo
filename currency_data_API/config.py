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

config = Config.load_config()
Config.DB_PATH = (Config.RootDirectory / config["DB_PATH"]).resolve()
Config.DATA_FOLDER = (Config.RootDirectory / config["DATA_FOLDER"]).resolve()
Config.CURRENCYPAIRS = config["CURRENCY_PAIRS"]

Config.DEBUG = os.getenv('DEBUG', 'True') == 'True'
Config.PORT = int(os.getenv('PORT', 5000))