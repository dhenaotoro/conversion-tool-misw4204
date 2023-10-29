from celery import Celery, Task
from datetime import datetime as dt, timedelta
from modelos import db, Archivo, ArchivoSchema
from sqlalchemy import create_engine, orm
import moviepy.editor as moviepy
import re
import logging

log = logging.getLogger()
celery_app = Celery(__name__, broker='redis://redis-server:6379/0')

celery_app.conf.update(
    result_expires=3600,
    enable_utc = False,
    timezone = 'America/Bogota'
)

celery_app.conf.beat_schedule = {
    "convertir_archivos-task": {
        "task": "tareas.convertir_archivos",
        "schedule": timedelta(minutes=2)
    }
}

class M_DBTask(type):
    pass

class DBTask(Task):
    __metaclass__=M_DBTask
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()

    @property
    def database(self):
        if self._session is None:
            engine = create_engine("postgresql://postgres:postgres@db:5432/conversion_tool")
            Session = orm.sessionmaker(engine) 
            self._session = Session()
        return self._session 

@celery_app.task(base=DBTask, bind=True)
def convertir_archivos(self: Task):
    for archivo_desde_bd in self.database.query(Archivo).filter_by(estado='uploaded').all():
        archivo = ArchivoSchema().dump(archivo_desde_bd)
        log.info(f"logging argument {archivo}")
        tiempo_actual = dt.now()
        fecha_hora_actual = tiempo_actual.strftime("%Y-%m-%d %H:%M:%S")
        log.info(f"Inicio del batch {fecha_hora_actual} para procesar el evento {archivo}")

        log.info(f"Archivo {archivo['nombreArchivo']} leido identificado con id {archivo['id']}")
        nombre_archivo_sin_extension = re.sub(r'.(mp4|webm|avi)', '', archivo['nombreArchivo'])
        nombre_archivo_completo = re.sub(r'.*\w\/', '', nombre_archivo_sin_extension)
        
        try:
            clip = moviepy.VideoFileClip(archivo['nombreArchivo'])
            log.info(f"El formato destino es {archivo['nuevoFormato']}")
            url_archivo_destino = f"./videos/destino/{nombre_archivo_completo}.{archivo['nuevoFormato']}"
            if archivo['nuevoFormato'] == 'webm' or archivo['nuevoFormato'] == 'mp4':
                clip.write_videofile(url_archivo_destino)
                log.info(f"El archivo fue procesado correctamente y quedó depositado en la ruta ./videos/destino/{nombre_archivo_completo}.{archivo['nuevoFormato']}")
            elif archivo['nuevoFormato']  == 'avi':
                clip.write_videofile(url_archivo_destino, codec='rawvideo')
                log.info(f"El archivo fue procesado correctamente y quedó depositado en la ruta ./videos/destino/{nombre_archivo_completo}.{archivo['nuevoFormato']}")
            else:
                log.info(f"El batch no está preparado para procesar el formato {archivo['nuevoFormato'] }")
            archivo_info = self.database.query(Archivo).get(archivo['id'])
            log.info(f'archivo id consultado {archivo_info.id}')
            archivo_info.urlArchivo = url_archivo_destino
            archivo_info.estado = 'processed'
            self.database.commit()
        except Exception as e:
            log.info(f"Ocurrió un error al leer el archivo {str(e)}")

        #self.after_return()
