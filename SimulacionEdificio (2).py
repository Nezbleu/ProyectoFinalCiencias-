# -*- coding: utf-8 -*-
"""
Listas doblemente enlazadas
para la simulacion de los pisos del edificio
"""
import Evaluador_Sistemas_Ecuaciones_Diferenciales_Lineales_con_Coeficientes_Constantes as evaluador
# Clase del piso en general, con los parametros de Conductividad Termica y Resistencia Termica
    #__init__:             Constructor
    # getElementos         Retorna las propiedades externas del piso
    #getPisoInterno        Retorna el elemento que contiene las propiedades internas del piso
class Piso(object):
    def __init__(self,NumPiso,Ctermica,Rtermica,Tmin,Tmax,PisoInterno):
        #Atributos que tendra el nodo
        self.__NumPiso=NumPiso
        self.__Ctermica=Ctermica
        self.__Rtermica=Rtermica
        self.__Tmax=Tmax
        self.__Tmin=Tmin
        self.__PisoInterno=PisoInterno

        #Punteros del nodo
        self.__pSig = None
        self.__pAnt = None

    def getElementos(self):
        return self.__NumPiso, self.__Ctermica,self.__Rtermica,self.__Tmin,self.__Tmax
    
    def getPisoInterno(self):
        return self.__PisoInterno.getElementos()

# Clase de la estructura interna de un piso
    #__init__:             Constructor
    # getElementos         Retorna las propiedades internas del piso
class PisoInterno(object):
    def __init__(self,MatParedes,CantCuartos,UsoPiso,TempMin,TempMax):
        #Atributos que tendra el nodo
        self.__MatParedes=MatParedes
        self.__CantCuartos=CantCuartos
        self.__UsoPiso=UsoPiso
        self.__TempMin=TempMin
        self.__TempMax=TempMax

    def getElementos(self):
        return self.__MatParedes,self.__CantCuartos,self.__UsoPiso,self.__TempMin,self.__TempMax

# Clase Lista Doblemente Enlazada de los cuartos del edificio con todos sus metodos
    #__init__:             Constructor
    #calculosResistencia:  Calculadora de la resistencia térmica de un material
    #calculosCapacitancia: Calculadora de la resistencia térmica de un entorno
    #crearPermoda:         Creador de un edificio predefinido
    #eliminarUltimo:       Elimina el último piso agregado
    #getListaPisos:        Genera una lista de los elementos Piso que hay en el edificio
    #getVacio:             Indica si el edificio no tiene ningun piso construido
    #menu:                 Interfaz desplegable donde se trabaja la clase ListaDoblePisos
    #printListaExternos:   Imprime la lista de pisos con sus propiedades externas
    #printListaInternos:   Imprime la lista de pisos con sus propiedades internas
    #setNodoAlFinal:       Añade un nuevo piso al edificio
