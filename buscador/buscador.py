from ytmusicapi import YTMusic
import pandas as pd
import os

ytmusic = YTMusic()
artista_nombre = input("Escribe el nombre exacto del artista: ").strip()

# Buscar ID del artista
search = ytmusic.search(artista_nombre, filter="artists")
if not search:
    print(f"No se encontró el artista '{artista_nombre}'.")
    exit()

artist_id = search[0]['browseId']
artist_info = ytmusic.get_artist(artist_id)

# Recopilar canciones
canciones = []

def agregar_canciones(album, tipo):
    album_id = album['browseId']
    detalles = ytmusic.get_album(album_id)
    for track in detalles['tracks']:
        titulo = track['title']
        artistas = ", ".join([a['name'] for a in track['artists']])
        url = f"https://music.youtube.com/watch?v={track['videoId']}"
        canciones.append({
            "titulo": titulo,
            "artistas": artistas,
            "album": album['title'],
            "url": url
        })

if 'albums' in artist_info:
    for album in artist_info['albums']['results']:
        agregar_canciones(album, "album")

if 'singles' in artist_info:
    for single in artist_info['singles']['results']:
        agregar_canciones(single, "single")

# Crear DataFrame
df = pd.DataFrame(canciones)
print(f"\n🎵 Se encontraron {len(df)} canciones de {artista_nombre}")
print(df.head())

# Preguntar en qué formato guardar
formato = input("\n¿En qué formato quieres guardar el archivo? (csv/txt): ").strip().lower()
nombre_base = f"canciones_{artista_nombre.lower().replace(' ', '_')}"
carpeta = "/home/dnavarrete/Escritorio/descarga-de-mp3/buscador"
ruta = f"{carpeta}/{nombre_base}.{formato}"

# Crear carpeta si no existe
os.makedirs(carpeta, exist_ok=True)

if formato == "csv":
    df.to_csv(ruta, index=False)
    print(f"\n📄 Archivo CSV guardado en: {ruta}")

elif formato == "txt":
    with open(ruta, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"{row['url']}\n")  # SOLO las URLs
    print(f"\n📄 Archivo TXT (solo URLs) guardado en: {ruta}")

else:
    print("\n❌ Formato no válido. Usa 'csv' o 'txt'.")

