# SBD Release 03112022

from threading import Thread
from socket import *
from datetime import *

import RPi.GPIO as GPIO

# -----------------------------------------------------------------------------------
# SBD Module
from var_config import *  # config io address for weight scale, conveyor, LED
from class_timer import Timer1  # run timer to keep alive
from class_LED import TimerLED  # run LED
from class_Barcode1 import ScanBarCode1  # run barcode scanner 1
from class_Barcode2 import ScanBarCode2  # run barcode scanner 2
from class_Barcode3 import ScanBarCode3  # run barcode scanner 3
from class_WeightScale import ScanWeight  # run weight scale
from class_SocketServer import SocketServer  # socket server
# from class_SocketClient import ScanSocket #socket server
from func_Debug import State_Debug  # to run debug mode
from func_Idle import State_Idle  # receive socket client message process
from func_Weight import State_Weight  # run move process
from func_Move import State_Move  # run the process step by step
from func_AHBL import State_AHBL  # run the process AHBL
import var_global  # place where all variable needed
from var_gpiosetup import *  # gpio setup

# -----------------------------------------------------------------------------------
# map the inputs to the function blocks
ManageState = {0: State_Idle,
               1: State_Weight,
               2: State_Move,
               3: State_AHBL,
               100: State_Debug,
               }


# -----------------------------------------------------------------------------------
# Start programs
print("Program starts")

ts1 = Timer1()
var_global.ts1Thread = Thread(target=ts1.run)
var_global.ts1Thread.start()

tsLED = TimerLED()
var_global.tsLEDThread = Thread(target=tsLED.run)
var_global.tsLEDThread.start()

global sbc1
sbc1 = ScanBarCode1()
var_global.sbcThread1 = Thread(target=sbc1.run)
var_global.sbcThread1.start()

#global sbc2
#sbc2 = ScanBarCode2()
#var_global.sbcThread2 = Thread(target=sbc2.run)
#var_global.sbcThread2.start()

#global sbc3
#sbc3 = ScanBarCode3()
#var_global.sbcThread3 = Thread(target=sbc3.run)
#var_global.sbcThread3.start()

sw = ScanWeight()
var_global.swThread = Thread(target=sw.run)
var_global.swThread.start()


#ss = ScanSocket()
#ssThread = Thread(target=ss.run)
# ssThread.start()
global ss
ss = SocketServer()
ss.start()

try:
    while True:
        import var_global  # place where all variable needed
        if var_global.SocketRxMsg != "":
            var_global.SocketRxMsg = var_global.SocketRxMsg.strip()
            var_global.SocketRxMsg = var_global.SocketRxMsg.split(" ")
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Main, Socket Message: " + var_global.SocketRxMsg[0])
            RxMsg = var_global.SocketRxMsg[0].split(",")
            RxMsgLen = len(RxMsg)
            if RxMsg[0] == "001":
                tempStr = RxMsg[1].lstrip("0")
                if tempStr == "":
                    var_global.Com2 = 0
                else:
                    var_global.Com2 = int(tempStr)
                    if RxMsgLen == 3:
                        tempStr = RxMsg[2].strip()
                        var_global.Com3 = int(tempStr)

                #print("Main, Com2: " + str(Com2))
                # if RxMsgLen == 3:
                #   print("Main, Com3: " + str(Com3))

                var_global.bNewCommand = True
            var_global.SocketRxMsg = ""

        ManageState[var_global.State]()

# When you press ctrl+c, this will be called
finally:
    sbc1.terminate()
    ss.terminate()
    print("Goodbye :)")
    GPIO.cleanup()
