from datetime import *
import var_global  # place where all variable needed

class ScanBarCode2:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " ScanBarCode2 thread started...")
        while self._running:
            import var_global  # place where all variable needed
            var_global.BarCode2 = input("")
            if var_global.bDebug:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Code2: " + var_global.BarCode2)
                txMsg = "Code2: " + var_global.BarCode2 + "\n"
                var_global.SocketTxMsg2 = txMsg