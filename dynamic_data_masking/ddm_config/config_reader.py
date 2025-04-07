import os
from dotenv import load_dotenv
import importlib.resources

class ConfigReader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._load_env()
        return cls._instance

    def _load_env(self):
        try:
            # Access the .env file inside the installed package using importlib.resources
            with importlib.resources.path(
                "dynamic_data_masking.ddm_config.env_config", ".env"
            ) as env_path:
                if env_path.exists():
                    load_dotenv(env_path)
        except Exception as e:
            print(f"⚠️ Could not load .env file: {e}")

    def get(self, key, default=None):
        value = os.getenv(key, default)
        if value is None:
            print(f"⚠️ Warning: {key} not found in environment variables.")
        return value


# Singleton instance for convenient access
config = ConfigReader()

