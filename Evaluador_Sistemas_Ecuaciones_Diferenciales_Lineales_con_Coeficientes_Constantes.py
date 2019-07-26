import pylab
import math
from functools import reduce
import numpy as np

def crearLista(tamaño, valores):
    return [valores for i in range(tamaño)]

def crearMatriz(tamañoFila, tamañoColumna, valores):
    return [[valores for j in range(tamañoFila)] for i in range(tamañoColumna)]

def funcionMultiplicarListas(factor1, factor2):
        return [factor1[i]*factor2[i] for i in range(len(factor1))]

def funcionSumarListas(sumando1, sumando2):
    return [sumando1[i] + sumando2[i] for i in range(len(sumando1))]

def funcionLineal(constantes, variables, sistemaActual):
    i = sistemaActual
    resultado = 0
    for j in (range(3)):
        resultado = resultado + constantes[i][j]*variables[i+j]
    return resultado

def rungeKutta(f, sumVar, multVar, var, cons, lim, p):
    j = 0
    tamVar = len(var)
    h = crearLista(tamVar, p)
    h2 = crearLista(tamVar, p/2)
    k1 = crearLista(tamVar, 0)
    k2 = crearLista(tamVar, 0)
    k3 = crearLista(tamVar, 0)
    k4 = crearLista(tamVar, 0)
    posiciones = crearMatriz(lim,tamVar, 0)
    
    while(j<lim):
        for i in range(tamVar-2):
            k1[i] = h[0] * f(cons, var, i) #k1[x0] = h * (c1xs, c2x0, c3x1)
        for i in range(tamVar-2):
            k2[i] = h[0] * f(cons, sumVar(var, multVar(h2, k1)), i)
        for i in range(tamVar-2):
            k3[i] = h[0] * f(cons, sumVar(var, multVar(h2, k2)), i)
        for i in range(tamVar-2 ):
            k4[i] = h[0] * f(cons, sumVar(var, multVar(h, k3)), i)
        for i in range(tamVar):
            if i<(tamVar-1): #La ultima variable var(tamVar-1) corresponde a 0, no existe, la primera es una constante Ts, por eso no cambian
                var[i+1] = var[i+1] + (1/6) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) #la variable x[i+1] es la variable que corresponde a la derivada i
        for i in range(tamVar):
                posiciones[i][j]=var[i]
        j+=1
    return posiciones

def periodizarFunciones(listaDeFunciones):
    maximoLogaritmico = 0.01
    paso = 1/len(listaDeFunciones[0])
    for i in range(len(listaDeFunciones)):
        for j in range(len(listaDeFunciones[i])):
            listaDeFunciones[i][j] = listaDeFunciones[i][j]
            if maximoLogaritmico < math.fabs(listaDeFunciones[i][j]):
                maximoLogaritmico = math.fabs(listaDeFunciones[i][j])
    for i in range(len(listaDeFunciones)):
        for j in range(len(listaDeFunciones[i])):
            listaDeFunciones[i][j] = listaDeFunciones[i][j] * math.sin( math.pi*paso*j )**2  / (10 ** (math.log10(maximoLogaritmico)-2))
    return listaDeFunciones

def graficar(variableDependiente, variableIndependiente):
    t = variableDependiente
    x = variableIndependiente
    leyenda=["variable Sub"]
    for i in range(len(x)-1):
        pylab.plot(t ,x[i] ,'-')
        #print("Variable "+  str(i) + ": " + str(x[i]))
        if i!=0:
            leyenda.append("Piso " + str(i))
    #for i in range(len(x[1])):
      #  print("t: "+str(t[i])[:4]+", x: "+str(x[1][i]))
    pylab.legend(leyenda)
    pylab.grid(True)
    pylab.show()

def construirConstantes(cap, res): #Existen n pisos, con n capacitancias, y n+1 resistencias 
    constantes = crearMatriz(3, len(cap), 0)
    if len(cap)>2:
        for i in range(len(cap)):# i representa los pisos (sistema de ecuaciones), la primera resistencia representa el piso inferior, la segunda resistencia representa la del primer piso o actual (i+1)
            constantes[i][0] = (1/(cap[i]*res[i]))
            constantes[i][1] = ((-1)/(cap[i]*res[i+1])) + ((-1)/(cap[i]*res[i]))
            constantes[i][2] = ((1/cap[i]*res[i+1]))    
    return constantes

