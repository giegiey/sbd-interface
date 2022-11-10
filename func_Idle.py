from datetime import *
import RPi.GPIO as GPIO
from var_config import *  # config io address for weight scale, conveyor, LED

def State_Idle():
    import var_global  # place where all variable needed

    #auto detect if input sensor blocked meaning got luggage
    if GPIO.input(InputSen) == 0 and GPIO.input(OutputSen) == 1:
            var_global.bGetWeight = True
            # Checking weight of luggage
            # if more than 200gram
            if (var_global.Weight >= '00002'):
                print(datetime.now().strftime("%H:%M:%S.%f") +
                  'AHBL 1: Luggage detected on input sensor')
                var_global.bGetWeight = False
                var_global.AHBLStep = 2
                var_global.bBlinkRed = False
                var_global.bBlinkRedStop = True
                GPIO.output(LEDred, GPIO.HIGH)
                GPIO.output(LEDblue, GPIO.LOW)
                GPIO.output(LEDgreen, GPIO.LOW)
                var_global.State = 3

    if var_global.bNewCommand: # check if new command send
        var_global.bNewCommand = False # reject if already send
        if var_global.Com2 == 0: # 001, 000
            var_global.SocketTxMsg1 = "002,000\n"

        # 001, 001 : Get luggage weight
        elif var_global.Com2 == 1:
            print(datetime.now().strftime("%H:%M:%S.%f") + "(000 Msg) Idle : Get Weight")
            var_global.bGetWeight = True

        # 001, 002 : Start to check the luggage process
        elif var_global.Com2 == 2: 
            var_global.bGetWeight = False
            var_global.iStep = 1
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " State --> (002 Msg) Move Conveyor")
            var_global.bBlinkRed = False
            var_global.bBlinkRedStop = True
            GPIO.output(LEDred, GPIO.HIGH)
            GPIO.output(LEDgreen, GPIO.LOW)
            var_global.nRetry = numRetries
            var_global.State = 2

        # 001, 090 : Start Assisted Heavy Bag Loading
        elif var_global.Com2 == 90:
            var_global.bGetWeight = False
            var_global.AHBLStep = 1
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " AHBL State --> (090 Msg) Assisted Heavy Bag Loading ")
            var_global.bBlinkRed = False
            var_global.bBlinkRedStop = True
            GPIO.output(LEDred, GPIO.HIGH)
            GPIO.output(LEDblue, GPIO.LOW)
            GPIO.output(LEDgreen, GPIO.LOW)
            var_global.State = 3

        # 001, 001 : Reset everything or cancel
        elif var_global.Com2 == 4:
            print(datetime.now().strftime("%H:%M:%S.%f") + "(004 Msg) Idle : Reset")
            # resetAll()
            GPIO.output(ConFWD, GPIO.HIGH)
            GPIO.output(ConREV, GPIO.HIGH)
            var_global.bGetWeight = False
            var_global.BarCodeOld = ""
            var_global.WeightOld = "00000"
            var_global.bBCmultiple = False
            var_global.bBCheavyEnable = False
            var_global.bBCheavyFound = False
            var_global.State = 0
            var_global.iStep = 0
            var_global.bBlinkGreen = False
            var_global.bBlinkRed = False
            var_global.bBlinkRedStop = True
            GPIO.output(LEDgreen, GPIO.LOW)
        
        # 001, 005 : Check intrusion sensor
        elif var_global.Com2 == 5:
            bSensorDetect = False
            if GPIO.input(OutputSen) == 1:
                if GPIO.input(OutputSen) == 1:
                    if GPIO.input(OutputSen) == 1:
                        print(datetime.now().strftime(
                            "%H:%M:%S.%f") + " Conveyor, Detected ")
                        bSensorDetect = True
                        sensorCode = 1
            if bSensorDetect:
                if sensorCode == 1:
                    var_global.SocketTxMsg1 = "002,005,001\n"
                else:
                    var_global.SocketTxMsg1 = "002,005,002\n"
            else:
                var_global.SocketTxMsg1 = "002,005,000\n"
        
        # 001, 006 : Error red LED blinking
        elif var_global.Com2 == 6: 
            if not var_global.bBlinkRed:
                var_global.bBlinkRed = True
                GPIO.output(LEDgreen, GPIO.HIGH)
        
        # 001, 006 :  heavy weight luggage detected
        elif var_global.Com2 == 8:
            var_global.bBCheavyEnable = True
            var_global.bGetWeight = False
            var_global.iStep = 1
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " State --> Move Conveyor")
            var_global.bBlinkRed = False
            var_global.bBlinkRedStop = True
            GPIO.output(LEDred, GPIO.HIGH)
            GPIO.output(LEDgreen, GPIO.LOW)
            var_global.State = 2
        elif var_global.Com2 == 9:
            var_global.SocketTxMsg1 = var_global.SocketTxMsgOld
            var_global.bPrint = True
        elif var_global.Com2 == 100:
            if var_global.Com3 == 0:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " State still in Idle")
                var_global.SocketTxMsg1 = "State still in Idle\n"
            else:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " State --> Debug")
                var_global.SocketTxMsg1 = "State --> Debug\n"
                var_global.State = 100

