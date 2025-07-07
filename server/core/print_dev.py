import os
import inspect
from datetime import datetime
from pathlib import Path

# Colores para consola
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'      # ERROR
    GREEN = '\033[92m'    # INFO
    YELLOW = '\033[93m'   # WARNING
    CYAN = '\033[96m'     # DEBUG

class SimpleLogger:
    
    def __init__(self):
        # Crear carpeta logs dentro de server
        current_dir = Path(__file__).parent.parent  # server/core -> server
        self.log_dir = current_dir / "logs"
        self.log_dir.mkdir(exist_ok=True)
    
    def _write_log(self, level: str, message: str, color: str):
        # Obtener información del origen real (saltando las funciones intermedias)
        frame = inspect.currentframe()
        # Saltar: _write_log -> info/error/etc -> log_info/log_error/etc -> archivo_real
        for _ in range(3):
            frame = frame.f_back
            if frame is None:
                break
        
        # Si no encontramos el frame correcto, usar el último disponible
        if frame is None:
            frame = inspect.currentframe().f_back.f_back
        
        filename = Path(frame.f_code.co_filename).name
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        
        # Crear timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_str = now.strftime("%d_%m_%Y")
        
        # Formatear mensaje
        origin = f"{filename}:{function_name}:{line_number}"
        log_message = f"{timestamp} | {level:<7} | {origin:<30} | {message}"
        
        # Guardar en archivo (siempre)
        log_file = self.log_dir / f"{date_str}_app.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
        
        # Mostrar en consola con color (siempre)
        console_message = f"{color}[{now.strftime('%H:%M:%S')}] {level:<7}{Colors.RESET} | {message}"
        print(console_message)
    
    def debug(self, message: str):
        """Log de debug - color cyan"""
        self._write_log("DEBUG", message, Colors.CYAN)
    
    def info(self, message: str):
        """Log de información - color verde"""
        self._write_log("INFO", message, Colors.GREEN)
    
    def warning(self, message: str):
        """Log de advertencia - color amarillo"""
        self._write_log("WARNING", message, Colors.YELLOW)
    
    def error(self, message: str):
        """Log de error - color rojo"""
        self._write_log("ERROR", message, Colors.RED)

# Instancia global
logger = SimpleLogger()

def is_running_local():
    """Verifica si está ejecutándose en entorno local"""
    return os.environ.get("GAE_ENV") != "standard"

def printer_mensaje(printable):
    """Función de compatibilidad"""
    logger.info(str(printable))

# Funciones simples de logging
def log_debug(message: str):
    """Log nivel DEBUG"""
    logger.debug(message)

def log_info(message: str):
    """Log nivel INFO"""
    logger.info(message)

def log_warning(message: str):
    """Log nivel WARNING"""
    logger.warning(message)

def log_error(message: str):
    """Log nivel ERROR"""
    logger.error(message)
    