def construirCapacitancias(ListaDePisos):
    capacitancias = []
    for piso in ListaDePisos:
        capacitancias.append(piso[1])
    return capacitancias

def construirResistencias(ListaDePisos, resistenciaSubterranea = 1):
    resistencias = []
    resistencias.append(resistenciaSubterranea)
    for piso in ListaDePisos:
        resistencias.append(piso[2])
    return resistencias

def construirCondicionesInicialesMinimas(ListaDePisos,condicionSubterranea = 0):
    condiciones = []
    condiciones.append(condicionSubterranea)
    for piso in ListaDePisos:
        if piso[3] != 0:
            condiciones.append(piso[3])
        else:
            condiciones.append(1)
    condiciones.append(0)
    return condiciones
    
def construirCondicionesInicialesMaximas(ListaDePisos,condicionSubterranea = 0):
    condiciones = []
    condiciones.append(condicionSubterranea)
    for piso in ListaDePisos:
        if piso[3] != 0:
            condiciones.append(piso[4])
        else:
            condiciones.append(1)
    condiciones.append(0)
    return condiciones

def imprimirConstructores(ListaDePisos):
    variablesMaximas = construirCondicionesInicialesMaximas(ListaDePisos)
    variablesMinimas = construirCondicionesInicialesMinimas(ListaDePisos)
    capacitancias = construirCapacitancias(ListaDePisos)
    resistencias = construirResistencias(ListaDePisos)
    constantes = construirConstantes(capacitancias, resistencias)

def analizarHabitabilidad(funciones, limiteMaximo, limiteMinimo):
    pisosFrios = []
    pisosCalientes = []
    for i in range(len(funciones)):
        for j in funciones[i]:
            if (j > limiteMaximo) and not(i in pisosCalientes):
                pisosCalientes.append(i)
            elif (j < limiteMinimo) and not(i in pisosFrios):
                pisosFrios.append(i)
                
    for piso in pisosFrios:
        print("El piso número " + str(piso) + " es inhabitable por alcanzar temperaturas muy frias")
    for piso in pisosCalientes:
        print("El piso número " + str(piso) + " es inhabitable por alcanzar temperaturas muy altas")
        
def evaluarSistema(ListaDePisos, temperaturaAmbiente):
    inicio=0.03
    final=0.18
    paso=0.001
    t = np.arange(inicio, final, paso)
    limite=int((final-inicio)/paso)
    
    variablesMaximas = construirCondicionesInicialesMaximas(ListaDePisos)
    variablesMinimas = construirCondicionesInicialesMinimas(ListaDePisos)
    capacitancias = construirCapacitancias(ListaDePisos)
    resistencias = construirResistencias(ListaDePisos)
    constantes = construirConstantes(capacitancias, resistencias)
    
    
    #constantes = construirConstantes(construirCapacitancias(ListaDePisos), construirResistencias(ListaDePisos))
    #variables = [0,1,6,1,5,0]
    #constantes = [[1,-1/65,1/4],[1/4,-1/13,1/4],[1/474,-1/78,1/74],[1/74,-1/8,0]]
    
    #variables=[0,1,1,0]
    #constantes=[[0,-1,1],[1/22,1/55,0]]
    
    x = (rungeKutta(funcionLineal, funcionSumarListas, funcionMultiplicarListas, variablesMaximas, constantes, limite, paso))
    x = periodizarFunciones(x)
    for i in range(len(x)):
        x[i] = funcionSumarListas(x[i],crearLista(len(x[i]), temperaturaAmbiente))
    graficar(t,x)
    
    x = (rungeKutta(funcionLineal, funcionSumarListas, funcionMultiplicarListas, variablesMinimas, constantes, limite, paso))
    x = periodizarFunciones(x)
    for i in range(len(x)):
        x[i] = funcionSumarListas(x[i],crearLista(len(x[i]), temperaturaAmbiente))
    graficar(t,x)
    
    analizarHabitabilidad(x, 43, -5)
    #x[1] = funcionSumarListas(x[1],crearLista(len(x[1]),1))

#evaluarSistema()