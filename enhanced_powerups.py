# enhanced_powerups.py
"""
Sistema de power-ups mejorado con nuevos efectos y mecánicas avanzadas.
Extiende el sistema de power-ups existente con nuevas funcionalidades.
"""

import pygame
import random
import math
import time
from typing import Dict, List, Tuple, Optional
from powerups import PowerUp

class FreezerPowerUp(PowerUp):
    """Power-up que congela todas las letras por un tiempo determinado."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "congelador", (150, 200, 255), 8.0)  # 8 segundos de duración
        self.freeze_effect_active = False
        self.original_speeds = {}  # Guarda las velocidades originales
    
    def activate(self, game_session):
        """Activa el efecto de congelación."""
        super().activate(game_session)
        self.freeze_effect_active = True
        
        # Guardar velocidades originales y congelar letras
        for letra in game_session.letras:
            if 'original_speed' not in letra:
                letra['original_speed'] = {
                    'vx': letra.get('vx', 0),
                    'vy': letra.get('vy', 0),
                    'icon_vx': letra.get('icon_vx', 0),
                    'icon_vy': letra.get('icon_vy', 0)
                }
            
            # Congelar movimiento
            letra['vx'] = 0
            letra['vy'] = 0
            if 'icon_vx' in letra:
                letra['icon_vx'] = 0
            if 'icon_vy' in letra:
                letra['icon_vy'] = 0
        
        print("¡CONGELADOR ACTIVADO! Todas las letras están congeladas.")
    
    def update(self, game_session):
        """Actualiza el efecto de congelación."""
        super().update(game_session)
        
        if self.freeze_effect_active and not self.active:
            # Restaurar velocidades cuando el efecto termine
            for letra in game_session.letras:
                if 'original_speed' in letra:
                    letra['vx'] = letra['original_speed']['vx']
                    letra['vy'] = letra['original_speed']['vy']
                    if 'icon_vx' in letra:
                        letra['icon_vx'] = letra['original_speed']['icon_vx']
                    if 'icon_vy' in letra:
                        letra['icon_vy'] = letra['original_speed']['icon_vy']
                    del letra['original_speed']
            
            self.freeze_effect_active = False
            print("El efecto de congelación ha terminado.")
    
    def apply_to_new_letter(self, letra):
        """Aplica el efecto de congelación a nuevas letras que aparezcan."""
        if self.freeze_effect_active:
            letra['original_speed'] = {
                'vx': letra.get('vx', 0),
                'vy': letra.get('vy', 0),
                'icon_vx': letra.get('icon_vx', 0),
                'icon_vy': letra.get('icon_vy', 0)
            }
            letra['vx'] = 0
            letra['vy'] = 0
            if 'icon_vx' in letra:
                letra['icon_vx'] = 0
            if 'icon_vy' in letra:
                letra['icon_vy'] = 0

class MagnetPowerUp(PowerUp):
    """Power-up que atrae todas las letras hacia el centro de la pantalla."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "iman", (255, 100, 255), 6.0)  # 6 segundos de duración
        self.magnet_strength = 0.5  # Fuerza de atracción
        self.center_x = 0
        self.center_y = 0
    
    def activate(self, game_session):
        """Activa el efecto magnético."""
        super().activate(game_session)
        
        # Obtener centro de la pantalla desde game_session
        self.center_x = game_session.main.ANCHO // 2
        self.center_y = game_session.main.ALTO // 2
        
        print("¡IMÁN ACTIVADO! Las letras son atraídas hacia el centro.")
    
    def update(self, game_session):
        """Actualiza el efecto magnético."""
        super().update(game_session)
        
        if self.active:
            # Aplicar fuerza magnética a todas las letras
            for letra in game_session.letras:
                # Calcular dirección hacia el centro
                dx = self.center_x - letra['x']
                dy = self.center_y - letra['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 50:  # Solo atraer si está lejos del centro
                    # Normalizar y aplicar fuerza
                    force_x = (dx / distance) * self.magnet_strength
                    force_y = (dy / distance) * self.magnet_strength
                    
                    # Aplicar fuerza a la velocidad
                    letra['vx'] = letra.get('vx', 0) + force_x
                    letra['vy'] = letra.get('vy', 0) + force_y
                    
                    # También atraer el ícono si existe
                    if 'icon_x' in letra and 'icon_y' in letra:
                        icon_dx = self.center_x - letra['icon_x']
                        icon_dy = self.center_y - letra['icon_y']
                        icon_distance = math.sqrt(icon_dx*icon_dx + icon_dy*icon_dy)
                        
                        if icon_distance > 50:
                            icon_force_x = (icon_dx / icon_distance) * self.magnet_strength
                            icon_force_y = (icon_dy / icon_distance) * self.magnet_strength
                            
                            letra['icon_vx'] = letra.get('icon_vx', 0) + icon_force_x
                            letra['icon_vy'] = letra.get('icon_vy', 0) + icon_force_y

class MultiplierPowerUp(PowerUp):
    """Power-up que triplica los puntos obtenidos temporalmente."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "multiplicador", (255, 215, 0), 10.0)  # 10 segundos de duración
        self.multiplier = 3
        self.original_scoring = None
    
    def activate(self, game_session):
        """Activa el multiplicador de puntos."""
        super().activate(game_session)
        
        # Marcar que el multiplicador está activo
        game_session.score_multiplier = self.multiplier
        
        print(f"¡MULTIPLICADOR x{self.multiplier} ACTIVADO! Puntos triplicados.")
    
    def update(self, game_session):
        """Actualiza el multiplicador."""
        super().update(game_session)
        
        if not self.active and hasattr(game_session, 'score_multiplier'):
            # Restaurar multiplicador normal cuando termine
            game_session.score_multiplier = 1
            print("El multiplicador de puntos ha terminado.")

class ExtraLifePowerUp(PowerUp):
    """Power-up que otorga una vida extra (fallo adicional)."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "vida_extra", (255, 100, 100), 0.1)  # Efecto instantáneo
        self.lives_granted = 1
    
    def activate(self, game_session):
        """Otorga vida extra."""
        super().activate(game_session)
        
        # Aumentar el límite de fallos
        if hasattr(game_session, 'game_options') and 'fallos_limit' in game_session.game_options:
            game_session.game_options['fallos_limit'] += self.lives_granted
            print(f"¡VIDA EXTRA! +{self.lives_granted} fallo adicional permitido.")
        
        # Efecto inmediato, se desactiva automáticamente
        self.active = False

class TimeBombPowerUp(PowerUp):
    """Power-up que elimina todas las letras en pantalla después de un tiempo."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "bomba_tiempo", (255, 50, 50), 3.0)  # 3 segundos de cuenta regresiva
        self.countdown = 3.0
        self.warning_sound_played = False
    
    def activate(self, game_session):
        """Inicia la cuenta regresiva de la bomba."""
        super().activate(game_session)
        self.countdown = 3.0
        print("¡BOMBA DE TIEMPO ACTIVADA! Eliminará todas las letras en 3 segundos.")
    
    def update(self, game_session):
        """Actualiza la cuenta regresiva."""
        if self.active:
            self.countdown -= 1/60.0  # Asumiendo 60 FPS
            
            # Sonido de advertencia a 1 segundo
            if self.countdown <= 1.0 and not self.warning_sound_played:
                self.warning_sound_played = True
                # Aquí se podría reproducir un sonido de advertencia
            
            # Explotar cuando llegue a 0
            if self.countdown <= 0:
                self.explode(game_session)
                self.active = False
        
        super().update(game_session)
    
    def explode(self, game_session):
        """Elimina todas las letras y otorga puntos."""
        letters_destroyed = len(game_session.letras)
        
        # Otorgar puntos por cada letra eliminada
        bonus_points = letters_destroyed * 10
        if hasattr(game_session, 'player_managers'):
            for player_id in game_session.player_managers:
                game_session.player_managers[player_id].add_score(bonus_points)
        
        # Eliminar todas las letras
        game_session.letras.clear()
        
        print(f"¡EXPLOSIÓN! {letters_destroyed} letras eliminadas. +{bonus_points} puntos de bonificación.")

class EnhancedPowerUpManager:
    """Gestor mejorado de power-ups con los nuevos tipos."""
    
    def __init__(self):
        self.active_powerups = []
        self.powerup_types = {
            'congelador': FreezerPowerUp,
            'iman': MagnetPowerUp,
            'multiplicador': MultiplierPowerUp,
            'vida_extra': ExtraLifePowerUp,
            'bomba_tiempo': TimeBombPowerUp
        }
        
        # Probabilidades de aparición (suman 100)
        self.spawn_probabilities = {
            'congelador': 20,
            'iman': 20,
            'multiplicador': 15,
            'vida_extra': 10,
            'bomba_tiempo': 10,
            # Los power-ups originales tendrán el 25% restante
        }
    
    def create_random_powerup(self, x: int, y: int) -> PowerUp:
        """Crea un power-up aleatorio en las coordenadas especificadas."""
        rand_val = random.randint(1, 100)
        cumulative = 0
        
        for powerup_type, probability in self.spawn_probabilities.items():
            cumulative += probability
            if rand_val <= cumulative:
                return self.powerup_types[powerup_type](x, y)
        
        # Fallback a congelador si algo sale mal
        return FreezerPowerUp(x, y)
    
    def update_all_powerups(self, game_session):
        """Actualiza todos los power-ups activos."""
        for powerup in self.active_powerups[:]:  # Copia de la lista para modificar durante iteración
            powerup.update(game_session)
            if not powerup.active:
                self.active_powerups.remove(powerup)
    
    def add_powerup(self, powerup: PowerUp):
        """Añade un power-up a la lista de activos."""
        self.active_powerups.append(powerup)
    
    def get_active_powerups_info(self) -> List[Dict]:
        """Obtiene información de todos los power-ups activos."""
        info = []
        for powerup in self.active_powerups:
            info.append({
                'type': powerup.type,
                'remaining_time': powerup.duration,
                'color': powerup.color,
                'active': powerup.active
            })
        return info
    
    def has_active_powerup(self, powerup_type: str) -> bool:
        """Verifica si hay un power-up específico activo."""
        return any(p.type == powerup_type and p.active for p in self.active_powerups)
    
    def clear_all_powerups(self):
        """Elimina todos los power-ups activos."""
        self.active_powerups.clear()

# Función de utilidad para integración con el sistema existente
def create_enhanced_powerup_icons(main_game) -> Dict:
    """Carga iconos para los nuevos power-ups desde archivos de imagen."""
    import os
    
    icons = {}
    icon_size = (60, 60)
    
    # Mapeo de tipos de power-up a archivos de imagen
    powerup_image_files = {
        'congelador': 'hielo.png',
        'iman': 'iman.png',
        'multiplicador': 'x3.png',
        'vida_extra': 'vidaExtra.png',
        'bomba_tiempo': 'bomba_tiempo.png'
    }
    
    # Colores de respaldo si no se puede cargar la imagen
    powerup_colors = {
        'congelador': (150, 200, 255),
        'iman': (255, 100, 255),
        'multiplicador': (255, 215, 0),
        'vida_extra': (255, 100, 100),
        'bomba_tiempo': (255, 50, 50)
    }
    
    for powerup_type, image_file in powerup_image_files.items():
        try:
            # Intentar cargar la imagen desde archivo
            image_path = os.path.join(os.path.dirname(__file__), image_file)
            if os.path.exists(image_path):
                loaded_image = pygame.image.load(image_path).convert_alpha()
                # Escalar la imagen al tamaño deseado
                scaled_image = pygame.transform.scale(loaded_image, icon_size)
                icons[powerup_type] = scaled_image
                print(f"Cargada imagen para {powerup_type}: {image_file}")
            else:
                raise FileNotFoundError(f"No se encontró {image_file}")
                
        except (pygame.error, FileNotFoundError) as e:
            print(f"No se pudo cargar {image_file} para {powerup_type}: {e}")
            print(f"Usando gráfico de respaldo para {powerup_type}")
            
            # Crear gráfico de respaldo
            surface = pygame.Surface(icon_size, pygame.SRCALPHA)
            color = powerup_colors[powerup_type]
            pygame.draw.circle(surface, color, (30, 30), 25)
            pygame.draw.circle(surface, (255, 255, 255), (30, 30), 25, 3)
            
            # Añadir símbolo distintivo de respaldo
            if powerup_type == 'congelador':
                points = [(30, 10), (40, 25), (30, 40), (20, 25)]
                pygame.draw.polygon(surface, (255, 255, 255), points)
            elif powerup_type == 'iman':
                pygame.draw.arc(surface, (255, 255, 255), (15, 15, 30, 30), 0, 3.14, 5)
            elif powerup_type == 'multiplicador':
                font = pygame.font.Font(None, 24)
                text = font.render("x3", True, (0, 0, 0))
                surface.blit(text, (18, 20))
            elif powerup_type == 'vida_extra':
                pygame.draw.circle(surface, (255, 255, 255), (25, 22), 8)
                pygame.draw.circle(surface, (255, 255, 255), (35, 22), 8)
                points = [(20, 25), (30, 40), (40, 25)]
                pygame.draw.polygon(surface, (255, 255, 255), points)
            elif powerup_type == 'bomba_tiempo':
                pygame.draw.circle(surface, (0, 0, 0), (30, 35), 12)
                pygame.draw.line(surface, (255, 255, 255), (30, 23), (30, 15), 3)
            
            icons[powerup_type] = surface
    
    return icons
