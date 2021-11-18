#Autor: Pablo Menéndez Ruiz de Azúa
#Asignatura: Algoritmica GITT
#Profesor: Atilano Fernández

class Nodo():
    def __init__(self,value):
        self.clave=value
        self.color=1 #1-rojo 0-negro
        self.padre=None
        self.izq=None
        self.dcha=None

class Arbol():
    def __init__(self):
        self.raiz=None
        
    def Insertar(self,num):
        x=Nodo(num)
        self.InsertArbolBin(x)
        while (x!=self.raiz and x.padre.color==1): #Si el color del padre es negro no pasa nada
            if (x.padre==x.padre.padre.izq):
                y=x.padre.padre.dcha
                #Problema cuando no hay tío
                if y == None:
                    if x==x.padre.dcha:
                        x=x.padre
                        self.RotarIzqArbolBin(x)
                    x.padre.color=0
                    x.padre.padre.color=1
                    self.RotarDchaArbolBin(x.padre.padre)
                else:
                    if (y.color==1):
                        y.color=0
                        x.padre.color=0
                        x.padre.padre.color=1
                        x=x.padre.padre
                    else:
                        if x==x.padre.dcha:
                            x=x.padre
                            self.RotarIzqArbolBin(x)
                        x.padre.color=0
                        x.padre.padre.color=1
                        self.RotarDchaArbolBin(x.padre.padre)
            else:
                y=x.padre.padre.izq
                if y == None:
                    if x==x.padre.izq:
                        x=x.padre
                        self.RotarDchaArbolBin(x)
                    x.padre.color=0
                    x.padre.padre.color=1
                    self.RotarIzqArbolBin(x.padre.padre)
                else:
                    if (y.color==1):
                        y.color=0
                        x.padre.color=0
                        x.padre.padre.color=1
                        x=x.padre.padre
                    else:
                        if x==x.padre.izq:
                            x=x.padre
                            self.RotarDchaArbolBin(x)
                        x.padre.color=0
                        x.padre.padre.color=1
                        self.RotarIzqArbolBin(x.padre.padre)
        self.raiz.color=0
                    

    def InsertArbolBin(self,nodo_insertar):
        p=None
        x=self.raiz
        while x!=None:
            p=x
            if nodo_insertar.clave < x.clave:
                x=x.izq
            else:
                x=x.dcha

        nodo_insertar.padre=p
        
        if p==None:
            self.raiz=nodo_insertar
        else:
            if nodo_insertar.clave < p.clave:
                p.izq=nodo_insertar
            elif nodo_insertar.clave > p.clave:
                p.dcha=nodo_insertar

    def RotarIzqArbolBin(self,x):
        y=x.dcha
        x.dcha=y.izq
        if y.izq !=None:
            y.izq.padre=x
        y.padre=x.padre
        if x.padre==None:
            self.raiz=y
        elif x==x.padre.izq:
            x.padre.izq=y
        else:
            x.padre.dcha=y
        y.izq=x
        x.padre=y
    
    def RotarDchaArbolBin(self,x):
        y=x.izq
        x.izq=y.dcha
        if y.dcha!=None:
            y.dcha.padre=x
        y.padre=x.padre
        if x.padre==None:
            self.raiz=y
        elif x==x.padre.izq:
            x.padre.izq=y
        else:
            x.padre.dcha=y
        y.dcha=x
        x.padre=y
        
    def Buscar(self,num):
        x=self.raiz
        while x!= None:
            if x.clave==num:
                return x
            else:
                if x.clave > num:
                    x=x.izq
                else:
                    x=x.dcha
        return False
    
    def Eliminar(self,num):
        if self.Buscar(num)==False: #Comprobamos que el número se encuentra en el árbol
            print("\nEl nodo que quieres borrar no se encuentra en el árbol")
            return False
        else:
            n=self.Buscar(num)
        if n.izq==None or n.dcha==None: 
            y=n
        else: #Cuando tenga nodos a izq y dcha se busca el sucesor que va a ser el más a la izquierda de los que están 
              #a la derecha del nodo a borrar
            y=n.dcha
            while y.izq!=None:
                y=y.izq
        if y.izq!=None: #Si tiene hijos y, se crea una nueva variable que sea el nodo a unir, si no tiene guarda None
            x=y.izq
        else:
            x=y.dcha
        if x!=None:
            x.padre=y.padre
        if y.padre==None:
            self.raiz=x
        else: #Actualiza el hijo del padre de y
            if y==y.padre.izq:
                y.padre.izq=x
            else:
                y.padre.dcha=x
        if y!=n:
            n.clave=y.clave
        if y.color==0 :
            self.EliminarRN(x,y)
    
    def EliminarRN(self,x,y):#x es el hijo del nodo que hemos borrado
        color_x=0
        if x!=None:
            if x.color==1:
                x_color=1
        while x!=self.raiz and color_x==0:
            if x==None: #Si en la primera iteración x es nulo
                padre=y.padre
            else: padre=x.padre   
            if x==padre.izq:
                w=padre.dcha #hermano de x
                color_w=0
                color_w_izq=0
                color_w_dcha=0
                if w!=None:
                    if w.color==1:
                        color_w=1
                    if w.izq!=None:
                        if w.izq.color==1:
                            color_w_izq=1
                    if w.dcha!=None:
                        if w.dcha.color==1:
                            color_w_dcha=1
                if color_w==1:
                    w.color=0
                    padre.color=1
                    self.RotarIzqArbolBin(padre)
                    w=padre.dcha #nuevo w, objetivo es conseguir un hermano negro para x
                    if w!=None:
                        if w.color==1:
                            color_w=1
                        if w.izq!=None:
                            if w.izq.color==1:
                                color_w_izq=1
                        if w.dcha!=None:
                            if w.dcha.color==1:
                                color_w_dcha=1
                if color_w_izq==0 and color_w_dcha==0:
                    # Si el hermano de x y sus hijos son negros (o nulos), se sube un negro al padre y se le quita a los hijos (la x tiene doble negro)
                    # Se repite el bucle con el padre
                    if w!=None:
                        w.color=1
                    x=padre
                else:
                    if color_w_dcha==0:
                        #Si w y su hijo derecho son negros pero el izquierdo no, cambiamos el color de w y del izquierdo y rotamos hacia la derecha
                        w.izq.color=0
                        w.color=1
                        self.RotarDchaArbolBin(w)
                        w=padre.dcha
                    w.color=padre.color
                    padre.color=0
                    w.dcha.color=0
                    self.RotarIzqArbolBin(padre)
                    x=self.raiz
            else:
                w=padre.izq #hermano de x
                color_w=0
                color_w_izq=0
                color_w_dcha=0
                if w!=None:
                    if w.color==1:
                        color_w=1
                    if w.izq!=None:
                        if w.izq.color==1:
                            color_w_izq=1
                    if w.dcha!=None:
                        if w.dcha.color==1:
                            color_w_dcha=1
                if color_w==1:
                    w.color=0
                    padre.color=1
                    self.RotarDchaArbolBin(x.padre)
                    w=padre.izq #nuevo w, objetivo es conseguir un hermano negro para x
                    if w!=None:
                        if w.color==1:
                            color_w=1
                        if w.izq!=None:
                            if w.izq.color==1:
                                color_w_izq=1
                        if w.dcha!=None:
                            if w.dcha.color==1:
                                color_w_dcha=1
                if color_w_izq==0 and color_w_dcha==0:
                    print("Hola")
                    # Si el hermano de x y sus hijos son negros (o nulos), se sube un negro al padre y se le quita a los hijos (la x tiene doble negro)
                    # Se repite el bucle con el padre
                    if w!=None:
                        w.color=1
                    x=padre
                else:
                    if color_w_izq==0:
                        #Si w y su hijo izquierdo son negros pero el derecho no, cambiamos el color de w y del izquierdo y rotamos hacia la derecha
                        w.dcha.color=0
                        w.color=1
                        self.RotarIzqArbolBin(w)
                        w=padre.izq
                    w.color=padre.color
                    padre.color=0
                    w.izq.color=0
                    self.RotarDchaArbolBin(padre)
                    x=self.raiz
                    
        if x!=None:
            x.color=0            
            

    def Recorrer(self,lista):
        x=self.raiz
        if x!=None:
            lista.append(x.clave)
            HijoIzquierdo=Arbol()
            HijoDerecho=Arbol()
            HijoIzquierdo.raiz=x.izq
            HijoDerecho.raiz=x.dcha
            HijoIzquierdo.Recorrer(lista)
            print(x.clave)
            HijoDerecho.Recorrer(lista)
            
        
