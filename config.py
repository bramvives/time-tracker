import json
import os
from dataclasses import dataclass


@dataclass
class Config:
    db_path: str = "./data/db.sqlite"

    @classmethod
    def load(cls, config_file: str = "./data/config.json") -> "Config":
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                data = json.load(f)
                return cls(**data)
        else:
            config = cls()
            config.save(config_file)
            return config

    def save(self, config_file: str = "./data/config.json") -> None:
        config_dir = os.path.dirname(config_file)
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
        with open(config_file, "w") as f:
            json.dump({"db_path": self.db_path}, f, indent=2)
