import pandas as pd
import operator
import datetime

#Se crea el dataframe a partir del csv
df=pd.read_csv("resultado_jarm.csv")

#Se añaden los headers de las columnas al csv
df.columns=["Dominio","IP","Jarm","TLS 1","TLS 2","TLS 3","TLS 4","TLS 5","TLS 6","TLS 7","TLS 8","TLS 9","TLS 10"]

#Filtramos los dominios que tienen fingerprint 0 o bien no se pudo hacer conexion
sinconexion = str(str(0)*62)
df2 = df[df["IP"] != "Failed to resolve IP"] 
df_dominios = df2[df2["Jarm"] != str(sinconexion)]

#Eliminamos las columnas de los saludos TLS que no nos importan/aportan nada 
df_dominios = df_dominios.drop(["TLS 1","TLS 2","TLS 3","TLS 4","TLS 5","TLS 6","TLS 7","TLS 8","TLS 9","TLS 10"], axis=1)

#Se crea el dataframe de las botnets conocidas a partir del csv
df_C2=pd.read_csv("Servidores_C2.csv")

#Se crea el inner join entre ambos dataframes
inner_join = pd.merge(left=df_dominios,right=df_C2, left_on='Jarm', right_on='Jarm C2')

#Se agrega el campo de fecha
fecha = datetime.datetime.now()
inner_join["Fecha"]=fecha 

#Se elimina el campo repetido del Jarm
resultado_final = inner_join.drop(["Jarm C2"], axis=1)

#df.to_csv(r'Path where you want to store the exported CSV file\File Name.csv')
#df_output.to_csv(r'C:\Users\gonza\Desktop\Botnets_red_chilena.csv') seria en caso de no estar corriendo en colab
resultado_final.to_csv('Botnets_red_chilena.csv',index=False) #index se puede dejar como false para mantenerlos o quitar para que salga sin los header
