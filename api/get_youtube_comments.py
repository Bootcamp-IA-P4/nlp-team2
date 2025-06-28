from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import pandas as pd

# 🔐 Coloca tu API key aquí:
API_KEY = "TU_API_KEY_AQUI" 

# Construye el cliente de la API
youtube = build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url):
    """Extrae el ID del video de una URL completa"""
    try:
        query = urlparse(url).query
        return parse_qs(query)["v"][0]
    except Exception:
        raise ValueError("❌ URL no válida. Usa una como: https://www.youtube.com/watch?v=XXXXXXXXXXX")

def get_top_comments(video_id, max_comments=20):
    """Obtiene los primeros comentarios (top-level) del video"""
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=min(max_comments, 100)  # máximo permitido por la API es 100
    )
    response = request.execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments[:max_comments]

if __name__ == "__main__":
    try:
        url = input("🔗 Pega la URL del video de YouTube: ")
        video_id = extract_video_id(url)
        print(f"🎥 ID del video: {video_id}")

        print("🧪 Obteniendo los primeros comentarios...")
        comments = get_top_comments(video_id, max_comments=20)

        if comments:
            df = pd.DataFrame(comments, columns=["comment"])
            df.to_csv("youtube_comments_lite.csv", index=False)
            print(f"✅ {len(comments)} comentarios guardados en 'youtube_comments_lite.csv'")
        else:
            print("⚠️ No se encontraron comentarios.")

    except Exception as e:
        print(f"💥 Error: {e}")
