import yt_dlp
import os

# URL del video de YouTube que quieres descargar
video_url = 'https://www.youtube.com/watch?v=4VxdufqB9zg'  # Reemplaza con el ID real del video

# Crear la carpeta "musicas" si no existe
output_dir = 'musicas'
os.makedirs(output_dir, exist_ok=True)

# Opciones de descarga
ydl_opts = {
    'format': 'bestaudio/best',  # Mejor calidad de audio
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',  # Usar FFmpeg para extraer el audio
        'preferredcodec': 'mp3',  # Convertir a MP3
        'preferredquality': '192',  # Calidad de audio (en kbps)
    }],
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Almacenar en la carpeta "musicas" con el título del video
}

# Descargar el video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Descarga completa!")
