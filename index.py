import yt_dlp
import os
import sys

# Archivo de URLs
urls_file = 'urls.txt'  # Cambia si usas otro archivo

# Validar argumento de carpeta de salida
if len(sys.argv) < 2:
    print("Uso: python index.py <nombre_de_carpeta>")
    sys.exit(1)

output_dir = f'musicas/{sys.argv[1]}'
os.makedirs(output_dir, exist_ok=True)

ydl_opts = {
    'format': 'bestaudio/best',
    'cookiesfrombrowser': ('chrome',),  # Usar cookies de navegador para autenticación
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(output_dir, '%(playlist_title)s/%(title)s.%(ext)s'),  # Carpeta por playlist, si aplica
    # 'noplaylist': False por defecto, dejamos que descargue listas si la URL es una playlist
    'ignoreerrors': True,  # Continúa con siguientes URLs si hay error
}

with open(urls_file, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

for url in urls:
    print(f"Descargando: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        continue

print("Descargas completas!")

