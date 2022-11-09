from datetime import *
import RPi.GPIO as GPIO
from var_config import *  # config io address for weight scale, conveyor, LED


def State_Move():
    import var_global  # place where all variable needed
    var_global.bBCchecking = True
    var_global.bBCpass = False

    if var_global.bNewCommand:
        var_global.bNewCommand = False
        if var_global.Com2 == 0:
            var_global.SocketTxMsg1 = "002,000\n"
        elif var_global.Com2 == 4:
            print (datetime.now().strftime("%H:%M:%S.%f") + " Move    : Reset, Return to idle")
            GPIO.output(ConREV,GPIO.HIGH)
            GPIO.output(ConFWD,GPIO.HIGH)
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
            GPIO.output(LEDred,GPIO.HIGH)
            GPIO.output(LEDblue,GPIO.HIGH)
            GPIO.output(LEDgreen,GPIO.LOW)
        elif var_global.Com2 == 5:
            var_global.bBCchecking = False
            if var_global.Com3 == 1:
                var_global.bBCpass = True
        elif var_global.Com2 == 6:
            if not var_global.bBlinkRed:
                var_global.bBlinkRed = True
        elif var_global.Com2 == 8:
            var_global.bBCheavyEnable = True 
        elif var_global.Com2 == 9:
            var_global.SocketTxMsg1 = var_global.SocketTxMsgOld
            var_global.bPrint = False
        elif var_global.Com2 == 100:
            if var_global.Com3 == 0:
                print (datetime.now().strftime("%H:%M:%S.%f") + " State still in Idle")
                var_global.SocketTxMsg1 = "State still in Idle\n"
            else:
                print (datetime.now().strftime("%H:%M:%S.%f") + " State --> Debug")
                var_global.SocketTxMsg1 = "State --> Debug\n"
                var_global.State = 100
        
    if var_global.BarCode1 != "":
        if len(var_global.BarCode1) == 10:
            if var_global.BarCode1 == var_global.BarCodeOld:
                var_global.BCtime = datetime.now()
                print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Repeated")
            else:
                if var_global.BarCodeOld == "":
                    var_global.BCtime = datetime.now()
                    var_global.BarCodeOld = var_global.BarCode1
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode New: " + var_global.BarCodeOld)
                else:
                    var_global.bBCmultiple = True
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Mutiple ")
        else:
            if len(var_global.BarCode1) == 6:
                if var_global.BarCode1 == "012345":
                    var_global.bBCheavyFound = True
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Heavy ")
                else:
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Incomplete ")
            else:
                print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Incomplete ")
        var_global.BarCode1 = ""   
        
    if var_global.BarCode2 != "":
        if len(var_global.BarCode2) == 10:
            if var_global.BarCode2 == var_global.BarCodeOld:
                var_global.BCtime = datetime.now()
                print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Repeated")
            else:
                if var_global.BarCodeOld == "":
                    var_global.BCtime = datetime.now()
                    var_global.BarCodeOld = var_global.BarCode2
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode New: " + var_global.BarCodeOld)
                else:
                    var_global.bBCmultiple = True
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Mutiple ")
        else:
            if len(var_global.BarCode2) == 6:
                if var_global.BarCode2 == "012345":
                    var_global.bBCheavyFound = True
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Heavy ")
                else:
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Incomplete ")
            else:
                print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Incomplete ")
        var_global.BarCode2 = ""
                
    if var_global.BarCode3 != "":
        if len(var_global.BarCode3) == 10:
            if var_global.BarCode3 == var_global.BarCodeOld:
                var_global.BCtime = datetime.now()
                print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Repeated")
            else:
                if var_global.BarCodeOld == "":
                    var_global.BCtime = datetime.now()
                    var_global.BarCodeOld = var_global.BarCode3
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode New: " + var_global.BarCodeOld)
                else:
                    var_global.bBCmultiple = True
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Mutiple ")
        else:
            if len(var_global.BarCode3) == 6:
                if var_global.BarCode3 == "012345":
                    var_global.bBCheavyFound = True
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Heavy ")
                else:
                    print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Incomplete ")
            else:
                print (datetime.now().strftime("%H:%M:%S.%f") + " Move : BarCode Incomplete ")
        var_global.BarCode3 = ""

# ------------------------------

# ------------------------------
# Intrusion Sensor
    if GPIO.input(SenInt1) == 1:
        if GPIO.input(SenInt1) == 1:
            if GPIO.input(SenInt1) == 1:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Intrusion Sensor 1 ")
                var_global.iStep = 99

# ------------------------------
    if var_global.iStep == 1:
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " Move 1 : Conveyor Foward ")
        GPIO.output(ConREV, GPIO.HIGH)
        GPIO.output(ConFWD, GPIO.LOW)
        var_global.iStep += 1

# ------------------------------
    elif var_global.iStep == 2:
        if GPIO.input(OutputSen) == 0:
            if GPIO.input(OutputSen) == 0:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Move 2 : Sensor got luggage")
                var_global.startTime = datetime.now()
                var_global.iStep += 1

