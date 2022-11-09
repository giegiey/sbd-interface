from datetime import *
import RPi.GPIO as GPIO
import time
from var_config import *  # config io address for weight scale, conveyor, LED


class TimerLED:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " Timer LED thread started...")

        while self._running:
            import var_global  # place where all variable needed
            next_call2 = time.time()
            while True:
                next_call2 = next_call2+1
                max(0, next_call2 - time.time())
                time.sleep(next_call2 - time.time())
                if var_global.bBlinkRedStop:
                    GPIO.output(LEDred, GPIO.HIGH)
                    GPIO.output(LEDgreen, GPIO.LOW)
                    GPIO.output(LEDblue, GPIO.HIGH)
                    var_global.bBlinkRedStop = False
                if var_global.bBlinkGreenStop:
                    GPIO.output(LEDred, GPIO.HIGH)
                    GPIO.output(LEDgreen, GPIO.HIGH)
                    GPIO.output(LEDblue, GPIO.HIGH)
                    var_global.bBlinkGreenStop = True
                if var_global.bBlinkRed:
                    GPIO.output(LEDblue, GPIO.HIGH)
                    GPIO.output(LEDgreen, GPIO.HIGH)
                    if var_global.bRed:
                        GPIO.output(LEDred, GPIO.HIGH)
                        var_global.bRed = False
                    else:
                        GPIO.output(LEDred, GPIO.LOW)
                        var_global.bRed = True
                if var_global.bBlinkGreen:
                    GPIO.output(LEDred, GPIO.HIGH)
                    GPIO.output(LEDblue, GPIO.HIGH)
                    if var_global.bGreen:
                        GPIO.output(LEDgreen, GPIO.HIGH)
                        var_global.bGreen = False
                    else:
                        GPIO.output(LEDgreen, GPIO.LOW)
                        var_global.bGreen = True
