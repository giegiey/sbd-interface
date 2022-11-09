from datetime import *
import var_global  # place where all variable needed

class ScanBarCode3:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " ScanBarCode3 thread started...")
        while self._running:
            import var_global  # place where all variable needed
            var_global.BarCode3 = input("")
            if var_global.bDebug:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Code3: " + var_global.BarCode3)
                txMsg = "Code3: " + var_global.BarCode3 + "\n"
                var_global.SocketTxMsg3 = txMsg