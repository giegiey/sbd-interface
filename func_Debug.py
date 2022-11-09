from datetime import *
import RPi.GPIO as GPIO
from var_config import *  # config io address for weight scale, conveyor, LED

def State_Debug():
    import var_global  # place where all variable needed
    global s

    if var_global.bNewCommand:
        var_global.bNewCommand = False

        # alive
        if var_global.Com2 == 0:
            var_global.SocketTxMsg1 = "002,000\n"
            # s.send(str.encode("002,000"))

        # mode
        elif var_global.Com2 == 100:
            if var_global.Com3 == 0:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " State --> Idle")
                var_global.SocketTxMsg1 = "State --> Idle\n"
                var_global.bDebug = False
                #s.send(str.encode("State --> Idle"))
                var_global.State = 0
            else:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " State still in Debug")
                var_global.SocketTxMsg1 = "State still in Debug\n"
                #s.send(str.encode("State still in Debug"))

        # read Input
        elif var_global.Com2 == 101:
            strTemp = "IO "
            if (GPIO.input(14) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"
            if (GPIO.input(15) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"
            if (GPIO.input(15) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"
            if (GPIO.input(23) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"

            if (GPIO.input(InputSen) == 1):
                strTemp = strTemp + " 1"
            else:
                strTemp = strTemp + " 0"
            if (GPIO.input(25) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"
            if (GPIO.input(8) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"
            if (GPIO.input(7) == 1):
                strTemp = strTemp + "1"
            else:
                strTemp = strTemp + "0"

            if (GPIO.input(12) == 1):
                strTemp = strTemp + " 1\n"
            else:
                strTemp = strTemp + " 0\n"

            print(datetime.now().strftime("%H:%M:%S.%f") + " " + strTemp)
            var_global.SocketTxMsg1 = strTemp
            # s.send(str.encode(strTemp))

        # read BarCode
        elif var_global.Com2 == 102:
            print(datetime.now().strftime("%H:%M:%S.%f") + " Barcode Eanbaled")

        # read Weight
        elif var_global.Com2 == 103:
            if var_global.Com3 == 0:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Weight read disabled")
                var_global.SocketTxMsg1 = "Weight read disabled\n"
                #s.send(str.encode("Weight read disabled"))
                var_global.bGetWeight = False
            else:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Weight read enabled")
                var_global.SocketTxMsg1 = "Weight read enabled\n"
                #s.send(str.encode("Weight read enabled"))
                var_global.bGetWeight = True
                var_global.SerialTxMsg = "R"

        # Set Ouput
        elif var_global.Com2 == 104:
            if var_global.Com3 == 10:
                GPIO.output(ConFWD, GPIO.HIGH)
                print("Set 10 ")
            elif var_global.Com3 == 11:
                GPIO.output(ConFWD, GPIO.LOW)
                print("Set 11 ")
            elif var_global.Com3 == 20:
                GPIO.output(ConREV, GPIO.HIGH)
            elif var_global.Com3 == 21:
                GPIO.output(ConREV, GPIO.LOW)
            elif var_global.Com3 == 30:
                GPIO.output(22, GPIO.HIGH)
            elif var_global.Com3 == 31:
                GPIO.output(22, GPIO.LOW)
            elif var_global.Com3 == 40:
                GPIO.output(27, GPIO.HIGH)
            elif var_global.Com3 == 41:
                GPIO.output(27, GPIO.LOW)

            elif var_global.Com3 == 50:
                GPIO.output(17, GPIO.HIGH)
            elif var_global.Com3 == 51:
                GPIO.output(17, GPIO.LOW)
            elif var_global.Com3 == 60:
                GPIO.output(4, GPIO.HIGH)
            elif var_global.Com3 == 61:
                GPIO.output(4, GPIO.LOW)
            elif var_global.Com3 == 70:
                GPIO.output(3, GPIO.HIGH)
            elif var_global.Com3 == 71:
                GPIO.output(3, GPIO.LOW)
            elif var_global.Com3 == 80:
                GPIO.output(2, GPIO.HIGH)
            elif var_global.Com3 == 81:
                GPIO.output(2, GPIO.LOW)

            print(datetime.now().strftime("%H:%M:%S.%f") + "Set IO done")
            var_global.SocketTxMsg1 = "Set IO done\n"
            #s.send(str.encode("Set IO ok"))

        elif var_global.Com2 == 105:
            if var_global.Com3 == 1:
                var_global.bTestIntrusion = True
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Intrusion Sensor Test -> On")

            else:
                var_global.bTestIntrusion = False
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Intrusion Sensor Test -> Off")

    if var_global.bTestIntrusion:

        if GPIO.input(15) == 1:
            if GPIO.input(15) == 1:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Luggage Sensor ")