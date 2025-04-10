# main.py

from ModelPlayer import VideoPlayer

if __name__ == "__main__":
    carpeta_videos = r"C:\Users\hp\Documents\Github\Ventilador\media"
    lado_ventana = 518
    fps = -1  # -1 para usar el FPS original del video, o un valor específico

    reproductor = VideoPlayer(carpeta=carpeta_videos, lado_ventana=lado_ventana, fps=fps)
    reproductor.reproducir()
