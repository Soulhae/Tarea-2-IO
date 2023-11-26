import os
import random
import math
import time
start_time = time.time()

class SimulatedAnnealing():

    def __init__(self):
        self.initTemp = 7000 #Temperatura inicial
        self.coolingConst = 0.99 #Parámetro de enfriamento geométrico
        self.minTemp = 0.01 #Criterio de término, temperatura mínima
        
        self.n = -1
        self.i = -1
        self.f_size = None          #Inicialización de variables
        self.f_weight = None
        self.solucion = None
        self.simAnnealing()

    def simAnnealing(self): #Es la primera función que se ejecuta, y es donde se encuentra la metaheurística implementada
        firstSolucion = self.leerArchivo() #leerArchivo retorna solucionRandom, que nos genera nuestra primera solución
        # print(self.getEsfuerzo(firstSolucion))
        solActual = firstSolucion
        bestSolucion = firstSolucion
        tempActual = self.initTemp
        # test = 1
        print('Estamos trabajando para usted...')
        while tempActual>self.minTemp and (time.time() - start_time)<10:   #Dos criterios de término, temperatura mínima y tiempo de ejecución
        # while test<maxA:
            solVecina = self.generarVecino(solActual)
            evalVecina = self.getEsfuerzo(solVecina)
            evalActual = self.getEsfuerzo(solActual)
            if(evalVecina < evalActual):    #Al ser un problema de minimización, si la función de evaluación del vecino es menor se acepta directamente
                solActual = solVecina
            else:   #Si no, calculamos la probabilidad del criterio de Metrópolis, sacamos un número aleatorio y si es menor que esta probabilidad, aceptamos la solución
                prob = math.exp(-((evalVecina - evalActual)/tempActual))
                if random.uniform(0,1) < prob:
                    solActual = solVecina
                    # print('acepta')
                # else:
                    # print('no acepta')
            evalActual = self.getEsfuerzo(solActual)
            # print(solActual)
            # print(evalActual)
            # test += 1
            if(evalActual < self.getEsfuerzo(bestSolucion)):    #Vamos evaluando la solución que quede del proceso anterior, y si es mejor la guardamos en nuestra variable bestSolucion
                bestSolucion = solActual
            tempActual = tempActual * self.coolingConst     #Aplicamos enfriamiento para que de a poco vaya pasando de una alta exploración a una alta explotación
        listaPosiciones = []
        for item in bestSolucion:
            listaPosiciones.append(item[0])
        print('--- Solución óptima encontrada con los criterios de término propuestos ---')
        print(listaPosiciones)
        print('Esfuerzo de la solución encontrada: '+str(self.getEsfuerzo(bestSolucion))+'\n')
        print("--- Tiempo de ejecución: %.4s segundos ---" % (time.time() - start_time))

    def solucionRandom(self):   #Genera una solución aleatoria basada en la que se lee en leerArchivo
        listaSolucion = list(self.solucion.items())
        random.shuffle(listaSolucion)
        return listaSolucion

    def getEsfuerzo(self, solucion):    #Función que evalúa la solución para retornar el esfuerzo

        total = 0.0
        middle_distance = 0.0

        for i in range(self.n - 1):
            p1 = solucion[i][1]
            middle_distance = 0.0
            for j in range(i + 1, self.n):
                p2 = solucion[j][1]
                total += ((p1 / 2) + middle_distance + (p2 / 2)) * self.f_weight[i][j]
                middle_distance += p2
        return total
    
    def generarVecino(self, solucionActual): #Movimiento swap entre 2 instalaciones random
        vecino = solucionActual[:]
        i = random.randint(0, len(vecino) - 1)
        j = random.randint(0, len(vecino) - 1)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return vecino

    def leerArchivo(self): #Funcion que permite leer los archivos txt que contienen los datos, donde se guardan el número de instalaciones, los tamaños y una matriz de flujos
        listaArchivos = []
        for file_path in os.listdir(os.getcwd()):
            if os.path.isfile(os.path.join(os.getcwd(), file_path)):
                if file_path.endswith('.txt'):
                    listaArchivos.append(file_path)
        h = 1

        for archivo in listaArchivos:
            print(str(h)+'.- '+archivo)
            h+=1
        h = 1
        opcion = input('Elige una instancia para el problema: ')
        a = int(opcion) - 1
        nombreArchivo = listaArchivos[a]

        with open(nombreArchivo, "r", encoding="UTF-8") as bufferedReader:
            line = bufferedReader.readline().strip()

            while line:
                if line.startswith("EOF"):
                    break
                if line.startswith("#"):
                    line = bufferedReader.readline().strip()
                    continue

                if self.n < 0:
                    #Número de instalaciones
                    self.n = int(line)
                    self.f_size = [0] * self.n
                    self.solucion = {} #Se genera un diccionario de solución, para que al generar la solución inicial y el movimiento swap, no se pierdan los índices iniciales
                    self.f_weight = [[0] * self.n for _ in range(self.n)]
                elif self.i == -1:
                    #Tamaño de instalaciones
                    buf = line.split(",")
                    for k in range(self.n):
                        self.f_size[k] = int(buf[k].strip())
                        self.solucion[k + 1] = int(buf[k].strip())
                    self.i = 0
                else:
                    #Flujo entre instalaciones
                    buf = line.split(",")
                    for k in range(self.n):
                        self.f_weight[self.i][k] = int(buf[k].strip())
                    self.i += 1
                line = bufferedReader.readline().strip()

        # for key, value in self.solucion.items():
        #     print(f'Instalación {key}: {value}')
        return self.solucionRandom()

ola=SimulatedAnnealing()