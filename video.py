import os
import subprocess
import sys

# Obtener el nombre de la carpeta desde el argumento
if len(sys.argv) < 2:
    print("Error: Se debe proporcionar el nombre de la carpeta para guardar los videos.")
    sys.exit(1)

# Carpeta donde se guardarán los videos descargados (se obtiene del argumento)
directorio = sys.argv[1]
ruta_guardado = f"videos/{directorio}"

# Asegurarnos de que el directorio exista
os.makedirs(ruta_guardado, exist_ok=True)

# Archivo de texto donde están las URLs de los videos
archivo_urls = "urls.txt"

# Leer las URLs desde el archivo
try:
    with open(archivo_urls, 'r') as file:
        urls = file.readlines()
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_urls}.")
    exit(1)

# Descargar cada video usando yt-dlp
for url in urls:
    url = url.strip()

    if not url:
        continue

    comando = [
        "yt-dlp",
        "-f", "bv*+ba/b",  # Mejor combinación de video+audio
        "-o", os.path.join(ruta_guardado, "%(title)s.%(ext)s"),
        url
    ]

    try:
        subprocess.run(comando, check=True)
        print(f"✅ Descarga exitosa: {url}")
    except subprocess.CalledProcessError:
        print(f"❌ Error al descargar el video: {url}")

print("🎉 ¡Proceso de descarga completado!")

