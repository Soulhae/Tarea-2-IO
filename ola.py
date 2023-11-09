import os
import random

class SimulatedAnnealing():

    def __init__(self):
        self.initTemp = 2500 #Temperatura inicial
        self.coolingConst = 0.8 #Parámetro de enfriamento geométrico
        self.minTemp = 10 #Criterio de término, temperatura mínima
        
        self.n = -1
        self.i = -1
        self.f_size = None
        self.f_weight = None
        self.solucion = None
        self.simAnnealing()

    def simAnnealing(self):
        firstSolucion = self.leerArchivo()
        bestSolucion = firstSolucion
        tempActual = self.initTemp
        while tempActual>self.minTemp:
            #Evaluar sol y vecino, ver criterio de aceptación
            tempActual = tempActual * self.coolingConst

    def solucionRandom(self):
        random.shuffle(self.solucion)
        return self.solucion
    
    # def critAceptacion(self):     Si es mejor, acepta directamente, si no se calcula probabilidad con el criterio de Metropolis


    # def getEsfuerzo(self, solucion):     Falta multiplicar por el flujo

    #     total = 0.0
    #     middle_distance = 0.0

    #     for i in range(self.n - 1):
    #         p1 = solucion[i]
    #         middle_distance = 0.0
    #         for j in range(i + 1, self.n):
    #             p2 = solucion[j]
    #             total += self.f_size[p1] / 2 + middle_distance + self.f_size[p2] / 2
    #             middle_distance += self.f_size[p2]
    #     return total
    
    def generarVecino(solucion): #Movimiento swap entre 2 instalaciones random
        vecino = solucion[:]
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
                    self.solucion = [0] * self.n
                    self.f_weight = [[0] * self.n for _ in range(self.n)]
                elif self.i == -1:
                    # Segunda linea tamaño de instalaciones
                    buf = line.split(",")
                    for k in range(self.n):
                        self.f_size[k] = int(buf[k].strip())
                        self.solucion[k] = int(buf[k].strip())
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
        # print(self.solucion)
        return self.solucionRandom()

ola=SimulatedAnnealing()