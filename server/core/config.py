from dotenv import load_dotenv
import os

load_dotenv()
class Setting:
    def __init__(self):
        self.title = "Modzilla"
        self.version = "v1"
        self.description = "API para la moderación de comentarios de YouTube"
        self.authors = ["Fernando Garcia Catalan", "Juan Carlos Macias", "Alejandro Rajado Martin", "Vada Velazquez"]
        self.model = os.getenv("MODEL_BASE_URL")
        self.metrics = os.getenv("METRICS_BASE_URL")
setting = Setting()