class ListaDoblePisos(object):
    
    def __init__(self):
        self.__primero = None
        self.__ultimo = None
        self.__piso = 0
        self.__temperaturaAmbiente = 30

    def calculosResistencia(self,material):

        if material=="Hierro":
            return (0.1246)
        elif material=="Ladrillo":
            return (12.5)
        elif material=="Aluminio":
            return(0.0477)
        elif material=="Madera":
            return(12.5)
        elif material=="Vidrio":
            return(16.82)
        else:
            return (1)
    
    def calculosCapacitancia(self,uso, cuartos):
        if cuartos==0:
            if uso=="Oficina":
                return(0.02)
            elif uso=="Industrial":
                return(0.08) 
            else:
                return(0.02)
        else:
            if uso=="Oficina":
                return(0.02 * cuartos)
            elif uso=="Industrial":
                return(0.08 * cuartos) 
            else:
                return(0.02)
            
    def crearPermoda(self, pisoActual):
        self.setNodoAlFinal("Vidrio",3,"Oficina",5,20,pisoActual+1,self.calculosCapacitancia("Oficina",5),self.calculosResistencia("Vidrio"))
        self.setNodoAlFinal("Vidrio",5,"Oficina",5,20,pisoActual+2,self.calculosCapacitancia("Oficina",5),self.calculosResistencia("Vidrio"))
        self.setNodoAlFinal("Vidrio",2,"Oficina",5,20,pisoActual+3,self.calculosCapacitancia("Oficina",5),self.calculosResistencia("Vidrio"))
    
    def crearEcomoda(self, pisoActual):
        self.setNodoAlFinal("Hierro",3,"Industrial",5,20,pisoActual+1,self.calculosCapacitancia("Industrial",5),self.calculosResistencia("Hierro"))
        self.setNodoAlFinal("Hierro",5,"Industrial",1,20,pisoActual+2,self.calculosCapacitancia("Industrial",5),self.calculosResistencia("Hierro"))
        self.setNodoAlFinal("Hierro",2,"Industrial",1,20,pisoActual+3,self.calculosCapacitancia("Industrial",5),self.calculosResistencia("Hierro"))
    
    
    def eliminarUltimo(self):
        if self.getVacio()==True:
            print("La lista esta vacia")

        elif self.__primero==self.__ultimo:
            self.__primero=None
            self.__ultimo=None
            print("Elemento eliminado, la lista esta vacia")

        else:
            temp = self.__ultimo
            self.__ultimo=self.__ultimo.pAnt
            self.__ultimo.pSig=None
            temp = None
            print("Elemento eliminado")
    
    def getListaPisos(self):
        if self.getVacio()==True:
            return []
        else:
            lista=[]
            validar=True
            temp= self.__primero
            while(validar):
                lista.append(temp)
                if temp == self.__ultimo:
                    validar=False
                else:
                    temp= temp.pSig
            return lista
        
    def getListaPisosExternos(self):
        lista = []
        edificio = self.getListaPisos()
        for piso in edificio:
            lista.append(piso.getElementos())
        return lista
           
    def getVacio(self):
        if self.__primero == None:
            return True

    def menu(self):
        numPiso=0
        while True:
            # Mostramos el menu
            print ("Selecciona una opción")
            print ("\t1 - añadir un nuevo piso")
            print ("\t2 - eliminar un piso")
            print ("\t3 - mostrar los pisos internos")
            print ("\t4 - mostrar los pisos externos")
            print ("\t5 - desarrollar una temperatura ambiente")
            print ("\t6 - realizar análisis de habitabilidad")
            print ("\t7 - crear edificio prediseñado (ECOMODA)")
            print ("\t8 - crear edificio prediseñado (PERMODA)")
            print ("\t9 - salir")
            # solicituamos una opción al usuario
            opcionMenu = input("inserta un numero valor >> ")
            if opcionMenu=="1":
                print ("")
                numPiso=numPiso+1
                material= input("inserta el material en el que estan construidas sus paredes \nHierro\nLadrillo\nAluminio\nMadera\nVidrio \n>> ")
                cantCuartos= input("inserta la cantidad de cuatros que tendra el piso >> ")
                usoPiso= input("inserta el uso que tendra el piso (Oficina o Industrial) >> ")
                temMin= input("inserta la temperatura minima que tendra el piso >> ")
                temMax= input("inserta la temperatura maxima que tendra el piso >> ")
                self.setNodoAlFinal(material,cantCuartos,usoPiso,temMin,temMax,numPiso,self.calculosCapacitancia(usoPiso,cantCuartos),self.calculosResistencia(material))
                input("pulsa una tecla para continuar")
                
            elif opcionMenu=="2":
                print ("")
                self.eliminarUltimo()
                input("Se elimino el ultimpo piso...\npulsa una tecla para continuar")
            elif opcionMenu=="3":
                print ("")
                self.printListaInternos()
                input("pulsa una tecla para continuar")
            elif opcionMenu=="4":
                print ("")
                self.printListaExternos()
                input("pulsa una tecla para continuar")
            elif opcionMenu=="5":
                print ("")
                self.__temperaturaAmbiente = input("Introduzca una temperatura ambiente")
                input("pulsa una tecla para continuar")
            elif opcionMenu=="6":
                print ("")
                evaluador.evaluarSistema(self.getListaPisosExternos(),self.__temperaturaAmbiente)
                input("pulsa una tecla para continuar")
            elif opcionMenu=="7":
                print ("")
                self.crearEcomoda(numPiso)
                numPiso+=3
                input("pulsa una tecla para continuar")
            elif opcionMenu=="8":
                print ("")
                self.crearPermoda(numPiso)
                numPiso+=3
                input("pulsa una tecla para continuar")
            elif opcionMenu=="9":
                break
            else:
                print ("")
                input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
                
    def printListaExternos(self):
        edificio = self.getListaPisos()
        if len(edificio)==0:
            print("No hay un edificio construido")
        else:
            for piso in edificio:
                print(piso.getElementos())

    def printListaInternos(self):
        edificio = self.getListaPisos()
        if len(edificio)==0:
            print("No hay un edificio construido")
        else:
            for piso in edificio:
                print(piso.getPisoInterno())

    def setNodoAlFinal(self,MatParedes,CantCuartos,UsoPiso,TempMin,TempMax,NumPiso,Ctermica,Rtermica):
        nuevo = Piso(NumPiso,Ctermica,Rtermica,TempMin,TempMax,PisoInterno(MatParedes,CantCuartos,UsoPiso,TempMin,TempMax))
        if self.getVacio()==True:
            self.__primero = self.__ultimo = nuevo
        else:
            self.__ultimo.pSig=nuevo
            nuevo.pAnt=self.__ultimo
            self.__ultimo=nuevo
            
#MAIN

inicio=ListaDoblePisos()
inicio.menu()









