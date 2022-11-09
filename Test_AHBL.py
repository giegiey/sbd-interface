import signal
import serial
import RPi.GPIO as GPIO
from threading import Thread
from datetime import *
import time

# Input Pin definitions
InputSen = 20
OutputSen = 16
IntrusionSen = 21
# Output Pin definitions
LEDred = 13
LEDgreen = 26
LEDblue = 19
# GPIO CONVEYOR
ConREV = 12
ConFWD = 6

global Weight
global SerialTxMsg
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Suppress warnings
GPIO.setwarnings(False)
# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)
# Set Sennsor pin as input
GPIO.setup(InputSen, GPIO.IN)
GPIO.setup(OutputSen, GPIO.IN)
GPIO.setup(IntrusionSen, GPIO.IN)
# Set LED pin as output
GPIO.setup(LEDred, GPIO.OUT)
GPIO.setup(LEDgreen, GPIO.OUT)
GPIO.setup(LEDblue, GPIO.OUT)
# Set Conveyor pin as output
GPIO.setup(ConFWD, GPIO.OUT)
GPIO.setup(ConREV, GPIO.OUT)

# Off everything
GPIO.output(ConFWD, GPIO.HIGH)  # LOW: ON CON, HIGH: OFF LED
GPIO.output(ConREV, GPIO.HIGH)  # LOW: ON CON, HIGH: OFF LED
GPIO.output(LEDred, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED
GPIO.output(LEDblue, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED
GPIO.output(LEDgreen, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED

# red LED on


def redON():
    GPIO.output(LEDred, GPIO.LOW)  # LOW: ON LED, HIGH: OFF LED
    GPIO.output(LEDblue, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED
    GPIO.output(LEDgreen, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED

# blue LED on


def blueON():
    GPIO.output(LEDred, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED
    GPIO.output(LEDblue, GPIO.LOW)  # LOW: ON LED, HIGH: OFF LED
    GPIO.output(LEDgreen, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED

# green LED on


def greenON():
    GPIO.output(LEDred, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED
    GPIO.output(LEDblue, GPIO.HIGH)  # LOW: ON LED, HIGH: OFF LED
    GPIO.output(LEDgreen, GPIO.LOW)  # LOW: ON LED, HIGH: OFF LED

# conveyor forward


def convFWD():
    GPIO.output(ConFWD, GPIO.LOW)  # LOW: ON CON, HIGH: OFF LED
    GPIO.output(ConREV, GPIO.HIGH)  # LOW: ON CON, HIGH: OFF LED

# conveyor reverse


def convREV():
    GPIO.output(ConFWD, GPIO.HIGH)  # LOW: ON CON, HIGH: OFF LED
    GPIO.output(ConREV, GPIO.LOW)  # LOW: ON CON, HIGH: OFF LED

# conveyor stop


def convSTP():
    GPIO.output(ConFWD, GPIO.HIGH)  # LOW: ON CON, HIGH: OFF LED
    GPIO.output(ConREV, GPIO.HIGH)  # LOW: ON CON, HIGH: OFF LED

def onWeight():
    global SerialTxMsg
    SerialTxMsg = "R"

def offWeight():
    global SerialTxMsg
    SerialTxMsg = ""
    

class ScanWeight:

    
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global Weight
        global ser
        global SerialTxMsg

        offWeight()

        bRx = False
        print("ScanWeight thread started...")
        while self._running:
            if SerialTxMsg != "":
                ser.write(SerialTxMsg.encode("utf-8"))
                SerialTxMsg = ""
                bRx = True
            if bRx:
                RxMsg = ser.readline()
                # print(RxMsg)
                # print(len(RxMsg))
                if len(RxMsg) == 13:
                    RxMsg = RxMsg.decode("utf-8")
                    RxMsg = RxMsg[4:9]
                    Weight = str(int(float(RxMsg) * 10)).zfill(5)
                    print(" Weight: " + Weight)
                    bRx = False
                else:
                    print("Error")
                    Weight = ""
                    bRx = False


# ScanWeight
sw = ScanWeight()
swThread = Thread(target=sw.run)
swThread.start()

try:

    # start with green LED
    greenON()

    # send status: READY to BDK.

    while True:
        # GPIO.output(LEDred, GPIO.HIGH) # LOW: ON LED HIGH: OFF LED
        # GPIO.output(LEDblue, GPIO.HIGH) # LOW: ON LED HIGH: OFF LED
        # GPIO.output(LEDgreen, GPIO.LOW) # LOW: ON LED HIGH: OFF LED
        # check if input = block and output = clear
        if GPIO.input(InputSen) == 0 and GPIO.input(OutputSen) == 1:
            # move conveyor
            # blue LED on
            print('Conveyor moving forward. Status: Assisted Heavy Bag Loading ')
            blueON()
            convFWD()
            # time delay to stop conveyor after input sensor block
            time.sleep(3)

            # check if input = clear and output = clear
            if GPIO.input(InputSen) == 1 and GPIO.input(OutputSen) == 1:
                onWeight()
                # normal condition
                # green LED on
                # stop conveyor
                print('Conveyor stop. Status: Normal condition')
                greenON()
                convSTP()
                time.sleep(3)
                print(Weight)
                # print weight
                # luggage weight greater than 2kg
                if Weight >= '00020': 
                    print('Weight ok')

            # check if input = clear and output = block
            elif GPIO.input(InputSen) == 1 and GPIO.input(OutputSen) == 0:
                # this state would never happen
                # red LED on
                # stop conveyor
                print('Conveyor stop. Status: Check output')
                redON()
                convSTP()

            # check if input = block and output = block
            elif GPIO.input(InputSen) == 0 and GPIO.input(OutputSen) == 0:
                # Oversize too long bag,
                # stop conveyor
                print('Conveyor stop: Status: Oversize Bag or Multiple Bags ')
                redON()
                convSTP()
            # elif check scale greater than 2kg and trigger to bdk
            SerialTxMsg = "R"

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
    print('GPIO Cleanup.')