# ------------------------------
#     Stop conveyor
# ------------------------------

    elif var_global.iStep == 3:
        diffTime = datetime.now() - var_global.startTime
        if ((diffTime.seconds * 1000) + (diffTime.microseconds / 1000)) >= tBagMoveFWD:
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Move  3 : Conveyor Stop")
            GPIO.output(ConFWD, GPIO.HIGH)
            var_global.startTime = datetime.now()
            var_global.iStep += 1

# ------------------------------
    elif var_global.iStep == 4:
        diffTime = datetime.now() - var_global.startTime
        if ((diffTime.seconds * 1000) + (diffTime.microseconds / 1000)) >= tBagStop:
            # GPIO.output(ConFWD,GPIO.HIGH)
            if var_global.bBCmultiple:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Move  4 : Error, Multiple BarCode ")
                if (var_global.nRetry <= 0):
                    var_global.SocketTxMsg1 = "002,003,007\n"
                errorCode = 1
                var_global.iStep += 1
            else:
                if var_global.BarCodeOld != "":
                    if (var_global.bBCheavyEnable):
                        if (var_global.bBCheavyFound):
                            print(datetime.now().strftime("%H:%M:%S.%f") +
                                  " Move  4 : Success with BC Heavy" + var_global.BarCodeOld)
                            var_global.SocketTxMsg1 = "002,002," + var_global.BarCodeOld + "\n"
                            errorCode = 0
                            var_global.iStep = 10
                        else:
                            print(datetime.now().strftime("%H:%M:%S.%f") +
                                  " Move  4 : Error, BC Heavy but with Barcode ")
                            if (var_global.nRetry <= 0):
                                var_global.SocketTxMsg1 = "002,003,008\n"
                            var_global.iStep += 1
                    else:
                        print(datetime.now().strftime("%H:%M:%S.%f") +
                              " Move  4 : Success " + var_global.BarCodeOld)
                        var_global.SocketTxMsg1 = "002,002," + var_global.BarCodeOld + "\n"
                        errorCode = 0
                        var_global.iStep = 10
                else:
                    print(datetime.now().strftime("%H:%M:%S.%f") +
                          " Move  4 : Error, No BarCode ")
                    if (var_global.nRetry <= 0):
                        var_global.SocketTxMsg1 = "002,003,003\n"
                    var_global.iStep += 1

# ------------------------------
    elif var_global.iStep == 5:
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " Move  5 : Conveyor Backward ")
        # GPIO.output(LEDred,GPIO.LOW)
        GPIO.output(LEDgreen, GPIO.HIGH)
        var_global.bBlinkRed = True
        GPIO.output(ConREV, GPIO.LOW)
        GPIO.output(ConFWD, GPIO.HIGH)
        var_global.startTime = datetime.now()
        var_global.iStep += 1

# ------------------------------
    elif var_global.iStep == 6:
        if GPIO.input(InputSen) == 1:
            if GPIO.input(InputSen) == 1:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Move  6 : Sensor no luggage")
                var_global.startTime = datetime.now()
                var_global.iStep += 1

# ------------------------------
    elif var_global.iStep == 7:
        diffTime = datetime.now() - var_global.startTime
        if ((diffTime.seconds * 1000) + (diffTime.microseconds/1000)) >= (tBagMoveBWD):
            GPIO.output(ConREV, GPIO.HIGH)
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Move  7 : Conveyor stop ")
            if (var_global.nRetry <= 0):
                var_global.iStep = 100
            else:
                var_global.nRetry -= 1
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Move  7 : Retry " + str(var_global.nRetry))
                var_global.iStep = 1

# ------------------------------
    elif var_global.iStep == 10:
        if var_global.bBCchecking == False:
            if var_global.bBCpass == True:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Move 10 : Conveyor Foward ")
                GPIO.output(ConFWD, GPIO.LOW)
                GPIO.output(ConREV, GPIO.HIGH)
                var_global.startTime = datetime.now()
                var_global.iStep += 1
            else:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                      " Move 10 : Barcode Server Check Fail ")
                var_global.nRetry = 0
                var_global.iStep = 5

# ------------------------------
    elif var_global.iStep == 11:
        diffTime = datetime.now() - var_global.startTime
        if ((diffTime.seconds*1000) + (diffTime.microseconds/1000)) >= tBagMoveCont:
            GPIO.output(ConFWD, GPIO.HIGH)
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  " Move 11 : Conveyor stop ")
            var_global.iStep = 100

# ------------------------------
    elif var_global.iStep == 99:  # Intrusion red light alert
        GPIO.output(LEDred, GPIO.LOW)
        GPIO.output(LEDgreen, GPIO.HIGH)
        var_global.bBlinkRed = True
        var_global.SocketTxMsg1 = "002,003,002\n"
        var_global.iStep += 1

# ------------------------------
    elif var_global.iStep == 100:
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " Move 100 : Ends, Return to idle")
        GPIO.output(ConFWD, GPIO.HIGH)
        GPIO.output(ConREV, GPIO.HIGH)
        var_global.bBCheavyEnable = False
        var_global.bBCheavyFound = False
        var_global.BarCodeOld = ""
        var_global.WeightOld = "00000"
        var_global.bBCmultiple = False
        var_global.State = 0
        var_global.iStep = 0

    if var_global.SocketTxMsg1 != "":
        var_global.SocketTxMsgOld = var_global.SocketTxMsg1

