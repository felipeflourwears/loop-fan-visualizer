import json
import os
from threading import Thread

from dotenv import load_dotenv

load_dotenv()

from server import run_server
from ModelPlayer import VideoPlayer
from drive_sync import iniciar_sync_desde_config

CONFIG_PATH = "config.json"


def cargar_config():
    # Prioridad: variables de entorno (.env); config.json se mantiene como respaldo
    if os.getenv("DRIVE_FOLDER_ID"):
        return {
            "drive_folder_id": os.environ["DRIVE_FOLDER_ID"],
            "credentials_path": os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json"),
            "media_dir": os.getenv("MEDIA_DIR", "media"),
            "sync_interval_seconds": int(os.getenv("SYNC_INTERVAL_SECONDS", "600")),
        }

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    return None


def iniciar_drive_sync():
    config = cargar_config()
    if config is None:
        print("[main] No se encontro DRIVE_FOLDER_ID en .env ni config.json, se omite la sincronizacion con Drive.")
        return

    try:
        iniciar_sync_desde_config(config)
    except Exception as err:
        print(f"[main] No se pudo iniciar la sincronizacion con Drive: {err}")


if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()
    Thread(target=iniciar_drive_sync, daemon=True).start()

    player = VideoPlayer(
        carpeta="media",
        lado_ventana=648,
        fps=-1
    )
    player.reproducir()

#648