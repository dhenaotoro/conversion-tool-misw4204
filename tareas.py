from celery import Celery
from datetime import datetime as dt
from modelos import db, Archivo
import moviepy.editor as moviepy
import re

celery_app = Celery(__name__, broker='redis://redis-server:6379/0')

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print(f"Executing period task")
    sender.add_periodic_task(10.0, convertir_archivos.s(), name='Llama cada 10 segundos')

@celery_app.task
def convertir_archivos(archivo):
    tiempo_actual = dt.now()
    fecha_hora_actual = tiempo_actual.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Inicio del batch {fecha_hora_actual} para procesar el evento {archivo}")

    print(f"Archivo {archivo['nombreArchivo']} leido identificado con id {archivo['id']}")
    nombre_archivo_sin_extension = re.sub(r'.(mp4|webm|avi)', '', archivo['nombreArchivo'])
    nombre_archivo_completo = re.sub(r'.*\w\/', '', nombre_archivo_sin_extension)
    
    try:
        clip = moviepy.VideoFileClip(archivo['nombreArchivo'])
        print(f"El formato destino es {archivo['nuevoFormato']}")
        url_archivo_destino = f"./videos/destino/{nombre_archivo_completo}.{archivo['nuevoFormato']}"
        if archivo['nuevoFormato'] == 'webm' or archivo['nuevoFormato'] == 'mp4':
            clip.write_videofile(url_archivo_destino)
            print(f"El archivo fue procesado correctamente y quedó depositado en la ruta ./videos/destino/{nombre_archivo_completo}.{archivo['nuevoFormato']}")
        elif archivo['nuevoFormato']  == 'avi':
            clip.write_videofile(url_archivo_destino, codec='rawvideo')
            print(f"El archivo fue procesado correctamente y quedó depositado en la ruta ./videos/destino/{nombre_archivo_completo}.{archivo['nuevoFormato']}")
        else:
            print(f"El batch no está preparado para procesar el formato {archivo['nuevoFormato'] }")
        archivo_info = Archivo.query.get_or_404(archivo['id'])
        print(archivo_info.id)
        archivo_info.urlArchivo = url_archivo_destino
        db.session.commit()
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo {str(e)}")
