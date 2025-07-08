import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, Session
from .models import Base, Video, Thread , Request, Author, RequestThread, ToxicityAnalysis, VideoToxicitySummary
from dotenv import load_dotenv
import os
import argparse

try:
    load_dotenv()
except Exception as e:
    print(f"Error loading .env file: {e}")

def create_connection():
    try:
        engine = create_engine(os.getenv("POSTGRES_URL"), echo=False)
    except Exception as e:
        raise Exception(f"Error creating database connection: {e}")
    return engine
def open_session():
    try:
        engine = create_connection()
        Session = sessionmaker(bind=engine)
    except Exception as e:
        raise Exception(f"Error opening database session: {e}")
    return Session()

def create_tables():
    print("Creating tables...")
    try:
        engine = create_connection()
        Base.metadata.drop_all(engine)  # Eliminar tablas existentes (opcional)
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except Exception as e:
        raise Exception(f"Error creating tables: {e}")

def insert_new_video(session,data,now):
        try:
            author_name = data["author"]
            author = session.query(Author).filter_by(name=author_name).first()
            if author is None:
                author = Author(name=author_name)
                session.add(author)
                session.flush()
        # Crear nuevo video si no existe
            video = Video(
            youtube_video_id=data["video_id"],
            video_url=data["video_url"],
            title=data["title"],
            description=data["description"],
            fk_author_id=author.id,
            total_threads=data["total_threads"],
            updated_at=now,
            total_likes=data.get("total_likes"),
            total_comments=data.get("total_comments"),
            emoji_stats=data.get("emoji_stats"),
            total_emojis=data.get("total_emojis"),
            most_common_emojis=data.get("most_common_emojis")
        )

            session.add(video)  # Agregar a sesión para que tenga ID
            session.flush()  # Para asegurar que video.id esté disponible
        except Exception as e:
            raise Exception(f"Error inserting new video: {e}")
        return video

def update_video(session, video, data, now):
        author_name = data["author"]
        author = session.query(Author).filter_by(name=author_name).first()
        if author is None:
            author = Author(name=author_name)
            session.add(author)
            session.flush()
        try:
            # Actualizar campos existentes
            video.video_url = data["video_url"]
            video.title = data["title"]
            video.description = data["description"]
            video.fk_author_id = author.id
            video.total_threads = data["total_threads"]
            video.updated_at = now
            video.total_likes = data.get("total_likes")
            video.total_comments = data.get("total_comments")
            video.emoji_stats = data.get("emoji_stats")
            video.total_emojis = data.get("total_emojis")
            video.most_common_emojis = data.get("most_common_emojis")
        except Exception as e:
            raise Exception(f"Error updating video: {e}")

def create_thread(session, video, request, thread_data, now, parent_comment_id=None):
    author_name = thread_data["author"]

    # Buscar o crear autor
    author = session.query(Author).filter_by(name=author_name).first()
    if author is None:
        author = Author(name=author_name)
        session.add(author)
        session.flush()

    thread = Thread(
        fk_video_id=video.id,
        fk_author_id=author.id,
        parent_comment_id=parent_comment_id,
        comment=thread_data.get("comment"),
        likes=thread_data.get("likes", 0),
        published_time=thread_data.get("published_time"),
        emoji_count=thread_data.get("emoji_count", 0),
        emojis=thread_data.get("emojis", []),
        has_replies=thread_data.get("has_replies", False),
        replies_count=thread_data.get("replies_count", 0)
    )

    session.add(thread)
    session.flush()  # Necesario para obtener el ID

    # **NEW: Create the request-thread relationship**
    request_thread = RequestThread(
        fk_request_id=request.id,
        fk_thread_id=thread.id
    )
    session.add(request_thread)
    
    return thread

def insert_threads(session, video, request, threads_data, now):
    try:
        created_threads = []  # Track created threads
        
        for thread_data in threads_data:
            # Insertar comentario principal
            parent_thread = create_thread(
                session=session,
                video=video,
                request=request,
                thread_data=thread_data,
                now=now,
                parent_comment_id=None
            )
            created_threads.append(parent_thread)

            # Insertar replies (si existen)
            if thread_data.get("has_replies") and thread_data.get("replies"):
                for reply_data in thread_data["replies"]:
                    reply_thread = create_thread(
                        session=session,
                        video=video,
                        request=request,
                        thread_data=reply_data,
                        now=now,
                        parent_comment_id=parent_thread.id
                    )
                    created_threads.append(reply_thread)
        
        return created_threads
    except Exception as e:
        raise Exception(f"Error inserting threads: {e}")

def insert_video_from_scrapper(data):
    try:
        print("📽 Processing video request ...")
        session = open_session()
        now = datetime.now()

        # Search by youtube_video_id
        video = session.query(Video).filter_by(youtube_video_id=data["video_id"]).first()

        if video is None:
            video = insert_new_video(session, data, now)
        else:
            update_video(session, video, data, now)
    
        # Crear nueva Request vinculada al video
        request = Request(
            fk_video_id=video.id,
            request_date=now
        )
        session.add(request)
        session.flush()  # To ensure request.id is available


        insert_threads(session, video, request, data.get("threads", []), now)

        session.commit()
        session.close()


        print("💾 Data for current Request succesfully inserted/updated.")
    except Exception as e:
        raise Exception(f"Error processing video request: {e}")
    
