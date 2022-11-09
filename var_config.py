###########################################################################################
### GPIO PART
###########################################################################################
import serial

# LED gpio address
LEDred = 13
LEDblue = 19
LEDgreen = 26

# Intrusion address
SenInt1 = 24
#SenInt2 = 23
#SenInt3 = 24

# sensor gpio address
InputSen = 20
OutputSen = 16
IntrusionSen = 21

# conveyor gpio address
ConREV = 12
ConFWD = 6

numRetries = 1

# conveyor delay time in milisecond
tBagMoveFWD = 1000
tBagMoveBWD = 3000
tBagStop = 1000
tBagMoveCont = 10000

###########################################################################################
### USB PART
###########################################################################################

# barcode scanner 1
bs1 = open("/dev/hidraw1", "r")
# barcode scanner 2
# bs2 = open("/dev/hidraw0", "r")
# barcode scanner 3
# bs3 = open("/dev/hidraw3", "r")

# weight scale
ser = serial.Serial('/dev/ttyUSB0', 9600)
