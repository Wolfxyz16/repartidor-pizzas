#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound
from time import sleep
from threading import Thread


class waitForTones(Thread):
    def __init__(self, threadID, frequency):
        Thread.__init__(self)
        self.threadID = threadID
        self.sound = Sound()
        self.running = True

    def run(self):
        while self.running:
            for j in range(0,20):             # Do twenty times.
                # sound.play_tone(frequency, 0.2) #1500Hz for 0.2s
                sleep(0.5)
        self.sound.beep()


if __name__ == '__main__':
    t = waitForTones(1, 1500)
    t.setDaemon = True
    t.start()
    ts = TouchSensor()
    running = True
    counter = 0
    while running:
        ts.wait_for_bump()
        counter = counter + 1
        if counter >=5:
            t.running = False
            running = False
        sleep(0.01)
