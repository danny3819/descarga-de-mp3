import yt_dlp
import os

# Ruta del archivo de texto que contiene las URLs
urls_file = 'urls.txt'  # Cambia esto al nombre de tu archivo de texto

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
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Almacenar en la carpeta "musicas"
}

# Leer las URLs desde el archivo de texto
with open(urls_file, 'r') as file:
    urls = file.readlines()

# Descargar cada video
for url in urls:
    url = url.strip()  # Eliminar espacios en blanco y saltos de línea
    if url:  # Verificar que la URL no esté vacía
        print(f"Descargando: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

print("Descargas completas!")