def get_request_list():
    try:
        session = open_session()
        #requests = session.query(Request).join(Video, Request.fk_video_id == Video.id).all()
        requests = session.query(Request).options(joinedload(Request.video)).all()
        session.close()
        return requests
    except Exception as e:
        raise Exception(f"Error retrieving request list: {e}")
    
def get_request_by_id(request_id):
    try:
        session = open_session()
        request =  session.query(Request).options(joinedload(Request.video)).filter(Request.id == request_id).first()
        session.close()
        return request
    except Exception as e:
        raise Exception(f"Error retrieving request by ID: {e}")

def create_request_thread_relationships(session, request, threads):
    """
    Create RequestThread relationships for existing threads
    Useful for batch operations or migrations
    """
    try:
        for thread in threads:
            # Check if relationship already exists
            existing = session.query(RequestThread).filter_by(
                fk_request_id=request.id,
                fk_thread_id=thread.id
            ).first()
            
            if not existing:
                request_thread = RequestThread(
                    fk_request_id=request.id,
                    fk_thread_id=thread.id
                )
                session.add(request_thread)
        
        session.flush()
    except Exception as e:
        raise Exception(f"Error creating request-thread relationships: {e}")

def get_threads_by_request(request_id):
    """
    Get all threads associated with a specific request
    """
    try:
        session = open_session()
        threads = session.query(Thread).join(
            RequestThread, Thread.id == RequestThread.fk_thread_id
        ).filter(
            RequestThread.fk_request_id == request_id
        ).all()
        session.close()
        return threads
    except Exception as e:
        raise Exception(f"Error retrieving threads by request: {e}")

def get_requests_by_thread(thread_id):
    """
    Get all requests that include a specific thread
    """
    try:
        session = open_session()
        requests = session.query(Request).join(
            RequestThread, Request.id == RequestThread.fk_request_id
        ).filter(
            RequestThread.fk_thread_id == thread_id
        ).all()
        session.close()
        return requests
    except Exception as e:
        raise Exception(f"Error retrieving requests by thread: {e}")

def get_request_with_threads(request_id):
    """
    Get a request with all its associated threads
    """
    try:
        session = open_session()
        request = session.query(Request).options(
            joinedload(Request.video)
        ).filter(Request.id == request_id).first()
        
        if request:
            # Get associated threads
            threads = session.query(Thread).join(
                RequestThread, Thread.id == RequestThread.fk_thread_id
            ).filter(
                RequestThread.fk_request_id == request_id
            ).options(
                joinedload(Thread.author_obj)
            ).all()
            
            # Add threads to request object (not persisted, just for convenience)
            request.associated_threads = threads
        
        session.close()
        return request
    except Exception as e:
        raise Exception(f"Error retrieving request with threads: {e}")


def insert_toxicity_analysis(
    session: Session,
    fk_thread_id: int,
    fk_request_id: int,
    is_toxic: bool,
    toxicity_confidence: float,
    categories_detected: dict,
    category_scores: dict,
    model_version: str = "1.0.0",
    analyzed_at: datetime = None
):
    analysis = ToxicityAnalysis(
        fk_thread_id=fk_thread_id,
        fk_request_id=fk_request_id,
        is_toxic=is_toxic,
        toxicity_confidence=toxicity_confidence,
        categories_detected=categories_detected,
        category_scores=category_scores,
        model_version=model_version,
        analyzed_at=analyzed_at or datetime.utcnow()
    )
    session.add(analysis)
    session.commit()
    return analysis

def insert_video_toxicity_summary(
    session: Session,
    fk_video_id: int,
    fk_request_id: int,
    total_comments: int,
    toxic_comments: int,
    toxicity_rate: float,
    categories_summary: dict,
    most_toxic_thread_id: int = None,
    average_toxicity: float = None,
    model_info: dict = None,
    analysis_completed_at: datetime = None
):
    summary = VideoToxicitySummary(
        fk_video_id=fk_video_id,
        fk_request_id=fk_request_id,
        total_comments=total_comments,
        toxic_comments=toxic_comments,
        toxicity_rate=toxicity_rate,
        categories_summary=categories_summary,
        most_toxic_thread_id=most_toxic_thread_id,
        average_toxicity=average_toxicity,
        model_info=model_info or {},
        analysis_completed_at=analysis_completed_at or datetime.utcnow()
    )
    session.add(summary)
    session.commit()
    return summary


def main():
    try:
        parser = argparse.ArgumentParser(description="Database manager script")
        parser.add_argument("--file", type=str, help="Ruta del archivo JSON", default="scrap.json")
        parser.add_argument("--recreate", action="store_true", help="Eliminar y recrear tablas")
        args = parser.parse_args()

        if args.recreate:
            create_tables()
            exit()
    
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)

        insert_video_from_scrapper(data)
    except Exception as e:
        raise Exception(f"Error in db_manager main function: {e}")
if __name__ == "__main__":
    main()

    

