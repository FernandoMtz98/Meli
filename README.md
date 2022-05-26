<h1 align="center">
  <br>
    <img src="https://www.python.org/static/img/python-logo@2x.png" alt="SCRIPT FERNANDO MARTÍNEZ SÁNCHEZ" width="400">
  </br>
  <br>
    JJAutomatizer
  <br>
</h1>

# Meli
Script reto mercado libre

## Objetivos

Generar un programa que, a partir de los archivos dados, guarde su contenido en una base de datos y por
cada registro guardado, en donde la clasificación sea alta (high), envíe un email al manager del owner
pidiendo su OK respecto de la clasificación.
Se espera tener una base de datos con la siguiente información almacenada:

            ● nombre de la base de datos
            ● el email del owner
            ● el email del manager
            ● la clasificación de la misma

## Descripción

Se genero el script en el lenguaje de programacion python en su version 3.9, utilizando las siguientes librerias: "PANDAS", "jSON", "SMTPLib", "sqlalchemy" y "psycopg2". Para la creacion de la base de datos se utilizo el sistema de gestion de bases de datos "postgress", para hostear esta base de datos se genero una instancia en la plataforma heroku.

## Compilación del contenedor

    docker build -t maguey_lite .

## Ejecución del contenedor

    docker run --name prueba_appsec maguey_lite SITIO

</details>
<br>

# Jenkins
<details open>
<summary> Cerrar </summary>
<br>

## Descripción

El contenedor de Jenkins lanza una instancia que corre por el puerto 443, este necesita la creación del usuario jenkins con privilegios de root para  ejecutar comandos de Docker sin necesidad de contraseña:

    run - Ejecutar el contendor Maguey
    cp - Copiar archivos de contenedores
    container - Realiza alguna accion especifica con los contenedores, en este caso eliminarlos

Por temas de seguridad se restringirá el uso a las siguientes combinaciones de comandos:

    docker run --name prueba_appsec_* maguey_lite * - Realizar el escaneo automatico
    docker cp prueba_appsec_*:/resultados/ * - Copiar los resultados del escaneo
    docker container prune -f * - Eliminar el contedor usado

Dentro del directorio [Jenkins](Jenkins) existe el archivo Dockerfile para la compilación del contenedor y el archivo jenkins.sh para la creación del contenedor debido a la complejitud del comando.

## Instalación en la nube

Para lograr poder hacer una correcta integración con JIRA es necesario tener un certificado creado por una CA autorizada y por lo tanto un nombre de dominio.

