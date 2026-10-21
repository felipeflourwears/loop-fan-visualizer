import argparse
import io
import json
import os
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import control

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv")
STATE_FILENAME = ".drive_state.json"


def build_drive_service(credentials_path):
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def listar_remotos(service, folder_id):
    remotos = {}
    page_token = None

    while True:
        respuesta = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, md5Checksum)",
            pageToken=page_token,
        ).execute()

        for archivo in respuesta.get("files", []):
            nombre = archivo["name"]
            if nombre.lower().endswith(VIDEO_EXTENSIONS):
                remotos[nombre] = {
                    "id": archivo["id"],
                    "md5Checksum": archivo.get("md5Checksum"),
                }

        page_token = respuesta.get("nextPageToken")
        if not page_token:
            break

    return remotos


def _leer_estado(ruta_estado):
    if not os.path.exists(ruta_estado):
        return {}
    with open(ruta_estado, "r", encoding="utf-8") as f:
        return json.load(f)


def _escribir_estado(ruta_estado, estado):
    with open(ruta_estado, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2)


def _descargar_archivo(service, file_id, destino_final):
    destino_temp = destino_final + ".tmp"
    request = service.files().get_media(fileId=file_id)

    with io.FileIO(destino_temp, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        listo = False
        while not listo:
            _, listo = downloader.next_chunk()

    os.replace(destino_temp, destino_final)


def sync_once(service, folder_id, carpeta_local):
    os.makedirs(carpeta_local, exist_ok=True)
    ruta_estado = os.path.join(carpeta_local, STATE_FILENAME)

    remotos = listar_remotos(service, folder_id)
    estado_previo = _leer_estado(ruta_estado)

    hubo_cambios = False

    for nombre, info in remotos.items():
        checksum_previo = estado_previo.get(nombre, {}).get("md5Checksum")
        if checksum_previo != info["md5Checksum"]:
            destino = os.path.join(carpeta_local, nombre)
            try:
                _descargar_archivo(service, info["id"], destino)
                hubo_cambios = True
            except OSError as err:
                print(f"[drive_sync] No se pudo actualizar '{nombre}': {err}")

    for nombre in estado_previo:
        if nombre not in remotos:
            ruta_local = os.path.join(carpeta_local, nombre)
            if os.path.exists(ruta_local):
                try:
                    os.remove(ruta_local)
                    hubo_cambios = True
                except OSError as err:
                    print(f"[drive_sync] No se pudo borrar '{nombre}': {err}")

    _escribir_estado(ruta_estado, remotos)

    return hubo_cambios


def run_sync_loop(service, folder_id, carpeta_local, intervalo_seg):
    while True:
        try:
            if sync_once(service, folder_id, carpeta_local):
                print("[drive_sync] Playlist actualizada, recargando lista de videos.")
                control.recargar_lista = True
        except Exception as err:
            print(f"[drive_sync] Error durante la sincronizacion: {err}")

        time.sleep(intervalo_seg)


def iniciar_sync_desde_config(config):
    service = build_drive_service(config["credentials_path"])
    carpeta_local = config.get("media_dir", "media")
    intervalo = config.get("sync_interval_seconds", 600)

    run_sync_loop(service, config["drive_folder_id"], carpeta_local, intervalo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sincroniza videos desde Google Drive.")
    parser.add_argument("--credentials", required=True, help="Ruta al JSON de la cuenta de servicio")
    parser.add_argument("--folder-id", required=True, help="ID de la carpeta de Drive")
    parser.add_argument("--media-dir", default="media", help="Carpeta local de destino")
    parser.add_argument("--once", action="store_true", help="Sincroniza una sola vez y termina")
    parser.add_argument("--interval", type=int, default=600, help="Segundos entre sincronizaciones")
    args = parser.parse_args()

    drive_service = build_drive_service(args.credentials)

    if args.once:
        cambio = sync_once(drive_service, args.folder_id, args.media_dir)
        print("Sincronizacion completa. Hubo cambios:" if cambio else "Sincronizacion completa. Sin cambios.")
    else:
        run_sync_loop(drive_service, args.folder_id, args.media_dir, args.interval)
