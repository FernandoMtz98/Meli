<h1 align="center">
  <br>
    <img src="https://www.python.org/static/img/python-logo@2x.png" alt="script" width="400" img src="https://brand.heroku.com/static/media/heroku-logotype-horizontal.81c49462.svg alt="heroku" width="400">
  </br>
  <br>
    SCRIPT FERNANDO MARTÍNEZ SÁNCHEZ
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

## Ejecución del script desde terminal

    python3 script.py
<br>
<div style="text-align:center">
    <img src="Media/imagen1.PNG" width="900" height="500" />
</div>
</br>
# Referencias

* [HEROKU]([https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/#about](https://dashboard.heroku.com/))
* [POSTGRESS]([https://www.jenkins.io/doc/book/using/remote-access-api/](https://www.postgresql.org/))
* [https://www.python.org/](https://support.atlassian.com/jira-software-cloud/docs/smart-values-general/)
