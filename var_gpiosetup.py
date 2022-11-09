
import RPi.GPIO as GPIO

from var_config import *  # config io address for weight scale, conveyor, LED

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# Set Sennsor pin as input
GPIO.setup(InputSen, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OutputSen, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IntrusionSen, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(LEDgreen, GPIO.OUT)
GPIO.setup(LEDblue, GPIO.OUT)
GPIO.setup(LEDred, GPIO.OUT)
GPIO.setup(ConFWD, GPIO.OUT)
GPIO.setup(ConREV, GPIO.OUT)

GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
GPIO.output(4, GPIO.HIGH)
GPIO.output(LEDgreen, GPIO.HIGH)
GPIO.output(LEDblue, GPIO.HIGH)
GPIO.output(LEDred, GPIO.HIGH)
GPIO.output(ConFWD, GPIO.HIGH)
GPIO.output(ConREV, GPIO.HIGH)