#Mostrar el árbol
def Imprimir(arbol,cont=-1):
    cont+=1
    if arbol.raiz!=None:
        color="(R)"
        x=arbol.raiz
        if x.color==0:
            color="(N)"
        print(cont*"\t"+str(x.clave)+color)
        HijoIzquierdo=Arbol()
        HijoDerecho=Arbol()
        HijoIzquierdo.raiz=x.izq
        HijoDerecho.raiz=x.dcha
        #print(cont*"\t",end="")
        Imprimir(HijoIzquierdo,cont)
        Imprimir(HijoDerecho,cont)
        

    
#Programa principal
import string
def Opciones():
    print("\n")
    print("Opciones: ")
    print("- 1. Insertar un elemento en el árbol")
    print("- 2. Eliminar un elemento del árbol")
    print("- 3. Buscar un elemento en el árbol")
    print("- 4. Mostrar el árbol")
    print("- 5. Listar los elementos del árbol de forma ordenada")
    print("- 6. Eliminar el árbol")
    print("- 7. Cargar árbol desde fichero")
    print("- 8. Salir")
    opcion=input("Selecciona una de las opciones anteriores: ")
    while opcion not in string.digits:
        print("\nLa opción debe ser un número del 1 al 8 ")
        opcion=input("Selecciona una de las opciones anteriores: ")
    if int(opcion) not in range(1,9):
        print("\nLa opción debe ser un número del 1 al 8 ")
    print("\n")
    return int(opcion)
