from threading import Thread
from server import run_server
from ModelPlayer import VideoPlayer

if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()

    player = VideoPlayer(
        carpeta="media",
        lado_ventana=648,
        fps=-1
    )
    player.reproducir()

#648