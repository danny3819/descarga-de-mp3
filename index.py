import yt_dlp
import os
import sys
import traceback

# Archivo de URLs
urls_file = 'urls.txt'  # Cambia si usas otro archivo

# Validar argumento de carpeta de salida
if len(sys.argv) < 2:
    print("Uso: python index.py <nombre_de_carpeta>")
    sys.exit(1)

output_dir = f'musicas/{sys.argv[1]}'
os.makedirs(output_dir, exist_ok=True)

# Opciones para yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(output_dir, '%(playlist_title)s/%(title)s.%(ext)s'),
    'ignoreerrors': True,  # Esto ayuda, pero no es suficiente en todos los casos
    'quiet': False,
    'no_warnings': True,
    'ratelimit': None,  # Elimina el límite de velocidad si está configurado
    'throttled_rate_limit': None,  # Evita la espera extra entre descargas
}

# Leer URLs desde archivo
with open(urls_file, 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

for url in urls:
    print(f"\n🔽 Descargando: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"❌ Error al descargar {url}: {e}")
        traceback.print_exc()  # Opcional: muestra detalles del error
        continue

print("\n✅ Descargas completas!")

