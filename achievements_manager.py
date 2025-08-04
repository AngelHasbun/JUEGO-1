# achievements_manager.py
"""
Sistema de logros/achievements para el juego de mecanografía.
Gestiona el desbloqueo y seguimiento de logros del jugador.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class Achievement:
    """Clase para representar un logro individual."""
    
    def __init__(self, id: str, name: str, description: str, icon_color: Tuple[int, int, int], 
                 condition_func, reward_points: int = 100):
        self.id = id
        self.name = name
        self.description = description
        self.icon_color = icon_color
        self.condition_func = condition_func
        self.reward_points = reward_points
        self.unlocked = False
        self.unlock_date = None
        self.progress = 0.0  # Progreso hacia el logro (0.0 - 1.0)

class AchievementsManager:
    """Gestiona todos los logros del juego."""
    
    def __init__(self):
        self.achievements = {}
        self.total_points = 0
        self.unlocked_count = 0
        
        # Inicializar logros
        self._initialize_achievements()
        
        # Cargar progreso guardado
        self.load_achievements()
    
    def _initialize_achievements(self):
        """Inicializa todos los logros disponibles."""
        
        # Logros de Velocidad (WPM)
        self.achievements["velocista_novato"] = Achievement(
            "velocista_novato", "Velocista Novato", "Alcanza 20 WPM en una sesión",
            (255, 165, 0), lambda stats: stats['wpm'] >= 20, 50
        )
        
        self.achievements["velocista"] = Achievement(
            "velocista", "Velocista", "Alcanza 40 WPM en una sesión",
            (255, 255, 0), lambda stats: stats['wpm'] >= 40, 100
        )
        
        self.achievements["velocista_experto"] = Achievement(
            "velocista_experto", "Velocista Experto", "Alcanza 60 WPM en una sesión",
            (0, 255, 255), lambda stats: stats['wpm'] >= 60, 200
        )
        
        self.achievements["velocista_maestro"] = Achievement(
            "velocista_maestro", "Velocista Maestro", "Alcanza 80 WPM en una sesión",
            (255, 0, 255), lambda stats: stats['wpm'] >= 80, 500
        )
        
        # Logros de Precisión
        self.achievements["perfeccionista"] = Achievement(
            "perfeccionista", "Perfeccionista", "Logra 100% de precisión en una partida completa",
            (0, 255, 0), lambda stats: stats['accuracy'] >= 100 and stats['total_keystrokes'] >= 50, 300
        )
        
        self.achievements["precision_alta"] = Achievement(
            "precision_alta", "Alta Precisión", "Mantén 95% de precisión con más de 100 teclas",
            (100, 255, 100), lambda stats: stats['accuracy'] >= 95 and stats['total_keystrokes'] >= 100, 150
        )
        
        # Logros de Resistencia
        self.achievements["maratonista"] = Achievement(
            "maratonista", "Maratonista", "Juega durante 30 minutos seguidos",
            (255, 100, 100), lambda stats: stats['session_duration'] >= 1800, 250  # 30 minutos
        )
        
        self.achievements["resistencia"] = Achievement(
            "resistencia", "Resistencia", "Juega durante 10 minutos seguidos",
            (255, 150, 150), lambda stats: stats['session_duration'] >= 600, 100  # 10 minutos
        )
        
        # Logros de Racha
        self.achievements["combo_maestro"] = Achievement(
            "combo_maestro", "Maestro del Combo", "Consigue una racha de 50 aciertos seguidos",
            (255, 255, 100), lambda stats: stats['max_streak'] >= 50, 200
        )
        
        self.achievements["combo_experto"] = Achievement(
            "combo_experto", "Experto en Combos", "Consigue una racha de 25 aciertos seguidos",
            (255, 255, 150), lambda stats: stats['max_streak'] >= 25, 100
        )
        
        # Logros de Power-ups
        self.achievements["coleccionista"] = Achievement(
            "coleccionista", "Coleccionista", "Usa todos los tipos de power-ups disponibles",
            (150, 100, 255), self._check_powerup_collector, 150
        )
        
        # Logros de Dedicación
        self.achievements["dedicado"] = Achievement(
            "dedicado", "Jugador Dedicado", "Completa 10 sesiones de juego",
            (100, 150, 255), self._check_session_count, 200
        )
        
        self.achievements["veterano"] = Achievement(
            "veterano", "Veterano", "Completa 50 sesiones de juego",
            (150, 100, 200), lambda stats: self._get_total_sessions() >= 50, 500
        )
        
        # Logros Especiales
        self.achievements["primera_vez"] = Achievement(
            "primera_vez", "Primera Vez", "Completa tu primera partida",
            (255, 255, 255), lambda stats: True, 25
        )
        
        self.achievements["mejorador"] = Achievement(
            "mejorador", "En Constante Mejora", "Mejora tu récord personal de WPM",
            (0, 255, 255), self._check_wpm_improvement, 100
        )
    
    def _check_powerup_collector(self, stats: Dict) -> bool:
        """Verifica si el jugador ha usado todos los power-ups."""
        # Esta función será llamada desde el juego principal
        # Por ahora retorna False, se implementará cuando se integre
        return False
    
    def _check_session_count(self, stats: Dict) -> bool:
        """Verifica el número de sesiones completadas."""
        return self._get_total_sessions() >= 10
    
    def _get_total_sessions(self) -> int:
        """Obtiene el número total de sesiones del archivo de estadísticas."""
        try:
            with open('player_statistics.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return len(data.get('sessions', []))
        except:
            return 0
    
    def _check_wpm_improvement(self, stats: Dict) -> bool:
        """Verifica si el jugador mejoró su récord de WPM."""
        try:
            with open('player_statistics.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                records = data.get('records', {})
                current_best = records.get('best_wpm', 0)
                return stats['wpm'] > current_best
        except:
            return stats['wpm'] > 0  # Primer récord
    
    def check_achievements(self, session_stats: Dict, powerups_used: List[str] = None) -> List[Achievement]:
        """Verifica qué logros se han desbloqueado con las estadísticas actuales."""
        newly_unlocked = []
        
        # Agregar información de power-ups si está disponible
        if powerups_used:
            session_stats['powerups_used'] = powerups_used
        
        for achievement in self.achievements.values():
            if not achievement.unlocked:
                try:
                    # Verificar condición del logro
                    if achievement.condition_func(session_stats):
                        achievement.unlocked = True
                        achievement.unlock_date = datetime.now().isoformat()
                        achievement.progress = 1.0
                        self.unlocked_count += 1
                        self.total_points += achievement.reward_points
                        newly_unlocked.append(achievement)
                except Exception as e:
                    print(f"Error verificando logro {achievement.id}: {e}")
                    continue
        
        # Guardar progreso si hay nuevos logros
        if newly_unlocked:
            self.save_achievements()
        
        return newly_unlocked
    
    def get_achievement_progress(self, achievement_id: str, current_stats: Dict) -> float:
        """Calcula el progreso hacia un logro específico (0.0 - 1.0)."""
        if achievement_id not in self.achievements:
            return 0.0
        
        achievement = self.achievements[achievement_id]
        if achievement.unlocked:
            return 1.0
        
        # Calcular progreso basado en el tipo de logro
        if "velocista" in achievement_id:
            target_wpm = 20 if "novato" in achievement_id else \
                        40 if achievement_id == "velocista" else \
                        60 if "experto" in achievement_id else 80
            return min(current_stats.get('wpm', 0) / target_wpm, 1.0)
        
        elif "precision" in achievement_id or "perfeccionista" in achievement_id:
            target_accuracy = 100 if "perfeccionista" in achievement_id else 95
            current_accuracy = current_stats.get('accuracy', 0)
            return min(current_accuracy / target_accuracy, 1.0)
        
        elif "maratonista" in achievement_id:
            return min(current_stats.get('session_duration', 0) / 1800, 1.0)  # 30 min
        
        elif "resistencia" in achievement_id:
            return min(current_stats.get('session_duration', 0) / 600, 1.0)  # 10 min
        
        elif "combo" in achievement_id:
            target_streak = 50 if "maestro" in achievement_id else 25
            return min(current_stats.get('max_streak', 0) / target_streak, 1.0)
        
        elif "dedicado" in achievement_id:
            return min(self._get_total_sessions() / 10, 1.0)
        
        elif "veterano" in achievement_id:
            return min(self._get_total_sessions() / 50, 1.0)
        
        return 0.0
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        """Obtiene lista de logros desbloqueados."""
        return [ach for ach in self.achievements.values() if ach.unlocked]
    
    def get_locked_achievements(self) -> List[Achievement]:
        """Obtiene lista de logros aún bloqueados."""
        return [ach for ach in self.achievements.values() if not ach.unlocked]
    
    def get_achievement_summary(self) -> Dict:
        """Obtiene resumen de logros."""
        total_achievements = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        
        return {
            'total_achievements': total_achievements,
            'unlocked_count': unlocked,
            'locked_count': total_achievements - unlocked,
            'completion_percentage': round((unlocked / total_achievements) * 100, 1),
            'total_points': self.total_points,
            'recent_unlocks': [ach for ach in self.get_unlocked_achievements() if ach.unlock_date][-5:]
        }
    
    def save_achievements(self):
        """Guarda el progreso de logros a archivo."""
        data = {
            'total_points': self.total_points,
            'unlocked_count': self.unlocked_count,
            'achievements': {}
        }
        
        for ach_id, achievement in self.achievements.items():
            data['achievements'][ach_id] = {
                'unlocked': achievement.unlocked,
                'unlock_date': achievement.unlock_date,
                'progress': achievement.progress
            }
        
        try:
            with open('achievements.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando logros: {e}")
    
    def load_achievements(self):
        """Carga el progreso de logros desde archivo."""
        try:
            with open('achievements.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                self.total_points = data.get('total_points', 0)
                self.unlocked_count = data.get('unlocked_count', 0)
                
                saved_achievements = data.get('achievements', {})
                for ach_id, ach_data in saved_achievements.items():
                    if ach_id in self.achievements:
                        self.achievements[ach_id].unlocked = ach_data.get('unlocked', False)
                        self.achievements[ach_id].unlock_date = ach_data.get('unlock_date')
                        self.achievements[ach_id].progress = ach_data.get('progress', 0.0)
                        
        except (FileNotFoundError, json.JSONDecodeError):
            # Archivo no existe o está corrupto, usar valores por defecto
            pass
    
    def reset_achievements(self):
        """Reinicia todos los logros (para testing o reset completo)."""
        for achievement in self.achievements.values():
            achievement.unlocked = False
            achievement.unlock_date = None
            achievement.progress = 0.0
        
        self.total_points = 0
        self.unlocked_count = 0
        self.save_achievements()
    
    def get_achievement_by_id(self, achievement_id: str) -> Optional[Achievement]:
        """Obtiene un logro específico por su ID."""
        return self.achievements.get(achievement_id)
