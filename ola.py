import os
import random
import math
import time
start_time = time.time()

class SimulatedAnnealing():

    def __init__(self):
        self.initTemp = 10000 #Temperatura inicial
        self.coolingConst = 0.99 #Parámetro de enfriamento geométrico
        self.minTemp = 0.01 #Criterio de término, temperatura mínima
        
        self.n = -1
        self.i = -1
        self.f_size = None
        self.f_weight = None
        self.solucion = None
        self.simAnnealing()

    def simAnnealing(self):
        firstSolucion = self.leerArchivo()
        # print(self.getEsfuerzo(firstSolucion))
        solActual = firstSolucion
        bestSolucion = firstSolucion
        tempActual = self.initTemp
        test = 1
        while tempActual>self.minTemp:
        # while test<maxA:
            solVecina = self.generarVecino(solActual)
            evalVecina = self.getEsfuerzo(solVecina)
            evalActual = self.getEsfuerzo(solActual)
            if(evalVecina < evalActual):
                solActual = solVecina
            else:
                prob = math.exp(-((evalVecina - evalActual)/tempActual))
                if random.uniform(0,1) < prob:
                    solActual = solVecina
                    # print('acepta')
                # else:
                    # print('no acepta')
            evalActual = self.getEsfuerzo(solActual)
            # print(solActual)
            # print(evalActual)
            test += 1
            if(evalActual < self.getEsfuerzo(bestSolucion)):
                bestSolucion = solActual
            tempActual = tempActual * self.coolingConst
        listaPosiciones = []
        for item in bestSolucion:
            listaPosiciones.append(item[0])
        print(listaPosiciones)
        print(self.getEsfuerzo(bestSolucion))
        print("--- Tiempo de ejecución: %.4s segundos ---" % (time.time() - start_time))

    def solucionRandom(self):
        listaSolucion = list(self.solucion.items())
        random.shuffle(listaSolucion)
        return listaSolucion

    def getEsfuerzo(self, solucion):

        total = 0.0
        middle_distance = 0.0

        for i in range(self.n):
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

    def leerArchivo(self):
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
                    # Primera linea número de instalaciones
                    self.n = int(line)
                    self.f_size = [0] * self.n
                    self.solucion = {}
                    self.f_weight = [[0] * self.n for _ in range(self.n)]
                elif self.i == -1:
                    # Segunda linea tamaño de instalaciones
                    buf = line.split(",")
                    for k in range(self.n):
                        self.f_size[k] = int(buf[k].strip())
                        self.solucion[k + 1] = int(buf[k].strip())
                    self.i = 0
                else:
                    # Tercera linea flujo entre instalaciones
                    buf = line.split(",")
                    for k in range(self.n):
                        self.f_weight[self.i][k] = int(buf[k].strip())
                    self.i += 1
                line = bufferedReader.readline().strip()

        # print(f"Numero de instalaciones: {self.n}")
        # print("Tamaños:", " ".join(map(str, self.f_size)))
        # print("Flujo:")
        # for row in self.f_weight:
        #     print(" ".join(map(str, row)))
        for key, value in self.solucion.items():
            print(f'Instalación {key}: {value}')
        return self.solucionRandom()

ola=SimulatedAnnealing()