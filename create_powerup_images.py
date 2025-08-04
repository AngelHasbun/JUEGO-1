#!/usr/bin/env python3
"""
Script para crear las imágenes de los nuevos power-ups.
Genera imágenes PNG de alta calidad para cada power-up.
"""

import pygame
import math
import os

# Inicializar pygame para crear imágenes
pygame.init()

def create_magnet_image():
    """Crea la imagen del power-up Imán (iman.png)"""
    size = (64, 64)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colores del imán
    red = (220, 50, 50)
    blue = (50, 50, 220)
    silver = (200, 200, 200)
    dark_gray = (80, 80, 80)
    
    # Dibujar forma de herradura (imán)
    center_x, center_y = 32, 32
    
    # Cuerpo principal del imán
    pygame.draw.circle(surface, silver, (center_x, center_y), 28)
    pygame.draw.circle(surface, (40, 40, 40), (center_x, center_y), 28, 3)
    
    # Parte superior (polo norte - rojo)
    pygame.draw.arc(surface, red, (8, 8, 48, 48), 0, math.pi, 12)
    
    # Parte inferior (polo sur - azul)
    pygame.draw.arc(surface, blue, (8, 8, 48, 48), math.pi, 2*math.pi, 12)
    
    # Líneas de campo magnético
    for i in range(3):
        offset = (i - 1) * 8
        pygame.draw.arc(surface, (100, 100, 255, 150), 
                       (center_x - 20 + offset, center_y - 20, 40, 40), 
                       0, math.pi, 2)
    
    # Brillos
    pygame.draw.circle(surface, (255, 255, 255, 180), (center_x - 8, center_y - 8), 6)
    
    return surface

def create_ice_image():
    """Crea la imagen del power-up Congelador (hielo.webp -> hielo.png)"""
    size = (64, 64)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colores del hielo
    ice_blue = (150, 200, 255)
    light_blue = (200, 230, 255)
    white = (255, 255, 255)
    dark_blue = (100, 150, 200)
    
    center_x, center_y = 32, 32
    
    # Cristal de hielo principal (forma de diamante)
    points = [
        (center_x, center_y - 24),      # Arriba
        (center_x + 20, center_y - 8),  # Derecha arriba
        (center_x + 16, center_y + 16), # Derecha abajo
        (center_x, center_y + 24),      # Abajo
        (center_x - 16, center_y + 16), # Izquierda abajo
        (center_x - 20, center_y - 8),  # Izquierda arriba
    ]
    
    # Sombra del cristal
    shadow_points = [(x + 2, y + 2) for x, y in points]
    pygame.draw.polygon(surface, (50, 50, 100, 100), shadow_points)
    
    # Cristal principal
    pygame.draw.polygon(surface, ice_blue, points)
    pygame.draw.polygon(surface, dark_blue, points, 2)
    
    # Facetas internas del cristal
    inner_points = [
        (center_x, center_y - 12),
        (center_x + 10, center_y),
        (center_x, center_y + 12),
        (center_x - 10, center_y)
    ]
    pygame.draw.polygon(surface, light_blue, inner_points)
    
    # Brillos y reflejos
    pygame.draw.circle(surface, white, (center_x - 6, center_y - 10), 4)
    pygame.draw.circle(surface, (255, 255, 255, 150), (center_x + 8, center_y - 6), 3)
    
    # Copos de nieve alrededor
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x = center_x + int(28 * math.cos(rad))
        y = center_y + int(28 * math.sin(rad))
        
        # Pequeños copos
        pygame.draw.circle(surface, white, (x, y), 2)
        pygame.draw.line(surface, white, (x-3, y), (x+3, y), 1)
        pygame.draw.line(surface, white, (x, y-3), (x, y+3), 1)
    
    return surface

def create_multiplier_image():
    """Crea la imagen del power-up Multiplicador (x3.png)"""
    size = (64, 64)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colores dorados
    gold = (255, 215, 0)
    dark_gold = (200, 170, 0)
    light_gold = (255, 240, 100)
    orange = (255, 140, 0)
    
    center_x, center_y = 32, 32
    
    # Fondo circular dorado
    pygame.draw.circle(surface, gold, (center_x, center_y), 28)
    pygame.draw.circle(surface, dark_gold, (center_x, center_y), 28, 3)
    
    # Anillo interior
    pygame.draw.circle(surface, light_gold, (center_x, center_y), 22)
    pygame.draw.circle(surface, orange, (center_x, center_y), 22, 2)
    
    # Texto "x3" grande y llamativo
    font = pygame.font.Font(None, 36)
    text_surface = font.render("x3", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    
    # Sombra del texto
    shadow_surface = font.render("x3", True, (100, 50, 0))
    surface.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))
    
    # Texto principal
    surface.blit(text_surface, text_rect)
    
    # Brillos en los bordes
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x = center_x + int(26 * math.cos(rad))
        y = center_y + int(26 * math.sin(rad))
        pygame.draw.circle(surface, (255, 255, 255, 200), (x, y), 3)
    
    # Brillo central
    pygame.draw.circle(surface, (255, 255, 255, 150), (center_x - 8, center_y - 8), 5)
    
    return surface

