import json
import smtplib
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
import os

def jsonFile():
    #Conección a la base de datos: nombreDeUsuario - contraseña - instancia - nombre base de datos
    db_user = os.environ.get('db_user','') #dentro de las comillas va el valor de la variable
    db_password = os.environ.get('db_password','') #dentro de las comillas va el valor de la variable
    db_host = os.environ.get('db_host','') #dentro de las comillas va el valor de la variable
    db_name = os.environ.get('db_name','') #dentro de las comillas va el valor de la variable
    engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
    #Creacion de las columnas de la tabla
    columnas = ['nombreDb', 'emailOwner', 'emailManager', 'confidencialidad','integridad','disponibilidad', 'user_id'] # Crear Columnas
    #Asignacion de los valores
    estructura = {'nombreDb':None,'emailOwner':None,'emailManager':None,'confidencialidad':None,'integridad':None,'disponibilidad':None, 'user_id':None} #Se crean los valores del diccionario
    dataFrame = pd.DataFrame(columns=columnas)
    f=open('./dblist.json','r+') # Se abre el archivo json
    x=json.load((f)) # Guardamos el contenido del json en X

    #Recorrido del json
    for i in x['db_list']:
        estructura['nombreDb']=i['dn_name']
        estructura['emailOwner']=i['owner']['email'] if 'email' in i['owner'] else None
        estructura['confidencialidad']=i['classification']['confidentiality']
        estructura['integridad'] = i['classification']['integrity']
        estructura['disponibilidad'] = i['classification']['availability']
        estructura['user_id'] = i ['owner']['uid']
        dataFrame = dataFrame.append(estructura,ignore_index=True)

    dataExcel = pd.read_excel(io='./user_manager.xlsx',names=['row_id','user_id','user_state','user_manager']) # leemos el excel y se asignan cabeceras a las columnas
    #Se crea un nuevo dataframe donde se van a combinar las columnas del archivo cvs y json
    newData = dataFrame.join(dataExcel.set_index('user_id'),on='user_id')
    #eliminamos las columnas que no se necesitan
    newData= newData.drop(['emailManager','row_id','user_state','user_id'], axis=1)
    #Se crea una conexion a la base de datos nuevamente
    con = psycopg2.connect(f'dbname={db_name} user={db_user} host={db_host} password={db_password}')
    #Creacion del objeto cursor
    cursor = con.cursor()
    #Declaramos query para eliminar contenido de la tabla
    sql = "delete from users;"
    #Ejecucion del query
    cursor.execute(sql)
    #se envia la informacion del dataframe a la base de datos
    r = newData.to_sql('users',con=engine, if_exists='append',index=False)
    #print(r)
    #Se recorre el dataframe
    for i in range(0,len(newData.index)):
        #Si dentro el valor de alguna de las columnas: confidencialidad, integridad o disponibilidad es igual a high se manda un correo
        if newData.iloc[i]['confidencialidad']=='high' or newData.iloc[i]['integridad']=='high' or newData.iloc[i]['disponibilidad']=='high':
            email(newData.iloc[i]['user_manager'])

#funcion para enviar correo
def email(para):
    cuerpo = "Necesitamos su Ok para la clasificacion de la base"
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465) # se levanta el servidor smtp
        server.ehlo() #handshake
        server.login('fernandoMELI98@gmail.com','lkfcwbnxrixhhvbb')
        server.sendmail('fernandoMELI98@gmail.com', para, cuerpo) # se envia el correo
        server.close() # se cierra la conexion
    except Exception as e:
        print(e)

jsonFile()

