import random
import matplotlib.pyplot as plt


def recuperar_datos(nombre):
    try:
        with open(nombre + '.csv', 'r', newline='') as archivo:
            contenido = archivo.readlines()
        datos_enteros = [[float(elemento) for elemento in lista] for lista in
                         [linea.strip().split(",") for linea in contenido]]
        return datos_enteros
    except:
        return []


class kMeans:
    def __init__(self, datos, kGrupos, centroides):
        self.datos = datos
        self.kGrupos = kGrupos
        self.centroides = centroides
        self.grupos = [[] for _ in range(kGrupos)]

    def calcular_distancia(self, puntoA, puntoB):
        return (sum([(puntoA[i] - puntoB[i]) ** 2 for i in range(len(puntoA))])) ** 0.5

    def calcular_centroides(self):
        nuevos_centroides = []
        for grupo in self.grupos:
            suma_coordenadas = [sum(coordenadas) for coordenadas in zip(*grupo)]
            promedio_coordenadas = [suma / len(grupo) for suma in suma_coordenadas]

            nuevos_centroides.append(promedio_coordenadas)
        return nuevos_centroides

    def entrenar(self):
        while True:
            for punto in self.datos:
                self.grupos[self.clasificar(punto)].append(punto)

            nuevos_centroides = self.calcular_centroides()

            if nuevos_centroides == self.centroides:
                break
            else:
                self.centroides = nuevos_centroides
                self.grupos = [[] for _ in range(kGrupos)]

    def clasificar(self, punto):
        lista_distancias = []
        for centroide in self.centroides:
            lista_distancias.append(self.calcular_distancia(punto, centroide))
        return lista_distancias.index(min(lista_distancias))

    def graficar(self):
        # Crear el gráfico de puntos
        plt.scatter([punto[0] for punto in self.grupos[0]], [punto[1] for punto in self.grupos[0]], c='yellow')
        plt.scatter([punto[0] for punto in self.grupos[1]], [punto[1] for punto in self.grupos[1]], c='purple')
        plt.scatter([punto[0] for punto in self.centroides], [punto[1] for punto in self.centroides], c='black',
                    marker='x')

        # Etiquetas de los ejes
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')

        # Título del gráfico
        plt.title('Gráfico de puntos')

        # Mostrar el gráfico
        plt.show()


datos = recuperar_datos("../csv/sample_data.csv")

kGrupos = 2

centroides = [datos[i] for i in random.sample(range(len(datos)), kGrupos)]

kMeans = kMeans(datos, kGrupos, centroides)
kMeans.entrenar()

print("CENTROIDES FINALES")
for centroide in kMeans.centroides:
    print([round(numero, 5) for numero in centroide])

print("CLASIFICACIÓN")
for punto in datos:
    print("Punto: ", punto, ", cluster", kMeans.clasificar(punto))
