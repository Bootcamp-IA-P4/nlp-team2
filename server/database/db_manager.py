import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Video, Thread  
from dotenv import load_dotenv
import os

load_dotenv()

# 2. Conexión a PostgreSQL
engine = create_engine(os.getenv("POSTGRES_URL"), echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# 3. Crear tablas si no existen
#Base.metadata.drop_all(engine)  # Eliminar tablas existentes (opcional)
Base.metadata.drop_all(engine)  # Eliminar tablas existentes (opcional)
Base.metadata.create_all(engine)

# 4. Insertar vídeo
def insert_video_from_scrapper(data):

    now = datetime.now()
    video = Video(
        youtube_video_id=data["video_id"],
        video_url=data["video_url"],
        title=data["title"],
        description=data["description"],
        author=data["author"],
        total_threads=data["total_threads"],
        inserted_at=now
    )

    # 5. Insertar comentarios como threads
    for thread_data in data["threads"]:
        thread = Thread(
            author=thread_data["author"],
            comment=thread_data["comment"],
            inserted_at=now
        )
        video.comments.append(thread)

# 6. Guardar en la base de datos
    session.add(video)
    session.commit()
    session.close()


with open("scrap.json", "r", encoding="utf-8") as f:
    data = json.load(f)
insert_video_from_scrapper(data)