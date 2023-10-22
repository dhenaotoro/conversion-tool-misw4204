# Aplicación conversion-tool-misw4204
## Descripción
La aplicación permite la conversión entre videos de formatos mp4, webm y avi. Actualmente no soporta conversión entre formatos mpeg y wmv.

A continuación se enuncian dos apartados para explicar como desplegar la aplicación en su máquina y como usar la aplicación (después de estar desplegada) por medio de una API expuesta en PostMan de manera pública.

## Pasos para ejecutar los contenedores que despliegan la aplicación conversion-tool.

1. Asegurarse que la aplicación Docker Desktop está instalada y ejecutada en su computador sea Mac o Windows. Ver el siguiente enlace para instalar Docker Desktop en ambas plataformas:

 - Windows: ToDo incluir enlace.
 - Linux o Mac: ToDo incluir enlace.

2. Abrir una consola de comandos y descargar del repositorio los fuentes de la aplicación conversion-tool.

- Opción https:
```bash
git clone https://github.com/dhenaotoro/conversion-tool-misw4204
```
- Opción ssh:
```bash
git clone git@github.com:dhenaotoro/conversion-tool-misw4204.git
```

3. Luego de estar en el directorio principal, por favor ejecutar los comandos necesarios para instalar las dependencias del proyecto:

- Asegurarse que tiene instalado python igual o mayor a la versión 3.8 en su máquina, en caso de que no, descargarlo desde [aquí](https://www.python.org/downloads/)

- Posteriormente, se debe crear un ambiente virtual usando los siguientes comandos:
```bash
py -m venv virtualenv
venv virtualenv
```

- Luego se debe activar el ambiente virtual usando el siguiente comando:

Para windows:
```bash
.\virtualenv\Scripts\activate.bat
```

Para Linux o Mac
```bash
./virtualenv/bin/activate
```

- Finalmente, se debe ejecutar el comando para instalar las depedencias:
```bash
pip install -r requirements.txt
```

4. Luego de haber instalado las dependencias de la aplicación, por favor ejecutar el siguiente comando para levantar la aplicación conversion-tool con todos los contenedores necesarios.

```bash
docker-compose up
```

Nota: Es importante que se aseguren que los puertos 5432, 6378 y 8000 estén disponibles en su máquina con el fin de que el proceso de despliegue se realice exitosamente.

Nota: Tener presente que el comando `docker-compose up` toma el control de la consola de comandos y no te dejará ejecutar algún otro comando adicional, en caso de necesitarlo por favor abrir otra instancia de consola de comandos y ubicarse nuevamente en el directorio donde se encuentran los archivos fuentes de la aplicación.

5.  Verificar que en la aplicación Docker Desktop se encuentra un contenedor agrupador que contiene los contenedores listados a continuación:

- Un contenedor relacionado con el broker-message (Plataforma de colas) llamado `redis-server`.
- Un contenedor relacionado con la api de la aplicación `convertion-tool-api`.
- Un contenedor relacionado con la gestión de tareas que leen mensajes de colas disponibles `worker`.
- Un contenedor relacionado con la base de datos llamado `db`.

Nota: Todos los contenedores deben estar en color verde incluyendo el contenedor agrupador.

## Pasos para usar la aplicación.

1. Descargar la colección y ambiente de Postman desde [aquí]()

2. Crear un usuario en la aplicación usando el endpoint denominado `Crear cuenta de usuario`.

3. Hace login usando el usuario creado y su contraseña por medio del endpoint denominado `Recuperar Token`, con el fin de generar el token que a su vez permite autenticar el usuario ante los demás endpoints relacionados con la gestión de la conversión de videos.

4. Ubicar el video que se desea convertir en la ruta `.\videos\origen` (para windows) `./videos/origen` (para linux o mac).

Nota: Tener presente que el video debe estar en formato `mp4`, `webm` o `avi`. Actualmente no se soportan formatos `mpeg` y `wmv`.

5. Ejecutar el endpoint denominado `Crear tarea de conversion` para guardar el video en la base de datos. Aquí debemos especificar la ruta del video y el formato que se desea convertir.

Nota: la aplicación tiene una tarea asincrona que se encarga de revisar cada minuto (Desde el momento en que se desplegó toda la aplicación) si existen videos por convertir, en caso de que si, se convierten y se actualiza en la base de datos el estado del video `processed`.

6. [Opcional] Ejecutar el endpoint denominado `Recuperar tareas de conversion` para verificar el estado de los videos que estén registrados en la base de datos.

7. [Opcional] Ejecutar el endpoint denominado `Recuperar tarea` para verificar el estado de un video en especial, donde se deben enviar el id del video.

8. [Opcional] Ejecutar el endpoint denominado `Eliminar tarea` para eliminar un video de la base de datos en caso de que no se desee convertir.
