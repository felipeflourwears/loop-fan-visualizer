import pygame
import cv2
import os
import numpy as np

def reproducir_videos_en_carpeta(carpeta, lado_ventana):
    pygame.init()

    archivos = [f for f in os.listdir(carpeta) if f.endswith(('.mp4', '.avi', '.mkv'))]
    if not archivos:
        print("No se encontraron videos.")
        return

    lado = lado_ventana
    screen = pygame.display.set_mode((lado, lado), pygame.NOFRAME)

    clock = pygame.time.Clock()

    # Loop Videos
    while True:
        for archivo in archivos:
            cap = cv2.VideoCapture(os.path.join(carpeta, archivo))
            if not cap.isOpened():
                print(f"No se pudo abrir el video {archivo}")
                continue

            # FPS
            fps = cap.get(cv2.CAP_PROP_FPS)
            #fps=30
            if fps == 0:
                fps = 30 

            print(f"Reproduciendo {archivo} a {fps:.2f} FPS...")

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cap.release()
                        pygame.quit()
                        return

                ret, frame = cap.read()
                if not ret:
                    break

                # Convertir BGR a RGB y ajustar tamaño al cuadrado
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (lado, lado))
                frame_surface = pygame.surfarray.make_surface(np.transpose(frame_resized, (1, 0, 2)))

                # Dibujar frame en pantalla
                screen.blit(frame_surface, (0, 0))

                # Dibujar borde cuadrado rojo
                pygame.draw.rect(screen, (255, 0, 0), (0, 0, lado, lado), 5)

                pygame.display.update()

                # Respetar los FPS del video
                clock.tick(fps)

            cap.release()

    pygame.quit()

# Ruta carpeta de videos
videos = r"C:\Users\hp\Documents\Github\Ventilador\media"
# Tamaño de la ventana cuadrada en píxeles
ventilador = 518
reproducir_videos_en_carpeta(videos, ventilador)
