# MMPP models consist of a Poisson process modulated by the rate lambda
# which is determined by the state of a Markov chain
# DELTAt denota un arbitrario pero constante intervalo de tiempo y constituye el latido del sistema

import numpy as np  # NumPy package for arrays, random number generation, etc
from scipy.stats import poisson
import math as mth
import simpy
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon


class dispMTC(object):

    # Definición de constructor
    def __init__(self, lambdareg,Xpos,Ypos,estado):
        self.lambdareg=lambdareg
        self.posicion=[Xpos,Ypos]
        self.estado=estado

    # Definición de métodos
    def actualizarEstado(self,Theta):
        self.Pnk= self.calculoPnk(self.calculoThetan(Theta))
        auxuniforme=np.random.uniform(0,1,1)
        if self.estado==1 and auxuniforme > self.Pnk[1][1]:
            self.estado=0
        if self.estado==0 and auxuniforme > self.Pnk[0][0]: # si la variable uniforme es mayor a la probabilidad de que no cambie de estado, cambia de estado
            self.estado=1

    def calculoPnk(self,Thetan):
        return (1-Thetan)*self.m_Pu + Thetan*self.m_Pc

    def calculoThetan(self,Theta):
        delta= np.random.normal(0.5,0.16,1)
        return Theta*delta

    def generarArribo(self,tiempoactual):
        tespera=np.random.exponential(1/(self.lambdareg),1)
        self.tiempoArribo=tiempoactual+tespera
        self.arribos.append(self.tiempoArribo)

    def generarArriboAlarma(self,tiempoactual):
        self.arribos.append(tiempoactual)
        self.cuentaAlarmas=self.cuentaAlarmas+1

    matriz_Pu= [[1,1],[0,0]]
    matriz_Pc= [[0,1],[1,0]]
    Pnk=[]
    m_Pu = np.array(matriz_Pu)
    m_Pc = np.array(matriz_Pc)
    tiempoArribo=100000000
    arribos=[]
    cuentaAlarmas=0


#Iniciación del algoritmo
tiempolimite=10 #segundos , tiempo de paro
tiempo=0 # variable que registro el instante de tiempo actual
Deltatiempo= 0.01 #segundos , diferencial de tiempo entre iteración
titeraciones=tiempolimite/Deltatiempo # las iteraciones  que se producirán
numDisp1=50 # número de dispositivos de tipo 1
lambdareg1=1/60 # la tasa lambda para el estado regular de los dispositivos de tipo 1
disp = []


for k in range(0,numDisp1+1): # Generamos los dispositivos de tipo 1
    disp.append(dispMTC(lambdareg1,np.random.uniform(0,100,1),np.random.uniform(0,100,1),0))

for t in range(0,int(titeraciones)+1): # Ciclo que representa el avance en el tiempo
    Theta = np.random.beta(3, 4, 1)

    print(tiempo)

    for n in range(0,numDisp1+1): # Ciclo que recorre todos los dispositivos
        disp[n].actualizarEstado(Theta)

        if disp[n].estado==1: #alarma
            disp[n].generarArriboAlarma(tiempo)#Generar exactamente 1 paquete
        elif disp[n].tiempoArribo>tiempo:
            disp[n].generarArribo(tiempo) # Generar un paquete en caso de que no exista ya uno

    tiempo= tiempo + Deltatiempo