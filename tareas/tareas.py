from celery import Celery

from modelos import db, Archivo

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task()
def ejecutar_conversion(id_tarea, fecha):
    tareas = Archivo.query.filter_by(estado='uploaded').all()
    for tarea in tareas:
        with open(tarea.nombreArchivo) as archivo:
            archivo_leido = archivo.read()
            #Conversion
            #Guardar