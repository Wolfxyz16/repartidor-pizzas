class SigueLineasThread(Thread):
    """
    Hilo encargado de seguir la línea negra sin salirse

    Atributos:
        lecturas (list): Lecturas del sensor LSA
        pesos (list): Pesos con los que pondera la posición de la línea, cuanto más en los extremos mayor valor
        vel_min, vel_max (int): Velocidades mínimas y máximas que puede asignar a los servomotres

    Métodos:
        binario: Recibe las lecturas de LSA y devuelve una lista de binarios diciendo si hay linea o no. <90 hay linea
    """
    
    def __init__(self, threadID, lsa):
        Thread.__init__(self)
        self.threadID = threadID
        self.running = True
        self.lsa = lsa
        self.pesos = [7, 6, 5, 4, 3, 2, 1, 0]
        self.vel_min = 20
        self.vel_max = 50
        self.vl = 0
        self.vr = 0

    def readLSA(lsa):
        """
        Función para leer las ocho lecturas del sensor LSA

        Args:
            lsa (Sensor): Objeto de tipo sensor

        returns:
            list: Una lista con las lecturas
        """
        lista = []
        for i in range(0, 8): lista.append(lsa.value(i))
        return lista


    def binario(self, lecturas):
        """
        Función para convertir los valores LSA en una lista binaria

        Args:
            lecturas (list): Lecturas del sensor LSA
        """
        lista = []
        for i in lecturas:
            # si el valor es menor a 90, hay linea
            if i < 90: lista.append(1)

            # si el valor es igual o mayor a 90, no hay linea
            else: lista.append(0)
        return lista

    def f(self, x):
        """
        Esta es la función que utilizamos para calcular a que velocidad debemos de poner los servomotores

        Args:
            x (float): Es un número entre 1-7 que nos indica que posición del sensor está detectando la línea. Ejemplo, 3.5 línea en el medio
        """
        # Calculamos una velocidad que depende de x, que depende de vel_min y vel_max
        if x < 3.0:
            return ( ( x * (self.vel_max - self.vel_min) ) / 3 ) + self.vel_min
        else:
            # Si x es mayor o igual a 3, devolvemos la velocidad máxima
            return self.vel_max

    def run(self):
        while self.running:
            lecturas = readLSA(self.lsa)
            binarios = self.binario(lecturas)
            resultado = [a * b for a, b in zip(binarios, self.pesos)]

            # Verificamos si hay alguna línea detectada (1 en la lista binaria)
            if sum(binarios) != 0:
                # Calculamos la posición promedio de la línea detectada
                posicion = sum(resultado) / sum(binarios)
             
            # Calculamos la velocidad de cada motor usando la posición de la línea

            # Velocidad del motor izquierdo
            self.vl = f(posicion)
            # Velocidad del motor derecho
            self.vr = f(7 - posicion)


def main():
    print("Welcome to pizza delivery :)")
    
    vl, vr = 10, 10
    lsa = Sensor()
    tank = MoveTank(OUTPUT_A, OUTPUT_D)

    # Creamos los hilos
    siguelineas_thread = SigueLineasThread(1, lsa)

    siguelineas_thread.setDaemon() = True

    # Arrancamos los hilos
    siguelineas_thread.start()

    while True:
        tank.on(siguelineas_thread.vl, siguelineas_thread.vr)
        sleep(0.01)

if __name__ == "__main__":
    main()
