from google.cloud import pubsub_v1
import moviepy.editor as moviepy
import re
import logging
import json

log = logging.getLogger()

def callback(archivo_json: pubsub_v1.subscriber.message.Message) -> None:
    log.info(f"Received {archivo_json}.")
    archivo_json.ack()
    if archivo_json:
            log.info(f"logging argument {archivo_json}")
        archivo = json.loads(archivo_json)
        log.info(f"dic {archivo}")
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

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("software-en-la-nube-grupo-15", "SuscripcionProcesarVideos")
log.info(f"subscriber: {subscriber}\n")
log.info(f"subscription_path: {subscription_path}\n")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
log.info(f"response pull: {streaming_pull_future}..\n")

#Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:    
        streaming_pull_future.result(timeout=5)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
