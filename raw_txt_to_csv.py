import datetime
from pandas import DataFrame

#Abrimos el archivo txt con los servidores C2 y sus Jarm
a_file = open("C2.txt", "r")

#Creamos una lista vacia
list_of_lists = []
#Guardamos cada linea del archivo txt como una lista en la lista list_of_lists (lista de listas)
for line in a_file:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  list_of_lists.append(line_list)

a_file.close()

#Encontramos la primera aparicion del string |, para llegar a la tabla donde estan los datos útiles
#posicion guarda la fila del archivo C2.txt en la que se comienza a leer la tabla
i=0
while i<=len(list_of_lists):
  if list_of_lists[i]!=[]:
    if list_of_lists[i][0]=="|":
      posicion=i
      i=27
    else:
      i=i+1
  else:
    i=i+1

#texto equivale a list_of_lists anterior, pero solo guardando en cada lista los valores de cada fila de la tabla (ya no hay nada del texto original de introduccion)
texto=[]
for i in range(posicion,len(list_of_lists)):
  texto.append(list_of_lists[i])

#convertimos a strings de texto cada lista, así solo tenemos una lista de strings
csv=[]
for i in texto:
  listToStr = ' '.join(map(str, i)) 
  csv.append(listToStr)

#hacemos un split para separar los campos relevantes que en la tabla estaban delimitados por el string |
#generamos nuevamente una lista de listas, similar a la encontrada en texto, pero con los campos bien separados e identificados y sin el caracter |
csv2=[]
for i in csv:
  csv2.append(i.split('|'))

#generamos nuevamente una lista, aunque ahora eliminamos los campos vacios ""
csv3=[]
for i in csv2:
  csv3.append(i[1:len(i)-1])

#eliminamos las 2 primeras listas (o filas de la tabla), ya que una son los headers mal hechos y otra son puros caracteres separadores -----
csv3=csv3[2:len(csv3)]

#eliminamos los espacios de los strings, para que se puedan comparar bien con el fingerprint de los dominios
#p =" Hola "
#y = p.replace(" ","") -> "Hola"
for i in range(0,len(csv3)):
  for j in range(0,len(csv3[i])):
    csv3[i][j] = csv3[i][j].replace(' ','')

#Lo convertimos en un df

df = DataFrame(csv3,columns=['C2/Red Team Tool','SSL Implementation Tested','Jarm C2','Link'])
fecha = datetime.datetime.now()
df["Fecha C2"]=fecha 

#Descargamos el df
df.to_csv('Servidores_C2.csv',index=False) #index se puede dejar como false para mantenerlos o quitar para que salga sin los header