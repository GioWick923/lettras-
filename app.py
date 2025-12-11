import pygame
import sys
import math

# --- CONFIGURACIÓN ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

# Colores (Basados en tu diseño)
COLOR_FONDO = (20, 20, 20)      # Gris oscuro casi negro
COLOR_TEXTO = (255, 255, 255)   # Blanco
# Color crema solicitado (#eeefbe -> RGB)
COLOR_RESALTADO = (238, 239, 190) 

# Configuración de Texto
FONT_SIZE = 36
ESPACIO_LINEAS = 80  # Espacio entre líneas
VELOCIDAD_AUTO = 3   # Segundos por línea

# Texto de ejemplo
LETRA_CANCION = """This is the rhythm of the night
The night, oh, yeah
The rhythm of the night
This is the rhythm of my life
My life, oh, yeah
The rhythm of my life
Oh, yeah
I know you wanna say it
But you can't find the words
To tell me how you feel
"""

class KaraokeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.RESIZABLE)
        pygame.display.set_caption("LyricalFlow Python")
        self.clock = pygame.time.Clock()
        
        # Fuentes
        try:
            self.font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 20)
        except:
            self.font = pygame.font.Font(None, FONT_SIZE)

        # Estado
        self.lines = [line for line in LETRA_CANCION.split('\n') if line.strip()]
        self.current_index = 0
        self.is_playing = False
        self.last_switch_time = 0
        
        # Scroll suave
        self.scroll_y = 0
        self.target_scroll_y = 0

    def draw_text_centered(self, text, y_pos, is_active, alpha=255):
        # Renderizar texto
        color = COLOR_RESALTADO if is_active else COLOR_TEXTO
        
        # Si es pygame, el alpha se maneja diferente dependiendo de la versión,
        # así que usaremos una superficie temporal para la transparencia
        text_surf = self.font.render(text, True, color)
        
        # Crear superficie con transparencia
        alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, alpha))
        
        # Blit texto en alpha surf usando mezcla
        text_surf.set_alpha(alpha)
        
        # Calcular posición X centrada
        rect = text_surf.get_rect(center=(ANCHO_PANTALLA // 2, y_pos))
        
        # Escala: Hacer más grande la línea activa
        if is_active:
            scale = 1.1
            width = int(rect.width * scale)
            height = int(rect.height * scale)
            text_surf = pygame.transform.smoothscale(text_surf, (width, height))
            rect = text_surf.get_rect(center=(ANCHO_PANTALLA // 2, y_pos))
            
            # DIBUJAR SUBRAYADO DIFUMINADO (Simulado)
            # Dibujamos varios rectángulos con baja opacidad para simular el blur
            underline_width = rect.width
            underline_y = rect.bottom - 5
            
            # Glow exterior
            s = pygame.Surface((underline_width + 20, 10), pygame.SRCALPHA)
            pygame.draw.rect(s, (*COLOR_RESALTADO, 30), s.get_rect(), border_radius=5)
            self.screen.blit(s, (rect.centerx - (underline_width + 20)//2, underline_y - 2))
            
            # Línea principal
            s2 = pygame.Surface((underline_width, 4), pygame.SRCALPHA)
            pygame.draw.rect(s2, (*COLOR_RESALTADO, 180), s2.get_rect(), border_radius=2)
            self.screen.blit(s2, (rect.left, underline_y))

        self.screen.blit(text_surf, rect)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            current_time = pygame.time.get_ticks()

            # --- EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    global ANCHO_PANTALLA, ALTO_PANTALLA
                    ANCHO_PANTALLA, ALTO_PANTALLA = event.w, event.h
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_playing = not self.is_playing
                        self.last_switch_time = current_time
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.current_index = min(self.current_index + 1, len(self.lines) - 1)
                        self.last_switch_time = current_time # Reset timer
                    elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.current_index = max(self.current_index - 1, 0)
                        self.last_switch_time = current_time

            # --- LÓGICA ---
            if self.is_playing:
                # Cambiar línea automáticamente cada X segundos
                if current_time - self.last_switch_time > VELOCIDAD_AUTO * 1000:
                    if self.current_index < len(self.lines) - 1:
                        self.current_index += 1
                        self.last_switch_time = current_time
                    else:
                        self.is_playing = False

            # Calcular Scroll Objetivo (Centrar la línea actual)
            # La posición ideal es: Centro de pantalla - (Indice * Espacio)
            target_y = (ALTO_PANTALLA // 2) - (self.current_index * ESPACIO_LINEAS)
            
            # Interpolación lineal para suavidad (Lerp)
            self.scroll_y += (target_y - self.scroll_y) * 0.1

            # --- DIBUJAR ---
            self.screen.fill(COLOR_FONDO)

            # Dibujar todas las líneas
            for i, line in enumerate(self.lines):
                # Posición Y basada en scroll
                y_pos = self.scroll_y + (i * ESPACIO_LINEAS)
                
                # Optimización: No dibujar si está muy fuera de pantalla
                if -50 < y_pos < ALTO_PANTALLA + 50:
                    distancia = abs(i - self.current_index)
                    is_active = (i == self.current_index)
                    
                    # Calcular opacidad (Blur inactive effect)
                    if is_active:
                        alpha = 255
                    else:
                        # Más lejos = más transparente
                        alpha = max(40, 255 - (distancia * 60))
                    
                    self.draw_text_centered(line, y_pos, is_active, alpha)

            # UI Overlay
            status_text = "REPRODUCIENDO" if self.is_playing else "PAUSA (Espacio)"
            ui_surf = self.font_small.render(status_text, True, (100, 100, 100))
            self.screen.blit(ui_surf, (20, 20))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = KaraokeApp()
    app.run()
