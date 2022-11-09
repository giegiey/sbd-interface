from datetime import *
import var_global  # place where all variable needed

class ScanBarCode1:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " ScanBarCode1 thread started...")
        while self._running:
            import var_global  # place where all variable needed
            var_global.BarCode1 = input("")
            if var_global.bDebug:
                print(datetime.now().strftime(
                    "%H:%M:%S.%f") + " Code1: " + var_global.BarCode1)
                txMsg = "Code1: " + var_global.BarCode1 + "\n"
                var_global.SocketTxMsg1 = txMsg