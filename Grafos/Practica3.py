#Autor: Pablo Menéndez Ruiz de Azúa
#Asignatura: Algoritmica GITT
#Profesor: Atilano Fernández

import matplotlib.pyplot as plt
import networkx as nx 
import numpy as np
import pandas as pd

def comprobacion(filas,columnas,etiquetas):
    cero=list(np.zeros(len(filas[1])))
    nodos=list(filas.keys())
    fuente=0
    cont_fuente=0
    cont_sumidero=0
    sumidero=0
    
    #Comprobamos que solo hay una fuente y un sumidero
    for i in filas:
        if filas[i]==cero:
            sumidero=i
            cont_sumidero+=1
    for i in columnas:
        if columnas[i]==cero:
            fuente=i
            cont_fuente+=1
    if cont_sumidero!= 1 or cont_fuente!=1:
        return False
    
    #Comprobamos que desde la fuente se puede llegar a todos los nodos y desde todos los nodos se puede llegar al sumidero
    for i in nodos:
        if i != fuente:
            desde_fuente=encontrar_camino(etiquetas,fuente,i)
            if desde_fuente == []:
                return False
        if i != sumidero:
            hasta_sumidero=encontrar_camino(etiquetas,i,sumidero)
            if hasta_sumidero == []:
                return False
    return fuente,sumidero


#Función para dibujar la red de aumento
def dibujar_grafo(etiquetas,tabla):
    plt.figure(figsize=(7,5))
    G=nx.DiGraph()
    G.add_node(0)
    G.add_nodes_from(list(tabla.keys()))
    conexiones=list(etiquetas.keys())
    for i in range(len(etiquetas)):
        G.add_edges_from([conexiones[i]],weight=etiquetas[conexiones[i]][0])

    pos=nx.circular_layout(G)
    nx.draw_networkx(G,pos,with_labels=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=etiquetas)
    plt.title("Red [Capacidad, flujo]")
    plt.show()
    
#Función para el camino de aumento
def camino_aumento(camino,delta,tabla):
    plt.figure(figsize=(7,5))
    G=nx.DiGraph()
    G.add_node(0)
    G.add_nodes_from(list(tabla.keys()))
    etiquetas={}
    for i in camino:
        G.add_edges_from([i],weight=delta)
        etiquetas[i]=delta
    pos=nx.circular_layout(G)
    nx.draw_networkx(G,pos,with_labels=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=etiquetas)
    plt.title("camino de aumento")
    plt.show()

    

#Función para dibujar la red residual
def residual(etiquetas,tabla):
    plt.figure(figsize=(7,5))
    G=nx.DiGraph()
    G.add_node(0)
    G.add_nodes_from(list(tabla.keys()))
    conexiones=list(etiquetas.keys())
    long= len(etiquetas)
    new_etiq={}
    
    for i in range(long):
        cap=etiquetas[conexiones[i]][0]
        fluj=etiquetas[conexiones[i]][1]
        new_etiq[conexiones[i]]=cap-fluj
        if new_etiq[conexiones[i]]==0:
            del new_etiq[conexiones[i]]
        
    conexiones=list(new_etiq.keys())
    for i in range(len(new_etiq)):
        G.add_edges_from([conexiones[i]],weight=new_etiq[conexiones[i]])

    pos=nx.circular_layout(G)
    nx.draw_networkx(G,pos,with_labels=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=new_etiq)
    plt.title("Red residual")
    plt.show()
    

#FordFulkerson

#Función para encontrar un camino entre nodos posible
def extraer_camino(camino,prohibido,etiquetas):
    conexiones=list(etiquetas.keys())
    capacidad=[]
    flujo=[]

    for [u,v] in etiquetas.values():
        capacidad.append(u)
        flujo.append(v)
    
    for i in range(len(conexiones)):
        (u,v)=conexiones[i]
        if u == camino[-1] and capacidad[i] > flujo [i] and v not in camino and v not in prohibido:
            camino.append(v)
            break

