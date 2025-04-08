import pygame
import cv2
import os
import numpy as np

def crear_mascara_circular(diametro):
    mascara = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    centro = (diametro // 2, diametro // 2)
    radio = diametro // 2
    pygame.draw.circle(mascara, (255, 255, 255, 255), centro, radio)
    return mascara

def reproducir_videos_en_carpeta(carpeta, diametro_ven):
    pygame.init()

    archivos = [f for f in os.listdir(carpeta) if f.endswith(('.mp4', '.avi', '.mkv'))]
    if not archivos:
        print("No se encontraron videos.")
        return

    diametro = diametro_ven
    screen = pygame.display.set_mode((diametro, diametro), pygame.NOFRAME)

    # Mascara
    mascara = crear_mascara_circular(diametro)

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

                # THRESHOLD BGR TO RGB MISMO COLOR
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (diametro, diametro))
                frame_surface = pygame.surfarray.make_surface(np.transpose(frame_resized, (1, 0, 2)))

                #APLICAR MASCARA
                frame_surface.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                
                #CONTORNO COLOR ROJO
                pygame.draw.circle(frame_surface, (255, 0, 0), (diametro // 2, diametro // 2), diametro // 2, 5)

                screen.fill((0, 0, 0))
                screen.blit(frame_surface, (0, 0))
                pygame.display.update()

                # RESPETAR LOS FPS PARA TENER LA MISMA VELOCIDAD DE LOS VIDEOS
                clock.tick(fps)

            cap.release()

    pygame.quit()

# RUTA CARPETA VIDEOS
#videos = r"C:\Users\it\Videos\Videos"
videos = r"C:\Users\hp\Documents\Github\Ventilador\media"
#PIXELES DIAMETRO VENTILADOR
ventilador = 518
reproducir_videos_en_carpeta(videos, ventilador)

