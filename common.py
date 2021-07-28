import json

def get_config(file_path: str) -> dict:
    with open(file_path) as config_file:
        config = json.load(config_file)
    return config