- El nombre de dominio se puede obtener de forma gratuita con [FreeNom](http://www.freenom.world/es/index.html?lang=es).
- Y el certificado con [Let's Encrypt](https://letsencrypt.org/es/)

Una vez asociado el nombre de dominio con la dirección IP (Azure, AWS, Google, etc) será necesario instalar el bot CertBot para la validación del sitio y creación de los certificados SSL/TLS

```bash
# Instalación de CertBot con SNAP
snap install --classic certbot

# Enlace para la ejecución de comandos directamente
ln -s /snap/bin/certbot /usr/bin/certbot

# Creación de los certificados
certbot certonly --standalone --preferred-challenges http -d [DOMINIO]

# Conversión de los certiciados a JKS keystore
cd /etc/letsencrypt/live/www.secappjenkins.ml/
openssl pkcs12 -inkey privkey.pem -in fullchain.pem -export -out keys.pkcs12
keytool -importkeystore -srckeystore keys.pkcs12 -srcstoretype pkcs12 -destkeystore jenkins.jks
mv jenkins.jks /home/usuarioJenkins/certs
```

De esta manera se tendrá un certificado válido.

## Creación del contenedor

    docker build -t jenkins_testing .

## Ejecución del contenedor

```bash
docker run -u 0 -d --name jenkins-appsec \              # Ejecuta la instancia jenkins-appsec como un demonio
    -v /home/usuarioJenkins/certs/:/var/jenkins_home \  # Todos los archivos creados de Jenkins se guardarán de forma local en la máquina local
    -p 443:8443 \                                       # El puerto 8443 de Jenkins saldŕa por el puerto local 443
    -v /var/run/docker.sock:/var/run/docker.sock \      # El socket de la conexión Docker de Jenkins saldrá por el socket local
    -v $(which docker):/usr/bin/docker \                # Los comandos de Docker se ejecutarán de forma local
    jenkins_testing \                                   # Nombre del contenedor a instanciar
    --httpPort=-1 --httpsPort=8443 \                    # Configuración de los puertos 443
    --httpsKeyStore=/var/jenkins_home/jenkins.jks \     # Ruta del certicado de Jenkins que se cambiará
    --httpsKeyStorePassword=appsec                      # Contraseña del certficado
```

O mediante la ejecución del script jenkins.sh

    ./jenkins.sh

</details>
<br>

# JIRA
<details open>
<summary> Cerrar </summary>
<br>

## Descripción

JIRA es un software de seguimiento de proyectos e incidencias enfocado en DevOps, sin embargo, existe la posibilidad de automatizar procesos mediante la integración con Jenkins a la vez de poder monitorear las actividades realizadas. 

## Creación del proyecto

Como la idea principal es automatizar procesos solo será necesario crear un proyecto general, en este caso la plantilla "Gestión de proyectos" funcionará.

</details>
<br>

# Automatización
<details open>
<summary> Cerrar </summary>
<br>

## Descripción

El proceso de automatizar consiste en las llamadas a la API de Jenkins y a la API de JIRA, las cuales ejecutarán los scripts de automatización y darán progreso a los demás procesos.

<div style="text-align:center"><img src="Media/diagrama.svg" /></div>

## Triggers

Los triggers son la parte fundamental del proceso de automatización, para esto es necesario crearlos desde JIRA en la configuración de proyectos.

* Proyecto
    - Configuración del proyecto
        - Automatización
            - Crear regla
<br>
<br>
<div style="text-align:center">
    <img src="Media/automatizacion_1.gif" width="900" height="500" />
</div>

Ejemplo:

Se requiere del issue "Cargar archivo TXT" tenga un archivo para poderlo enviar a otro lado.
<br>
<br>
<div style="text-align:center">
    <img src="Media/automatizacion_2.gif" width="900" height="500" />
</div>

Por lo tanto se necesita de un trigger que se active cuando se agregue un comentario al issue, una vez que valide el archivo realice alguna acción para procesarlo, en este caso solo será necesario transicionar el estado a Finalizado.

* Trigger
    - Incidencia comentada.
* Condición(es)
    - Archivo adjuntos en la incidencia (Si existe).
    - La incidencia coincide con el JQL (issukey = TES-6).
* Acción(es)
    - Realizar la transición de la incidencia a "Finalizada".
<br>
<br>
<div style="text-align:center">
    <img src="Media/automatizacion_3.gif" width="900" height="500" />
</div>

Resultado:
<br>
<br>
<div style="text-align:center">
    <img src="Media/automatizacion_4.gif" width="900" height="500" />
</div>


## Consultas a API / Conectar Jira con Jenkins 

Este proceso es la parte fundamental entre las comunicaciones de JIRA y Jenkins, por lo que es de suma importancia entender como son las peticiones que se envian.

### API JIRA

JIRA Cloud proporciona una guía extensa de cómo usar la [API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/#about) en su respectiva versión.

Para todas consultas será necesario tener el token de autenticación, el cual se consigue en las opciones de seguridad de la cuenta atlassian. Con este token se formará un base64 con el correo electrónico y la credencial:

    ejemplos@ejemplo.com:token

El header quedaría de la siguiente forma:

    Authorization: Basic base64
  
Para lograr conectar Jira con Jenkins, necesitamos seguir los siguientes pasos:
  
  1) Dar clic en el apartado de usuario
  2) Dentro de la nueva vista, dar clic en el apartado "configurar"
  3) En el apartado de "Clave API Token" dé clic en la opción "Add New Token"
  4) Finalmente, introduzca una cadena de texto la cúal pueda identificar fácilmente y dé clic en el botón "Generate"

Dependiendo las consultas que se requieran usar, se solicitará uno o más parámetros, las consultas más solicitas son las siguientes:

    Información del issue (GET)
    https://[dominio]/rest/api/2/issue/[issueKey]

    Transición de estado del issue (POST)
    Parámetros JSON: {"transition":{"id":41}}
    https://[dominio]/rest/api/2/issue/[issueKey]/transitions?expand=transitions.fields

    Obtención de archivos (GET)
    https://[dominio]/secure/attachment/[attachmentKey]/

Estas peticiones pueden ser enviadas con el comando cURL o por Python entre otros.

```bash
curl -D- -u correo:token -X POST --data '{"transition":{"id":41}}' -H "Content-Type: application/json" https://[dominio]/rest/api/2/issue/[issueKey]/transitions?expand=transitions.fields

curl -L -D- -u correo:token  -X GET https://[dominio]/secure/attachment/[attachmentkey]/ --output appsec_sow.png
```
### API Jenkins

Jenkins solamente proporciona información para crear/borrar Jobs y ejecutar Builds, de la misma forma es necesario tener un token de autenticación que se puede conseguir en la configuración del sistema y quedaría de la siguiente forma la crendencial:

    ejemplos@ejemplo.com:token

El header quedaría de la siguiente forma:

    Authorization: Basic base64 

La mayoría de consultas serán de ejecutar Builds con parámetros al Job correspondiente:

    Ejecutar el Job de "Reconocimiento" (POST)
    https://[dominio]/job/Reconocimiento/buildWithParameters/sitio=[sitio]&issueKey=[issueKey]

    Ejecutar el Job de "Obtener SoW" (POST)
    https://[dominio]/job/Reconocimiento/buildWithParameters/issueKey=[issueKey]&attachmentKey=[attachmentKey]

Nota:

* Solicita el método POST pero envía los datos en formato GET ¯\\\_(ツ)_/¯

