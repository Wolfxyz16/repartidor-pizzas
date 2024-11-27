#!/usr/bin/env python3

import os
from siguelineas_thread import SigueLineasThread
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.sensor import Sensor
from time import sleep

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

    tank.on(vl, vr)

if __name__ == "__main__":
    main()