def create_extra_life_image():
    """Crea la imagen del power-up Vida Extra (vidaExtra.png)"""
    size = (64, 64)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colores del corazón
    red = (220, 50, 50)
    dark_red = (180, 30, 30)
    pink = (255, 100, 150)
    white = (255, 255, 255)
    
    center_x, center_y = 32, 32
    
    # Sombra del corazón
    shadow_points = [
        (center_x + 2, center_y + 22),  # Punta inferior
        (center_x - 14, center_y + 2),  # Izquierda
        (center_x - 14, center_y - 6),  # Izquierda arriba
        (center_x - 6, center_y - 14),  # Centro izquierda
        (center_x + 2, center_y - 10),  # Centro
        (center_x + 10, center_y - 14), # Centro derecha
        (center_x + 18, center_y - 6),  # Derecha arriba
        (center_x + 18, center_y + 2),  # Derecha
    ]
    pygame.draw.polygon(surface, (100, 20, 20, 150), shadow_points)
    
    # Corazón principal
    # Círculos superiores
    pygame.draw.circle(surface, red, (center_x - 8, center_y - 8), 12)
    pygame.draw.circle(surface, red, (center_x + 8, center_y - 8), 12)
    
    # Triángulo inferior
    heart_points = [
        (center_x, center_y + 20),      # Punta inferior
        (center_x - 16, center_y),      # Izquierda
        (center_x + 16, center_y),      # Derecha
    ]
    pygame.draw.polygon(surface, red, heart_points)
    
    # Bordes del corazón
    pygame.draw.circle(surface, dark_red, (center_x - 8, center_y - 8), 12, 2)
    pygame.draw.circle(surface, dark_red, (center_x + 8, center_y - 8), 12, 2)
    pygame.draw.polygon(surface, dark_red, heart_points, 2)
    
    # Brillos en el corazón
    pygame.draw.circle(surface, pink, (center_x - 12, center_y - 12), 4)
    pygame.draw.circle(surface, pink, (center_x + 4, center_y - 12), 4)
    pygame.draw.circle(surface, white, (center_x - 10, center_y - 10), 2)
    
    # Cruz médica (símbolo de vida/salud)
    cross_color = white
    # Línea vertical
    pygame.draw.rect(surface, cross_color, (center_x - 2, center_y - 6, 4, 12))
    # Línea horizontal
    pygame.draw.rect(surface, cross_color, (center_x - 6, center_y - 2, 12, 4))
    
    # Partículas de vida alrededor
    for angle in range(0, 360, 72):
        rad = math.radians(angle)
        x = center_x + int(30 * math.cos(rad))
        y = center_y + int(30 * math.sin(rad))
        pygame.draw.circle(surface, (255, 200, 200, 180), (x, y), 2)
    
    return surface

def create_time_bomb_image():
    """Crea la imagen del power-up Bomba de Tiempo (bomba_tiempo.png)"""
    size = (64, 64)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colores de la bomba
    black = (40, 40, 40)
    dark_gray = (80, 80, 80)
    red = (220, 50, 50)
    orange = (255, 140, 0)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    
    center_x, center_y = 32, 40
    
    # Sombra de la bomba
    pygame.draw.circle(surface, (20, 20, 20, 150), (center_x + 2, center_y + 2), 18)
    
    # Cuerpo principal de la bomba
    pygame.draw.circle(surface, black, (center_x, center_y), 16)
    pygame.draw.circle(surface, dark_gray, (center_x, center_y), 16, 2)
    
    # Brillo en la bomba
    pygame.draw.circle(surface, (100, 100, 100), (center_x - 6, center_y - 6), 4)
    
    # Mecha de la bomba
    mecha_points = [
        (center_x, center_y - 16),
        (center_x - 2, center_y - 24),
        (center_x + 4, center_y - 30),
        (center_x + 2, center_y - 36),
    ]
    
    # Dibujar mecha
    for i in range(len(mecha_points) - 1):
        pygame.draw.line(surface, (139, 69, 19), mecha_points[i], mecha_points[i + 1], 3)
    
    # Chispa en la punta de la mecha
    spark_x, spark_y = mecha_points[-1]
    pygame.draw.circle(surface, red, (spark_x, spark_y), 3)
    pygame.draw.circle(surface, orange, (spark_x, spark_y), 2)
    pygame.draw.circle(surface, yellow, (spark_x, spark_y), 1)
    
    # Partículas de chispa
    for i in range(5):
        angle = math.radians(i * 72)
        px = spark_x + int(8 * math.cos(angle))
        py = spark_y + int(8 * math.sin(angle))
        pygame.draw.circle(surface, (255, 200, 100, 200), (px, py), 1)
    
    # Números del temporizador en la bomba
    font = pygame.font.Font(None, 20)
    timer_text = font.render("3", True, red)
    text_rect = timer_text.get_rect(center=(center_x, center_y))
    surface.blit(timer_text, text_rect)
    
    return surface

def main():
    """Función principal para crear todas las imágenes"""
    print("Creando imágenes de power-ups...")
    
    # Crear directorio si no existe
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Crear las imágenes
    images = {
        "iman.png": create_magnet_image(),
        "hielo.png": create_ice_image(),  # Cambio de .webp a .png
        "x3.png": create_multiplier_image(),
        "vidaExtra.png": create_extra_life_image(),
        "bomba_tiempo.png": create_time_bomb_image()
    }
    
    # Guardar las imágenes
    for filename, surface in images.items():
        filepath = os.path.join(current_dir, filename)
        pygame.image.save(surface, filepath)
        print(f"[OK] Creada: {filename}")
    
    print("¡Todas las imágenes de power-ups han sido creadas exitosamente!")
    
    # Mostrar las imágenes creadas (opcional)
    print("\nImágenes creadas:")
    for filename in images.keys():
        print(f"  - {filename}")

if __name__ == "__main__":
    main()
    pygame.quit()