opcion=Opciones()
arbol=Arbol()
while opcion!=8:
    if opcion==1:
        cont=1
        while cont==1:
            cont=0
            num=input("Introduce el número que quieras insertar en el árbol: ")
            for i in num:
                if i not in string.digits:
                    cont=1
        arbol.Insertar(int(num))
        print("\n")
        Imprimir(arbol)
        print("\n")
    elif opcion==2:
        cont=1
        while cont==1:
            cont=0
            num=input("Introduce el número que quieras borrar del árbol: ")
            for i in num:
                if i not in string.digits:
                    cont=1
        arbol.Eliminar(int(num))
        print("\n")
        Imprimir(arbol)
        print("\n")
    elif opcion==3:
        cont=1
        while cont==1:
            cont=0
            num=input("Introduce el número que quieres buscar en el árbol: ")
            for i in num:
                if i not in string.digits:
                    cont=1
        if arbol.Buscar(int(num))==False:
            print("\nEl número que has introducido no se encuentra en el árbol")
            ans=str(input("¿Quieres introducirlo? (S o N): "))
            if ans=="S":
                arbol.Insertar(int(num))
                print("\n")
                Imprimir(arbol)
                print("\n")
        else:
            x=arbol.Buscar(int(num))
            print("\nEl número %s se encuentra en el árbol"%num)
    elif opcion==4:
        Imprimir(arbol)
    elif opcion==5:
        lista=[]
        arbol.Recorrer(lista)
        lista.sort()
        ans=input("¿Lo quieres en formato de lista? (S o N)")
        if ans=="S":
            print(lista)
    elif opcion==6:
        arbol=Arbol()
        print("\n Arbol borrado, para comprobarlo seleccione la opción 4 para ver el árbol")
    elif opcion==7:
        arbol=Arbol()
        with open('arbol.txt','r') as file:
            numeros=file.read().splitlines()
        for i in numeros:
            arbol.Insertar(int(i))
        Imprimir(arbol)
    opcion=Opciones()           
    
        
            
           
                
