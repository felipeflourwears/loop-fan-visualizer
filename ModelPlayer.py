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
        
        # Cargar todos los archivos multimedia de la carpeta
        self.archivos = self._cargar_archivos()

        if not self.archivos:
            raise FileNotFoundError(f"No hay videos en la carpeta: {carpeta}")

        # ===== PARÁMETROS DE CALIBRACIÓN =====
        self.offset_x = 0      
        self.offset_y = 0
        self.radio_ref = self.lado // 2 - 5  
        self.modo_calibracion = True         
        # ===================================

        pygame.init()
        self.screen = pygame.display.set_mode((self.lado, self.lado), pygame.NOFRAME)
        self.clock = pygame.time.Clock()

    def _cargar_archivos(self):
        return sorted([f for f in os.listdir(self.carpeta) if f.endswith(('.mp4', '.avi', '.mkv'))])

    def reproducir(self):
        # Índice interno para controlar el loop de la lista de archivos
        indice_actual = 0

        while True:
            # Si drive_sync bajó/borró videos, recargamos la lista antes de elegir el siguiente
            if getattr(control, 'recargar_lista', False):
                control.recargar_lista = False
                nuevos_archivos = self._cargar_archivos()
                if nuevos_archivos:
                    self.archivos = nuevos_archivos
                    indice_actual = indice_actual % len(self.archivos)

            # Si 'control' fuerza un cambio de índice, lo usamos; si no, usamos el ciclo normal
            if hasattr(control, 'video_index'):
                idx = control.video_index % len(self.archivos)
            else:
                idx = indice_actual % len(self.archivos)

            ruta_video = os.path.join(self.carpeta, self.archivos[idx])
            cap = cv2.VideoCapture(ruta_video)

            # Obtener FPS del video original si no se especifica uno fijo
            fps_video = cap.get(cv2.CAP_PROP_FPS)
            fps_actual = self.fps if self.fps > 0 else (fps_video if fps_video > 0 else 30)

            while cap.isOpened():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cap.release()
                        pygame.quit()
                        return

                # Si hay una señal externa para cambiar de video
                if getattr(control, 'cambiar_video', False):
                    control.cambiar_video = False
                    break

                ret, frame = cap.read()
                
                # Al llegar al final del video actual, salimos para pasar al siguiente
                if not ret:
                    break

                # Procesamiento de imagen para Pygame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.lado, self.lado))
                frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                # Renderizado
                self.screen.fill((0, 0, 0))
                self.screen.blit(frame, (self.offset_x, self.offset_y))

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

            # Avanza automáticamente al siguiente video en la lista de la carpeta media
            indice_actual = (idx + 1) % len(self.archivos)
            if hasattr(control, 'video_index'):
                control.video_index = indice_actual