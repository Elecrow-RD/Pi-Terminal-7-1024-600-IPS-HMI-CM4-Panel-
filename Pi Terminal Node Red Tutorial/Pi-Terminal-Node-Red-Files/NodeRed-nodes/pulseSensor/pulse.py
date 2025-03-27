import time
import threading
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_ADS1x15
GPIO.setmode(GPIO.BCM)
GAIN = 1
class Pulsesensor:

    def __init__(self, channel = 0):
        self.channel = channel
        self.BPM = 0
        self.adc = Adafruit_ADS1x15.ADS1115()

    def getBPMLoop(self):
        rate = [0] * 10         # array to hold last 10 IBI values
        sampleCounter = 0       # used to determine pulse timing
        lastBeatTime = 0        # used to find IBI
        P = 512                 # used to find peak in pulse wave, seeded
        T = 512                 # used to find trough in pulse wave, seeded
        thresh = 512            # used to find instant moment of heart beat, seeded
        amp = 100               # used to hold amplitude of pulse waveform, seeded
        firstBeat = True        # used to seed rate array so we startup with reasonable BPM
        secondBeat = False      # used to seed rate array so we startup with reasonable BPM
        IBI = 600               # int that holds the time interval between beats! Must be seeded!
        Pulse = False           # "True" when User's live heartbeat is detected. "False" when not a "live beat".
        lastTime = int(time.time()*1000)
        while not self.thread.stopped:
            Signal = (self.adc.read_adc(channel=self.channel, gain=1, data_rate=128)) / 24
            # print('Signal', Signal)
            currentTime = int(time.time()*1000)
            sampleCounter += currentTime - lastTime
            lastTime = currentTime
            N = sampleCounter - lastBeatTime
            # find the peak and trough of the pulse wave
            if Signal < thresh and N > (IBI/5.0)*3:     # avoid dichrotic noise by waiting 3/5 of last IBI
                if Signal < T:                          # T is the trough
                    T = Signal                          # keep track of lowest point in pulse wave
            if Signal > thresh and Signal > P:
                P = Signal
            # signal surges up in value every time there is a pulse
            if N > 250:                                 # avoid high frequency noise
                if Signal > thresh and Pulse == False and N > (IBI/5.0)*3:
                    Pulse = True                        # set the Pulse flag when we think there is a pulse
                    IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
                    lastBeatTime = sampleCounter        # keep track of time for next pulse

                    if secondBeat:                      # if this is the second beat, if secondBeat == TRUE
                        secondBeat = False;             # clear secondBeat flag
                        for i in range(len(rate)):      # seed the running total to get a realisitic BPM at startup
                          rate[i] = IBI
                    if firstBeat:                       # if it's the first time we found a beat, if firstBeat == TRUE
                        firstBeat = False;              # clear firstBeat flag
                        secondBeat = True;              # set the second beat flag
                        continue

                    # keep a running total of the last 10 IBI values
                    rate[:-1] = rate[1:]                # shift data in the rate array
                    rate[-1] = IBI                      # add the latest IBI to the rate array
                    runningTotal = sum(rate)            # add upp oldest IBI values
                    runningTotal /= len(rate)           # average the IBI values
                    self.BPM = 60000/runningTotal       # how many beats can fit into a minute? that's BPM!

            if Signal < thresh and Pulse == True:       # when the values are going down, the beat is over
                Pulse = False                           # reset the Pulse flag so we can do it again
                amp = P - T                             # get amplitude of the pulse wave
                thresh = amp/2 + T                      # set thresh at 50% of the amplitude
                P = thresh                              # reset these for next time
                T = thresh

            if N > 2500:                                # if 2.5 seconds go by without a beat
                thresh = 512                            # set thresh default
                P = 512                                 # set P default
                T = 512                                 # set T default
                lastBeatTime = sampleCounter            # bring the lastBeatTime up to date
                firstBeat = True                        # set these to avoid noise
                secondBeat = False                      # when we get the heartbeat back
                self.BPM = 0

            time.sleep(0.005)

    # Start getBPMLoop routine which saves the BPM in its variable
    def startAsyncBPM(self):
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.stopped = False
        self.thread.start()
        return

    # Stop the routine
    def stopAsyncBPM(self):
        self.thread.stopped = True
        self.BPM = 0
        return

import time
import sys
p = Pulsesensor()
flag = 0
touch_time=0
touch_time1=0
time_print = 0

try:
    while True:
        Signal=p.adc.read_adc(p.channel, GAIN) / 24
        time.sleep(0.2)
        touch_time += 200
        touch_time1 += 200
        time_print += 200
        if Signal < 10 and touch_time > 2000 and flag == 0:
            flag = 1
            print('start detect pulse!')
            time.sleep(2)
            p.startAsyncBPM()

        if Signal > 1000 and touch_time1 > 2000 and flag == 1:
            flag = 0
            print('stop detect pulse!')
            p.stopAsyncBPM()

        if Signal > 10 and Signal < 850:
            touch_time=touch_time1=0

        if time_print>1000 and flag==1:
            time_print=0
            bpm = (p.BPM)
            if bpm > 0:
                # print("BPM: %d" % (bpm/3))
                print(int(bpm/3))
except:
    # print('some error heppend')
    p.stopAsyncBPM()