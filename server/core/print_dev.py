import os

def is_running_local():
    """
    Verifica si la solución se está ejecutando en el entorno local.

    Returns:
        bool: True si se está ejecutando en local, False si se está ejecutando en producción.
    """
    return os.environ.get("GAE_ENV") != "standard"

def printer_mensaje(printable):
    if is_running_local():
        print(printable)
    