#Función para encontrar un camino por el que pueda ir el flujo
def encontrar_camino (etiquetas,origen,final):
    camino = [origen]
    prohibido=[origen] #Esta variable es para cuando has pasado ya por un nodo del que no podía salir flujo, se guarda aquí 
                       #para que no vuelvas a pasar por él
    camino_tuplas = []
               
    #Mientras que el último nodo del camino no sea el final seguimos iterando
    while camino[-1]!=final:
        camino_ant=camino[:] #Copiamos el camino a otra variable para poder compararlas más tarde
        extraer_camino(camino,prohibido,etiquetas)

        if camino_ant == camino:#Si el camino antes y después de la función es el mismo quiere decir que no ha encontrado un camino  
                                #válido, por lo que hay que retroceder un nodo para ver si por otro camino puede seguir el flujo
            if camino == [origen]: # Si ha retrocedido tanto que ha vuelto a la fuente, y desde la fuente no hay caminos es 
                                   #porque ya no puede salir más flujo
                break
            else:
                prohibido.append(camino[-1])
                camino.pop(-1)
    
    if camino[-1] == final:
        for i in range(len(camino)-1):
            tupla=(camino[i],camino[i+1])
            camino_tuplas.append(tupla)

    else:
        camino_tuplas=[]
   
    
    return camino_tuplas


#Leemos el excel con los datos
df=pd.read_excel("fordfulkerson.xlsx")

#Extraemos los datos en forma de diccionario
filas={}
columnas={}
for i in range(6):
    fil=df.iloc[i]
    col=df[i]
    filas[i]=[]
    columnas[i]=[]
    for j in range(len(fil)-1):
        filas[i].append(fil[j])
        columnas[i].append(col[j])

#Inicializamos nuestras variables: conexiones, capacidad y flujo_tubería
capacidad=[]
conexiones=[]
for i in range(len(filas)):
    for j in range(len(filas[i])):
        if filas[i][j]!=0:
            tupla=(i,j)
            capacidad.append(filas[i][j])
            conexiones.append(tupla)

flujo_tuberia = list(np.zeros(len(capacidad)))

#Agrupamos nuestras tres variables en un diccionario llamado etiquetas para que nos sea más fácil acceder a él
etiquetas={}
for i in range(len(conexiones)):
    valor= [capacidad[i],int(flujo_tuberia[i])]
    etiquetas[conexiones[i]]=valor
#El diccionario etiquetas será de la forma (nodo1,nodo2): [Capacidad, flujo]

if comprobacion(filas,columnas,etiquetas) == False:
    print("No se puede aplicar el algorítmo de FordFulkenson porque la matriz no es una red de transportes")

#Realizamos nuestro programa aplicando el algoritmo de fordfulkenson utilizando dos funciones para encontrar el camino 
#y para dibujar.
else:
    #Inicializamos
    fuente,sumidero=comprobacion(filas,columnas,etiquetas)
    flujo_total = 0
    contador=1
    #Buscamos el primer camino
    camino = encontrar_camino(etiquetas,fuente,sumidero)
    
    #Pintamos el grafo origen
    print("Grafo origen: ")
    dibujar_grafo(etiquetas,filas)

    #Hasta que no se pueda llevar más flujo de la fuente al sumidero seguimos buscando caminos
    while camino != []:
        print("Camino"+str(contador)+": ",camino)
        
        #Buscamos el flujo que va a ir por el camino (delta)
        cap=[]
        for i in camino:
            cap.append(etiquetas[i][0]-etiquetas[i][1])
        delta=min(cap)
        flujo_total +=delta
        print("flujo del camino: ", delta)
        print("flujo total: ",flujo_total)
        
        #A los arcos por los que pasa el camino, les sumamos el flujo que pasa
        for i in camino:
            etiquetas[i][1]+=delta
        
        #Dibujamos nuestros tres gráficos (el camino, la red residual y la red de aumento)
        camino_aumento(camino,delta,filas)
        residual(etiquetas,filas)
        dibujar_grafo(etiquetas,filas)
        
        #Buscamos un camino nuevo entre la fuente y el sumidero
        camino=encontrar_camino(etiquetas,fuente,sumidero)
        contador += 1
    print("El flujo final es", flujo_total)  
      