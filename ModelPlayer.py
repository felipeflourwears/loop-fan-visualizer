import pygame
import cv2
import os
import numpy as np
import control

class VideoPlayer:
    def __init__(self, carpeta, lado_ventana, fps=-1):
        self.carpeta = carpeta
        self.lado = lado_ventana
        self.fps = fps
        self.archivos = [f for f in os.listdir(carpeta) if f.endswith(('.mp4', '.avi', '.mkv'))]

        if not self.archivos:
            raise FileNotFoundError("No hay videos en la carpeta")

        # ===== PARÁMETROS DE CALIBRACIÓN =====
        self.offset_x = 0      # prueba: -5, +5, etc
        self.offset_y = 0
        self.radio_ref = self.lado // 2 - 5  # círculo ligeramente más pequeño
        self.modo_calibracion = True         # ON para alinear, OFF para uso final
        # ===================================

        pygame.init()
        self.screen = pygame.display.set_mode((self.lado, self.lado), pygame.NOFRAME)
        self.clock = pygame.time.Clock()

    def reproducir(self):
        while True:
            idx = control.video_index % len(self.archivos)
            ruta_video = os.path.join(self.carpeta, self.archivos[idx])
            cap = cv2.VideoCapture(ruta_video)

            fps_actual = self.fps if self.fps != -1 else cap.get(cv2.CAP_PROP_FPS)

            while cap.isOpened():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cap.release()
                        pygame.quit()
                        return

                if control.cambiar_video:
                    control.cambiar_video = False
                    break

                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.lado, self.lado))
                frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                # === BLIT CON DESFASE CONTROLADO ===
                self.screen.fill((0, 0, 0))
                self.screen.blit(frame, (self.offset_x, self.offset_y))

                # === CÍRCULO ROJO DE REFERENCIA ===
                if self.modo_calibracion:
                    pygame.draw.circle(
                        self.screen,
                        (255, 0, 0),
                        (self.lado // 2, self.lado // 2),
                        self.radio_ref,
                        2
                    )

                pygame.display.update()
                self.clock.tick(fps_actual)

            cap.release()