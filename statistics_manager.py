# statistics_manager.py
"""
Sistema avanzado de estadísticas para el juego de mecanografía.
Calcula WPM, precisión, tiempo de reacción y otras métricas en tiempo real.
"""

import time
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class StatisticsManager:
    """Gestiona todas las estadísticas del juego."""
    
    def __init__(self):
        self.session_start_time = time.time()
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.incorrect_keystrokes = 0
        self.keystroke_times = []  # Para calcular tiempo de reacción
        self.wpm_history = []  # Historial de WPM por minuto
        self.last_wpm_update = time.time()
        self.current_streak = 0
        self.max_streak = 0
        self.letters_per_second = []
        
        # Estadísticas por tecla
        self.key_stats = {}  # {tecla: {'correct': int, 'incorrect': int, 'reaction_times': []}}
        
        # Cargar estadísticas históricas
        self.historical_stats = self.load_historical_stats()
    
    def record_keystroke(self, key: str, is_correct: bool, reaction_time: float = 0.0):
        """Registra una pulsación de tecla con sus métricas."""
        current_time = time.time()
        
        # Estadísticas generales
        self.total_keystrokes += 1
        if is_correct:
            self.correct_keystrokes += 1
            self.current_streak += 1
            self.max_streak = max(self.max_streak, self.current_streak)
        else:
            self.incorrect_keystrokes += 1
            self.current_streak = 0
        
        # Tiempo de reacción
        if reaction_time > 0:
            self.keystroke_times.append(reaction_time)
        
        # Estadísticas por tecla
        if key not in self.key_stats:
            self.key_stats[key] = {'correct': 0, 'incorrect': 0, 'reaction_times': []}
        
        if is_correct:
            self.key_stats[key]['correct'] += 1
        else:
            self.key_stats[key]['incorrect'] += 1
        
        if reaction_time > 0:
            self.key_stats[key]['reaction_times'].append(reaction_time)
        
        # Actualizar WPM cada minuto
        if current_time - self.last_wpm_update >= 60.0:
            self.update_wpm_history()
    
    def get_current_wpm(self) -> float:
        """Calcula el WPM actual basado en los últimos 60 segundos."""
        current_time = time.time()
        session_duration = current_time - self.session_start_time
        
        if session_duration < 1.0:  # Evitar división por cero
            return 0.0
        
        # WPM = (caracteres correctos / 5) / (tiempo en minutos)
        # Usamos 5 como promedio de caracteres por palabra
        words_typed = self.correct_keystrokes / 5.0
        minutes_elapsed = session_duration / 60.0
        
        return round(words_typed / minutes_elapsed, 1) if minutes_elapsed > 0 else 0.0
    
    def get_accuracy(self) -> float:
        """Calcula la precisión actual."""
        if self.total_keystrokes == 0:
            return 100.0
        return round((self.correct_keystrokes / self.total_keystrokes) * 100, 1)
    
    def get_average_reaction_time(self) -> float:
        """Calcula el tiempo de reacción promedio."""
        if not self.keystroke_times:
            return 0.0
        return round(sum(self.keystroke_times) / len(self.keystroke_times), 3)
    
    def get_session_duration(self) -> float:
        """Obtiene la duración de la sesión actual en segundos."""
        return time.time() - self.session_start_time
    
    def get_detailed_stats(self) -> Dict:
        """Obtiene estadísticas detalladas de la sesión actual."""
        return {
            'wpm': self.get_current_wpm(),
            'accuracy': self.get_accuracy(),
            'total_keystrokes': self.total_keystrokes,
            'correct_keystrokes': self.correct_keystrokes,
            'incorrect_keystrokes': self.incorrect_keystrokes,
            'current_streak': self.current_streak,
            'max_streak': self.max_streak,
            'average_reaction_time': self.get_average_reaction_time(),
            'session_duration': self.get_session_duration(),
            'key_stats': self.key_stats.copy()
        }
    
    def update_wpm_history(self):
        """Actualiza el historial de WPM."""
        current_wpm = self.get_current_wpm()
        self.wpm_history.append({
            'timestamp': time.time(),
            'wpm': current_wpm,
            'accuracy': self.get_accuracy()
        })
        self.last_wpm_update = time.time()
    
    def get_performance_grade(self) -> Tuple[str, str]:
        """Obtiene una calificación de rendimiento basada en WPM y precisión."""
        wpm = self.get_current_wpm()
        accuracy = self.get_accuracy()
        
        # Calificación basada en WPM
        if wpm >= 80:
            wpm_grade = "Experto"
            color = (0, 255, 0)  # Verde
        elif wpm >= 60:
            wmp_grade = "Avanzado"
            color = (0, 255, 255)  # Cian
        elif wpm >= 40:
            wpm_grade = "Intermedio"
            color = (255, 255, 0)  # Amarillo
        elif wpm >= 20:
            wpm_grade = "Principiante"
            color = (255, 165, 0)  # Naranja
        else:
            wpm_grade = "Novato"
            color = (255, 0, 0)  # Rojo
        
        # Ajustar por precisión
        if accuracy < 85:
            wpm_grade += " (Mejorar precisión)"
        elif accuracy >= 98:
            wmp_grade += " (Excelente precisión)"
        
        return wmp_grade, color
    
    def save_session_stats(self, game_mode: str, final_score: int):
        """Guarda las estadísticas de la sesión completada."""
        session_stats = self.get_detailed_stats()
        session_stats.update({
            'timestamp': datetime.now().isoformat(),
            'game_mode': game_mode,
            'final_score': final_score,
            'session_id': int(time.time())
        })
        
        # Agregar a estadísticas históricas
        if 'sessions' not in self.historical_stats:
            self.historical_stats['sessions'] = []
        
        self.historical_stats['sessions'].append(session_stats)
        
        # Mantener solo las últimas 100 sesiones
        if len(self.historical_stats['sessions']) > 100:
            self.historical_stats['sessions'] = self.historical_stats['sessions'][-100:]
        
        # Actualizar récords personales
        self.update_personal_records(session_stats)
        
        # Guardar a archivo
        self.save_historical_stats()
    
    def update_personal_records(self, session_stats: Dict):
        """Actualiza los récords personales."""
        records = self.historical_stats.get('records', {})
        
        # Récord de WPM
        if session_stats['wpm'] > records.get('best_wpm', 0):
            records['best_wpm'] = session_stats['wpm']
            records['best_wpm_date'] = session_stats['timestamp']
        
        # Récord de precisión
        if session_stats['accuracy'] > records.get('best_accuracy', 0):
            records['best_accuracy'] = session_stats['accuracy']
            records['best_accuracy_date'] = session_stats['timestamp']
        
        # Récord de racha
        if session_stats['max_streak'] > records.get('best_streak', 0):
            records['best_streak'] = session_stats['max_streak']
            records['best_streak_date'] = session_stats['timestamp']
        
        # Sesión más larga
        if session_stats['session_duration'] > records.get('longest_session', 0):
            records['longest_session'] = session_stats['session_duration']
            records['longest_session_date'] = session_stats['timestamp']
        
        self.historical_stats['records'] = records
    
    def load_historical_stats(self) -> Dict:
        """Carga estadísticas históricas desde archivo."""
        try:
            with open('player_statistics.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'sessions': [], 'records': {}}
    
    def save_historical_stats(self):
        """Guarda estadísticas históricas a archivo."""
        try:
            with open('player_statistics.json', 'w', encoding='utf-8') as f:
                json.dump(self.historical_stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")
    
    def get_historical_summary(self) -> Dict:
        """Obtiene un resumen de estadísticas históricas."""
        sessions = self.historical_stats.get('sessions', [])
        records = self.historical_stats.get('records', {})
        
        if not sessions:
            return {'total_sessions': 0, 'records': records}
        
        # Calcular promedios
        total_wpm = sum(s['wpm'] for s in sessions)
        total_accuracy = sum(s['accuracy'] for s in sessions)
        total_time = sum(s['session_duration'] for s in sessions)
        
        return {
            'total_sessions': len(sessions),
            'average_wpm': round(total_wpm / len(sessions), 1),
            'average_accuracy': round(total_accuracy / len(sessions), 1),
            'total_playtime': total_time,
            'records': records,
            'recent_sessions': sessions[-10:]  # Últimas 10 sesiones
        }
    
    def reset_session(self):
        """Reinicia las estadísticas de la sesión actual."""
        self.session_start_time = time.time()
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.incorrect_keystrokes = 0
        self.keystroke_times = []
        self.wpm_history = []
        self.last_wpm_update = time.time()
        self.current_streak = 0
        self.key_stats = {}
        self.letters_per_second = []