# Extra command LED

# For Maintanange page
        elif var_global.Com2 == 11:  # Green
            print(datetime.now().strftime("%H:%M:%S.%f") + " Test LED : Green")
            GPIO.output(LEDgreen, GPIO.LOW)
        elif var_global.Com2 == 12:  # Blue
            print(datetime.now().strftime("%H:%M:%S.%f") + " Test LED : Blue")
            GPIO.output(LEDblue, GPIO.LOW)
        elif var_global.Com2 == 13:  # Red
            print(datetime.now().strftime("%H:%M:%S.%f") + " Test LED : Red")
            GPIO.output(LEDred, GPIO.LOW)
        elif var_global.Com2 == 20:  # Off
            print(datetime.now().strftime("%H:%M:%S.%f") + " Test LED : Off")
            GPIO.output(LEDgreen, GPIO.HIGH)
            GPIO.output(LEDblue, GPIO.HIGH)
            GPIO.output(LEDred, GPIO.HIGH)
# Extra command Conveyor
        elif var_global.Com2 == 14:  # Forward
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Test conveyor : Conveyor Forward ")
            GPIO.output(ConFWD, GPIO.LOW)
            GPIO.output(ConREV, GPIO.HIGH)
        elif var_global.Com2 == 15:  # Reverse
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Test conveyor : Conveyor Reverse ")
            GPIO.output(ConREV, GPIO.LOW)
            GPIO.output(ConFWD, GPIO.HIGH)
        elif var_global.Com2 == 16:  # Stop
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Test conveyor : Conveyor Stop ")
            # stop reverse
            GPIO.output(ConFWD, GPIO.HIGH)
            GPIO.output(ConREV, GPIO.HIGH)

        elif var_global.Com2 == 17:  # Output Sensor
            if (GPIO.input(OutputSen) == 1):  # change Output sensor logic
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Test Output Sensor : Clear")
                var_global.SocketTxMsg1 = "Clear"
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Test Output Sensor : Block")
                var_global.SocketTxMsg1 = "Block"

        elif var_global.Com2 == 18:  # CheckInput Sensor
            if (GPIO.input(InputSen) == 1):  # change Input sensor logic
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Test Input Sensor : Clear")
                var_global.SocketTxMsg1 = "Clear"
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Test Input Sensor : Block")
                var_global.SocketTxMsg1 = "Block"

        elif var_global.Com2 == 19:  # Top Intrusion Sensor(Reverse logic)
            # If 0 mean clear
            if (GPIO.input(IntrusionSen) == 0):  # change Intrusion sensor logic
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Test Top Intrusion Sensor : Clear")
                var_global.SocketTxMsg1 = "Clear"
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Test Top Intrusion Sensor : Block")
                var_global.SocketTxMsg1 = "Block"
        elif var_global.Com2 == 21:  # Barcode 1
            var_global.bGetWeight = False
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Test Barcode: " + var_global.BarCodeOld)
            var_global.SocketTxMsg1 = var_global.BarCodeOld+"\n"
            var_global.BarCodeOld = ""
        elif var_global.Com2 == 22:  # Weight scale
            var_global.bGetWeight = True
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Test Weight: " + var_global.WeightOld)
            var_global.SocketTxMsg1 = var_global.WeightOld+"\n"

    if var_global.Weight != "":
        var_global.WeightOld = var_global.Weight
        var_global.SocketTxMsg2 = "002,001," + var_global.WeightOld + "\n"
        var_global.Weight = ""

    if var_global.SocketTxMsg1 != "":
        var_global.SocketTxMsgOld = var_global.SocketTxMsg1

    # timeout for barcode when no weight
    if var_global.BarCodeOld != "" and var_global.WeightOld == "00000":
        timeDiff = datetime.now() - var_global.BCtime
        if ((timeDiff.seconds*1000) + (timeDiff.microseconds/1000)) > 2000:
            var_global.BarCodeOld = ""
            var_global.bBCmultiple = False
            var_global.bBCheavyFound = False

    if var_global.BarCode1 != "":
        if len(var_global.BarCode1) == 10:
            if var_global.BarCode1 == var_global.BarCodeOld:
                var_global.BCtime = datetime.now()
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Idle : BarCode 1 Repeated")
            else:
                if var_global.BarCodeOld == "":
                    var_global.BCtime = datetime.now()
                    var_global.BarCodeOld = var_global.BarCode1
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 1 New: " + var_global.BarCodeOld)
                else:
                    var_global.bBCmultiple = True
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 1 Mutiple ")
        else:
            if len(var_global.BarCode1) == 6:
                if var_global.BarCode1 == "012345":
                    var_global.bBCheavyFound = True
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 1 Heavy ")
                else:
                    var_global.BarCodeOld = var_global.BarCode1
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 1 Incomplete ")
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Idle : BarCode 1 Incomplete ")
        var_global.BarCode1 = ""

    if var_global.BarCode2 != "":
        if len(var_global.BarCode2) == 10:
            if var_global.BarCode2 == var_global.BarCodeOld:
                var_global.BCtime = datetime.now()
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Idle : BarCode 2 Repeated")
            else:
                if var_global.BarCodeOld == "":
                    var_global.BCtime = datetime.now()
                    var_global.BarCodeOld = var_global.BarCode2
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 2 New: " + var_global.BarCodeOld)
                else:
                    var_global.bBCmultiple = True
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 2 Mutiple ")
        else:
            if len(var_global.BarCode2) == 6:
                if var_global.BarCode2 == "012345":
                    var_global.bBCheavyFound = True
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 2 Heavy ")
                else:
                    var_global.BarCodeOld = var_global.BarCode2
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 2 Incomplete ")
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Idle : BarCode 2 Incomplete ")
        var_global.BarCode2 = ""

    if var_global.BarCode3 != "":
        if len(var_global.BarCode3) == 10:
            if var_global.BarCode3 == var_global.BarCodeOld:
                var_global.BCtime = datetime.now()
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Idle : BarCode 3 Repeated")
            else:
                if var_global.BarCodeOld == "":
                    var_global.BCtime = datetime.now()
                    var_global.BarCodeOld = var_global.BarCode3
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 3 New: " + var_global.BarCodeOld)
                else:
                    var_global.bBCmultiple = True
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 3 Mutiple ")
        else:
            if len(var_global.BarCode3) == 6:
                if var_global.BarCode3 == "012345":
                    var_global.bBCheavyFound = True
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 3 Heavy ")
                else:
                    var_global.BarCodeOld = var_global.BarCode3
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Idle : BarCode 3 Incomplete ")
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Idle : BarCode 3 Incomplete ")
        var_global.BarCode3 = ""