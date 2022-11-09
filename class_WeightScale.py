from datetime import *
from var_config import *  # config io address for weight scale, conveyor, LED

class ScanWeight:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):

        bRx = False
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " ScanWeight thread started...")
        while self._running:
            import var_global  # place where all variable needed
            if var_global.SerialTxMsg != "":
                ser.write(var_global.SerialTxMsg.encode("utf-8"))
                var_global.SerialTxMsg = ""
                bRx = True
            if bRx:
                RxMsg = ser.readline()
                # print(RxMsg)
                # print(len(RxMsg))
                if len(RxMsg) == 13:
                    RxMsg = RxMsg.decode("utf-8")
                    RxMsg = RxMsg[4:9]
                    var_global.Weight = str(int(float(RxMsg) * 10)).zfill(5)
                    print(datetime.now().strftime(
                        "%H:%M:%S.%f") + " Weight: " + var_global.Weight)
                    if var_global.bDebug:
                        var_global.SocketTxMsg1 = "Weight: " + var_global.Weight + "\n"
                    bRx = False
                else:
                    print("Error")
                    var_global.Weight = ""
                    bRx = False