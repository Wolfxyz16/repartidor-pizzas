#!/usr/bin/env python3

import os
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.sensor import Sensor
from time import sleep

# Función para leer valores del sensor LSA
def readLSA(lsa):
    # Se inicializa una lista vacía para almacenar los valores
    lista=[]
    for i in range(0,8):
        # Se agregan las 8 lecturas del sensor
        lista.append(lsa.value(i))
    return lista

# Función para calcular la media de los valores en un array
def media(array):
    media = 0
    for i in array:
        media += i
    return media / len(array)

# Función para convertir los valores LSA en una lista binaria
def binario(array):
    lista = []
    for i in array:
        if i < 90: # si el valor es menor a 90, hay linea
            lista.append(1)
        else: # si el valor es igual o mayor a 90, no hay linea
            lista.append(0)
    return lista

# Función para multiplicar elemento a elemento dos listas
def multiplicar_listas(lista1, lista2):
    resultado = []
    for i in range(len(lista1)):
        resultado.append(lista1[i] * lista2[i])
    return resultado

# Función para calcular una velocidad dependiendo de la posición de la línea
def f(x, vel_max, vel_min):

    # Calculamos una velocidad que depende de x, que depende de vel_min y vel_max
    if x<3:
        return ( ( x * (vel_max - vel_min) ) / 3 ) + vel_min
    else:
        # Si x es mayor o igual a 3, devolvemos la velocidad máxima
        return vel_max

    

# [ 0   1   1   0   0   0   0   0 ] girar hacia izquierda
# [ 0   0   0   0   0   1   1   0 ] girar hacia derecha
# [ 0   0   0   1   1   0   0   0 ] no girar

def main():
    print("Welcome lsa_v2")
    lsa = Sensor()
    tank = MoveTank(OUTPUT_A, OUTPUT_D)
    # Definimos los pesos que indican la "importancia" de cada lectura
    pesos = [7, 6, 5, 4, 3, 2, 1, 0]
    # Velocidad máxima
    vel_max = 50
    # Velocidad mínima
    vel_min = 20
    
    while True:
        lecturas = readLSA(lsa)
        lista_binaria = binario(lecturas)
        resultado = multiplicar_listas(lista_binaria, pesos)

        # Verificamos si hay alguna línea detectada (1 en la lista binaria)
        if sum(lista_binaria) != 0:
            # Calculamos la posición promedio de la línea detectada
            posicion = sum(resultado) / sum(lista_binaria)
        
        # Calculamos la velocidad de cada motor usando la posición de la línea
        # Velocidad del motor izquierdo
        vl = f(posicion, vel_max, vel_min)
        # Velocidad del motor derecho
        vr = f(7 - posicion, vel_max, vel_min)

        print("vl: " + str(vl))
        print("vr: " + str(vr))

        tank.on(vl, vr)


if __name__ == "__main__":
    main()