#!/bin/bash

# Directorio donde están los archivos .webm (puedes cambiarlo si es necesario)
DIRECTORIO="videos/cumbias"  # Cambia esto si tu carpeta está en otra ruta

# Iterar sobre todos los archivos .webm en el directorio
for archivo in "$DIRECTORIO"/*.webm; do
    # Si el archivo .webm existe
    if [ -f "$archivo" ]; then
        # Obtener el nombre del archivo sin la extensión
        nombre_sin_extension="${archivo%.webm}"
        
        # Convertir el archivo .webm a .mp4 sin recodificar (solo cambiar el contenedor)
        ffmpeg -i "$archivo" -c copy "$nombre_sin_extension.mp4"
        
        # Verificar si la conversión fue exitosa
        if [ $? -eq 0 ]; then
            echo "Conversión exitosa: $archivo -> $nombre_sin_extension.mp4"
            
            # Eliminar el archivo .webm después de la conversión
            rm "$archivo"
            echo "Archivo $archivo eliminado."
        else
            echo "Error en la conversión de $archivo"
        fi
    fi
done

echo "¡Proceso completado!"

