import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "MAC": "00:1A:7D:DA:71:13",
    "COM": "COM5",
    "BAUDRATE": "9600",
    "KD": "0.0",
    "KP": "0.9",
    "KI": "0.2",
    "Kv": "0.0",
    "Kvi": "0.0",
    "Vbase": "0.0",
    "Volantazo": "0.0",
    "Umbral": "0.0"
}


def save_config(data):
    config = DEFAULT_CONFIG.copy()
    config.update({k: str(v) for k, v in data.items()})

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        config = DEFAULT_CONFIG.copy()
        config.update({k: str(v) for k, v in data.items()})
        return config

    except (json.JSONDecodeError, OSError):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    
def leer_var_en_json(ruta, nombre_var):
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return datos[nombre_var]