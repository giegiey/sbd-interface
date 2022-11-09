from datetime import *
import RPi.GPIO as GPIO
from var_config import *  # config io address for weight scale, conveyor, LED


def State_AHBL():
    import var_global  # place where all variable needed
    var_global.bBCchecking = True
    var_global.bBCpass = False

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
    if var_global.AHBLStep == 1:
        # input/output sensor 1: clear 0: block
        # check if input = block and output = clear
        if GPIO.input(InputSen) == 0 and GPIO.input(OutputSen) == 1:
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  'AHBL 1: Luggage detected on input sensor')
            var_global.AHBLStep += 1

# ------------------------------
    if var_global.AHBLStep == 2:
        print(datetime.now().strftime("%H:%M:%S.%f") +
              'AHBL 2: Conveyor move forward')
        # Conveyor forward
        GPIO.output(ConREV, GPIO.HIGH)
        GPIO.output(ConFWD, GPIO.LOW)
        # Blue LED ON
        GPIO.output(LEDred, GPIO.HIGH)
        GPIO.output(LEDblue, GPIO.LOW)
        GPIO.output(LEDgreen, GPIO.HIGH)
        var_global.AHBLStep += 1

# ------------------------------
    if var_global.AHBLStep == 3:
        # input/output sensor 1: clear 0: block
        # check if input = clear and output = clear
        if GPIO.input(InputSen) == 1 and GPIO.input(OutputSen) == 1:
            # normal condition
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  'AHBL 3: Normal COndition. Conveyor stop')
            # Red LED ON
            GPIO.output(LEDred, GPIO.HIGH)
            GPIO.output(LEDblue, GPIO.HIGH)
            GPIO.output(LEDgreen, GPIO.LOW)
            var_global.AHBLStep = 100
        # check if input = block and output = block
        # input/output sensor 1: clear 0: block
        elif GPIO.input(OutputSen) == 0:
            # Oversize too long bag,
            print(datetime.now().strftime("%H:%M:%S.%f") +
                  'AHBL 3: Oversize Bag or Multiple Bags. Conveyor stop')
            # stop conveyor
            GPIO.output(ConREV, GPIO.HIGH)
            GPIO.output(ConFWD, GPIO.HIGH)
            # Red LED ON
            GPIO.output(LEDred, GPIO.HIGH)
            GPIO.output(LEDblue, GPIO.LOW)
            GPIO.output(LEDgreen, GPIO.HIGH)
            var_global.bBlinkRed = True
            var_global.AHBLStep = 4

# ------------------------------
    # Reverse conveyor
    if var_global.AHBLStep == 4:
        print(datetime.now().strftime("%H:%M:%S.%f") +
              "AHBL 4 : Conveyor Backward ")
        GPIO.output(LEDred,GPIO.LOW)
        GPIO.output(LEDblue, GPIO.HIGH)
        GPIO.output(LEDgreen, GPIO.HIGH)
        var_global.bBlinkRed = True
        GPIO.output(ConREV, GPIO.LOW)
        GPIO.output(ConFWD, GPIO.HIGH)
        var_global.AHBLStep = 5

# ------------------------------
    # Check input if blocked
    if var_global.AHBLStep == 5:
        # input/output sensor 1: clear 0: block
        # check if input = block
        if GPIO.input(InputSen) == 0:
            if GPIO.input(InputSen) == 0:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                  "AHBL 5 : Check Input sensor if block  ")
                var_global.AHBLStep = 6

# ------------------------------
    # Check input if blocked
    if var_global.AHBLStep == 6:
        # input/output sensor 1: clear 0: block
        # check if input = clear
        if GPIO.input(InputSen) == 1:
            if GPIO.input(InputSen) == 1:
                print(datetime.now().strftime("%H:%M:%S.%f") +
                "AHBL 6 : Check Input sensor if clear and stop conveyor  ")
                var_global.AHBLStep = 100

# ------------------------------
    elif var_global.AHBLStep == 99:  # Intrusion red light alert
        GPIO.output(LEDred, GPIO.LOW)
        GPIO.output(LEDgreen, GPIO.HIGH)
        var_global.bBlinkRed = True
        var_global.SocketTxMsg1 = "002,003,002\n"
        var_global.AHBLStep += 1

# ------------------------------
    elif var_global.AHBLStep == 100:
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " Move 100 : Ends, Return to idle")
        GPIO.output(ConFWD, GPIO.HIGH)
        GPIO.output(ConREV, GPIO.HIGH)
        var_global.WeightOld = "00000"
        var_global.bBCmultiple = False
        var_global.State = 0
        var_global.AHBLStep = 0

    if var_global.SocketTxMsg1 != "":
        var_global.SocketTxMsgOld = var_global.SocketTxMsg1
