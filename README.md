# Aplicación conversion-tool-misw4204
## Descripción
La aplicación permite la conversión entre videos de formatos mp4, webm y avi. Actualmente no soporta conversión entre formatos mpeg y wmv.

A continuación se enuncian dos apartados para explicar como desplegar la aplicación en su máquina y como usar la aplicación (después de estar desplegada) por medio de una API expuesta en PostMan de manera pública.

## Pasos para ejecutar los contenedores que despliegan la aplicación conversion-tool.

1. Asegurarse que la aplicación Docker Desktop está instalada y ejecutada en su computador sea Mac o Windows. Ver el siguiente [enlace](https://jpadillaa.hashnode.dev/docker-instalacion-de-docker) para instalar Docker Desktop en ambas plataformas.
2. Abrir una consola de comandos y descargar del repositorio los fuentes de la aplicación conversion-tool.

- Opción https:
```bash
git clone https://github.com/dhenaotoro/conversion-tool-misw4204
cd conversion-tool-misw4204
```
- Opción ssh:
```bash
git clone git@github.com:dhenaotoro/conversion-tool-misw4204.git
cd conversion-tool-misw4204
```
- Opción Github Cli:
```bash
gh repo clone dhenaotoro/conversion-tool-misw4204
cd conversion-tool-misw4204
```

3. Ubicar los videos que se desean convertir en la ruta `.\videos\origen` (para windows) `./videos/origen` (para linux o mac).

Nota: Tener presente que el video debe estar en formato `mp4`, `webm` o `avi`. Actualmente no se soportan formatos `mpeg` y `wmv`.

4. Una vez realizados los pasos anteriores, por favor ejecutar el siguiente comando para levantar la aplicación conversion-tool con todos los contenedores necesarios.

Nota: Si se desea agregar o renombrar un archivo adicional para conversión después de desplegar el docker, se recomienda realizar el docker build para que la aplicación cargue el archivo nuevo o renombrado.

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

1. Descargar la colección y ambiente de Postman desde [aquí](https://github.com/dhenaotoro/conversion-tool-misw4204/files/13064891/OneDrive_2_22-10-2023.zip), una vez descargado se descomprime y se importa en postman.

2. Crear un usuario en la aplicación usando el endpoint denominado `Crear cuenta de usuario`.

3. Hacer login usando el usuario creado y su contraseña por medio del endpoint denominado `Recuperar Token`, con el fin de generar el token que a su vez permite autenticar el usuario ante los demás endpoints relacionados con la gestión de la conversión de videos.

Nota: En caso de que el token expire, por favor ejecutar nuevamente este paso y continuar ejecutando el endpoint que falló por token expirado.

4. Ejecutar el endpoint denominado `Crear tarea de conversion` para guardar el video en la base de datos. Aquí debemos especificar la ruta del video y el formato que se desea convertir.

Nota 1: la aplicación tiene una tarea asincrona que se encarga de revisar cada minuto (Desde el momento en que se desplegó toda la aplicación) si existen videos por convertir, en caso de que si, se convierten y se actualiza en la base de datos el estado del video `processed`.

Nota 2: Es importante tener en cuenta que los videos se tienen que almacenar en el directorio `./videos/origen` antes de hacer el despliegue de la aplicación para que se puedan procesar.

5. [Opcional] Ejecutar el endpoint denominado `Recuperar tareas de conversion` para verificar el estado de los videos que estén registrados en la base de datos.

6. [Opcional] Ejecutar el endpoint denominado `Recuperar tarea` para verificar el estado de un video en especial, donde se deben enviar el id del video.

7. [Opcional] Ejecutar el endpoint denominado `Eliminar tarea` para eliminar un video de la base de datos en caso de que no se desee convertir.

## Pasos para ver el video destino

1. Ingresar a Docker Desktop.
2. Buscar el contenedor denominado `conversion-tool-misw4204_worker_#` donde el caracter # puede corresponder a un número (dependiendo de cómo Docker Desktop lo muestre).
3. Ingresar a una terminal del contenedor denominado `conversion-tool-misw4204_worker_#`.
4. Dentro de la terminal ejecutar el siguiente comando:
`ls -ltha ./videos/destino/`

Nota: En ese directorio deben aparecer los videos que fueron procesados.