</details>
<br>

# Ejemplo de integración
<details open>
<summary> Cerrar </summary>
<br>

En este caso se solicita que una vez cargado el SoW con el Vo.Bo se envíe a Jenkins para que pueda recopilarlo, una vez que lo tenga solicita el cambio de estado del issue a Finalizado.

Se crean dos issues, uno que ejecutará las herramientas de automatización y otro que notificará a los consultores para poder iniciar el ejercicio.

## En JIRA

Retomando el ejemplo de automatización con JIRA, sólo se harán modificaciones con respecto a la acción; se agregará un la acción "Webhook" o "Enviar una solicitud Web".

Esta petición tiene como objetivo la URL:

    https://[dominio]/job/Reconocimiento/buildWithParameters/issuekey={{issue.key}}&attachmentkey={{attachment.key}}

    Nota: Van entre doble llave porque son valores Smart y el valor attachment.key debe ser único (para evitar fallos), por lo que en las anteriores condiciones se deben  restringir la cantidad de archivos a obtener.

Se cambia el estado a "En progreso" y se guarda.
<div style="text-align:center">
    <img src="Media/ejemplo_1.png?raw=true" width="900" height="500" />
</div>
## En Jenkins

Se crea un Job llamado "datos sow" con la opción activada "Está opción debe parametrizarse".

Se agregan dos parametros de tipo cadena: issuekey y attachmentkey

```bash
# La petición realiza la transición del issue a finalizado
curl -D- -u correo:token -X POST --data '{"transition":{"id":41}}' -H "Content-Type: application/json" https://andrestest.atlassian.net/rest/api/2/issue/${issuekey}/transitions?expand=transitions.fields

# Obtiene el archivo SoW
curl -L -D- -u correo:token -X GET https://andrestest.atlassian.net/secure/attachment/${attachmentkey}/ --output appsec_sow.png
```

<div style="text-align:center">
    <img src="Media/ejemplo_2.png?raw=true" width="900" height="500" />
    <img src="Media/ejemplo_3.png?raw=true" width="900" height="500" />
</div>


## En JIRA

Se crea un nuevo trigger que se activará cuando pase el estado del issue En progreso a Finalizada.

* Trigger
    - Transición de incidencia realizada (En progreso -> Finalizada)
* Condiciones
    - La incidencia coincide con el JQL (issukey = AS-1)
* Acción
    - Crear nueva incidencia (Lanzar herramientas de reconocimiento)
    - Bifurcar rama (Última incidencia creada)
        - Acción
            - Enviar una petición Web (https://www.secappjenkins.ml/job/Demo-Automatizacion/buildWithParameters?issuekey={{issue.key}}&fields={{issue.description}})
            - Realizar la transición de la incidencia a (En progreso)
    - Crear nueva incidencia (Enviar el Registro de hallazgos a consultores)
    - Bifurcar rama (Última incidencia creada)
        - Acción
            - Enviar correo electrónico (Notificación de inicio de pruebas al aplicativo del cliente X)
            - Realizar la transición de la incidencia a (Finalizada)

<div style="text-align:center">
    <img src="Media/ejemplo_4.png?raw=true" width="900" height="500" />
    <img src="Media/ejemplo_5.png?raw=true" width="900" height="500" />
</div>

## En Jenkins

Se crea un Job llamado "Reconocimiento" con la opción activada "Está opción debe parametrizarse".

Se agregan dos parametros de tipo cadena: issuekey y sitio

```bash
# Cadena aleatoria
aleatoria=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '')

# Eliminacion de contenedores parados
docker container prune -f

# Ejecucion del contenedor Maguey que guarda los archivos en la variable tmp
docker run --name prueba_appsec_$aleatoria maguey_lite ${fields}

# Copiar los archivos generados por las herramientas en el workspace 
docker cp prueba_appsec_$aleatoria:/resultados/ "${WORKSPACE}"

# Eliminacion de los archivos generados en la maquina local
docker container prune -f

# Actualización del Issue
curl -D- -u correo:token -X POST --data '{"transition":{"id":41}}' -H "Content-Type: application/json" https://andrestest.atlassian.net/rest/api/2/issue/${issuekey}/transitions?expand=transitions.fields
```

<div style="text-align:center">
    <img src="Media/ejemplo_6.png?raw=true" width="900" height="500" />
    <img src="Media/ejemplo_7.png?raw=true" width="900" height="500" />
</div>

## PoC

Por último, queda cargar el archivo SoW en el issue y esperar la ejecución de las herramientas.

<br>
<br>
<div style="text-align:center">
    <img src="Media/ejemplo_8.gif" width="900" height="500" />
</div>

</details>
<br>

# Referencias

* [HEROKU]([https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/#about](https://dashboard.heroku.com/))
* [POSTGRESS]([https://www.jenkins.io/doc/book/using/remote-access-api/](https://www.postgresql.org/))
* [https://www.python.org/](https://support.atlassian.com/jira-software-cloud/docs/smart-values-general/)
