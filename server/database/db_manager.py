import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Video, Thread , Request, Author
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

def create_connection():
    engine = create_engine(os.getenv("POSTGRES_URL"), echo=False)
    return engine
def open_session():
    engine = create_connection()
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    print("Creating tables...")
    engine = create_connection()
    Base.metadata.drop_all(engine)  # Eliminar tablas existentes (opcional)
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

def insert_new_video(session,data,now):
            # Crear nuevo video si no existe
        video = Video(
            youtube_video_id=data["video_id"],
            video_url=data["video_url"],
            title=data["title"],
            description=data["description"],
            author=data["author"],
            total_threads=data["total_threads"],
            updated_at=now
        )
        session.add(video)  # Agregar a sesión para que tenga ID
        session.flush()  # Para asegurar que video.id esté disponible
        return video

def update_video(video,data,now):
        # Actualizar campos existentes
        video.video_url = data["video_url"]
        video.title = data["title"]
        video.description = data["description"]
        video.author = data["author"]
        video.total_threads = data["total_threads"]
        video.updated_at = now  # O usa updated_at si tienes

def insert_video_from_scrapper(data):
    print("📽 Processing video request ...")
    session = open_session()
    now = datetime.now()

    # Search by youtube_video_id
    video = session.query(Video).filter_by(youtube_video_id=data["video_id"]).first()

    if video is None:
        video = insert_new_video(session, data, now)
    else:
        update_video(video, data, now)

    # Crear nueva Request vinculada al video
    request = Request(
        fk_video_id=video.id,
        request_date=now
    )
    session.add(request)
    session.flush()  # To ensure request.id is available


    # Insertar nuevos threads con referencia a Request y Author
    for thread_data in data.get("threads", []):
        author_name = thread_data["author"]

        # Buscar autor en DB
        author = session.query(Author).filter_by(name=author_name).first()
        if author is None:
            # Crear nuevo autor si no existe
            author = Author(name=author_name)
            session.add(author)
            session.flush()  # Para tener author.id

        thread = Thread(
            fk_video_id=video.id,
            fk_request_id=request.id,
            fk_author_id=author.id,  # Asignar fk_author_id
            comment=thread_data["comment"],
            inserted_at=now
        )
        session.add(thread)

    session.commit()
    session.close()

    print("💾 Data for current Request succesfully inserted/updated.")


def main():
    parser = argparse.ArgumentParser(description="Database manager script")
    parser.add_argument("--file", type=str, help="Ruta del archivo JSON", default="scrap.json")
    parser.add_argument("--recreate", action="store_true", help="Eliminar y recrear tablas")

    args = parser.parse_args()

    if args.recreate:
        create_tables()

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    insert_video_from_scrapper(data)

if __name__ == "__main__":
    main()