import yt_dlp
import os
import subprocess
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
from pathlib import Path

# Función para verificar si FFmpeg está instalado
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# Función para descargar FFmpeg
def download_ffmpeg(progress_var, console_text):
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-i686-static.tar.xz"
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir)

    # Descargar FFmpeg
    response = requests.get(ffmpeg_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(os.path.join(ffmpeg_dir, "ffmpeg.tar.xz"), 'wb') as f:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            downloaded += len(data)
            progress = int(downloaded * 100 / total_size)
            progress_var.set(progress)
            root.after(10, lambda: update_progress_bar(progress_var))  # Actualizar la barra en el hilo principal
            root.update_idletasks()

    # Descomprimir FFmpeg
    subprocess.run(['tar', '-xf', os.path.join(ffmpeg_dir, "ffmpeg.tar.xz"), '-C', ffmpeg_dir])

    # Agregar FFmpeg al PATH
    os.environ['PATH'] += os.pathsep + os.path.join(ffmpeg_dir, 'ffmpeg-*/bin')
    update_console_text(console_text, "FFmpeg descargado y descomprimido.\n")

# Función para descargar música
def download_music(urls, output_dir, progress_bar, progress_var, console_text):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook(progress_bar, progress_var, console_text)],
    }

    for url in urls:
        url = url.strip()
        if url:
            try:
                update_console_text(console_text, f"Descargando: {url}\n")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                messagebox.showerror("Error", f"Error al descargar el video: {e}")
                return

    messagebox.showinfo("Descarga Completa", "¡Todas las descargas se completaron exitosamente!")
    update_console_text(console_text, "Descarga completa.\n")

# Progreso de la descarga
def progress_hook(progress_bar, progress_var, console_text):
    def hook(d):
        if d['status'] == 'downloading':
            progress = int(d['downloaded_bytes'] * 100 / d['total_bytes'])
            progress_var.set(progress)
            root.after(10, lambda: update_progress_bar(progress_var))  # Actualizar la barra en el hilo principal
            update_console_text(console_text, f"Progreso: {progress}%\n")
    return hook

# Función para actualizar el progreso de la barra
def update_progress_bar(progress_var):
    progress_bar['value'] = progress_var.get()
    root.update_idletasks()

# Función para actualizar el texto en la consola
def update_console_text(console_text, message):
    console_text.config(state=tk.NORMAL)  # Hacer que se pueda escribir en el Text
    console_text.insert(tk.END, message)
    console_text.yview(tk.END)  # Desplazar el texto hacia abajo
    console_text.config(state=tk.DISABLED)  # Volver a poner el estado en DISABLED

# Función para iniciar la descarga de música
def start_download(console_text):
    urls_input = url_entry.get("1.0", tk.END)  # Obtener texto desde el widget Text
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Convertir el texto en una lista de URLs
    output_dir = f'musicas/{entry_album.get()}'
    os.makedirs(output_dir, exist_ok=True)

    if not check_ffmpeg():
        update_console_text(console_text, "FFmpeg no encontrado. Descargando...\n")
        download_ffmpeg(progress_var, console_text)
        download_music(urls, output_dir, progress_bar, progress_var, console_text)
    else:
        download_music(urls, output_dir, progress_bar, progress_var, console_text)

# Configuración de la ventana
root = tk.Tk()
root.title("Descargador de Música")

# Estilo de la interfaz
style = ttk.Style()
style.theme_use("alt")  # Usamos un tema más moderno

# Crear widgets
label_album = ttk.Label(root, text="Nombre del álbum:", font=("Arial", 12))
label_album.pack(pady=5)

entry_album = ttk.Entry(root, width=50, font=("Arial", 12))
entry_album.pack(pady=5)

label_urls = ttk.Label(root, text="Introduce las URLs de los videos:", font=("Arial", 12))
label_urls.pack(pady=5)

# Campo de texto para ingresar múltiples URLs
url_entry = tk.Text(root, height=5, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

# Barra de progreso
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400, mode='determinate')
progress_bar.pack(pady=20)

# Consola para mostrar el progreso de la descarga
console_text = tk.Text(root, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED, font=("Courier New", 10))
console_text.pack(pady=10)

# Botón para iniciar la descarga
start_button = ttk.Button(root, text="Iniciar descarga", command=lambda: Thread(target=start_download, args=(console_text,)).start(), style="TButton")
start_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
