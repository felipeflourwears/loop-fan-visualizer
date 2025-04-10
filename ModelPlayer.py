import pygame
import cv2
import os
import numpy as np

class VideoPlayer:
    def __init__(self, carpeta, lado_ventana, fps=-1):
        self.carpeta = carpeta
        self.lado = lado_ventana
        self.fps = fps
        self.archivos = [f for f in os.listdir(carpeta) if f.endswith(('.mp4', '.avi', '.mkv'))]

        if not self.archivos:
            raise FileNotFoundError("No se encontraron videos en la carpeta especificada.")

        pygame.init()
        self.screen = pygame.display.set_mode((self.lado, self.lado), pygame.NOFRAME)
        self.clock = pygame.time.Clock()

    def reproducir(self):
        while True:
            for archivo in self.archivos:
                ruta_video = os.path.join(self.carpeta, archivo)
                cap = cv2.VideoCapture(ruta_video)

                if not cap.isOpened():
                    print(f"No se pudo abrir el video {archivo}")
                    continue

                fps_actual = self.fps if self.fps != -1 else cap.get(cv2.CAP_PROP_FPS)
                print(f"Reproduciendo {archivo} a {fps_actual:.2f} FPS...")

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            cap.release()
                            pygame.quit()
                            return

                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_resized = cv2.resize(frame_rgb, (self.lado, self.lado))
                    frame_surface = pygame.surfarray.make_surface(np.transpose(frame_resized, (1, 0, 2)))

                    self.screen.blit(frame_surface, (0, 0))
                    pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, self.lado, self.lado), 5)
                    pygame.display.update()
                    self.clock.tick(fps_actual)

                cap.release()

        pygame.quit()
