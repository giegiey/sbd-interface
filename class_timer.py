
from datetime import *
import time

class Timer1:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        import var_global  # place where all variable needed
        # print out timer to start
        print(datetime.now().strftime("%H:%M:%S.%f") +
              " Timer 1s thread started...")
        # off debug time and set to false
        var_global.bDebugTime = False

        while self._running:
            next_call1 = time.time()
            while True:
                import var_global  # place where all variable needed
                next_call1 = next_call1+1
                max(0, next_call1 - time.time())
                time.sleep(next_call1 - time.time())
                if var_global.bGetWeight:
                    var_global.SerialTxMsg = "R"
                if var_global.bDebugTime:
                    MyDateTime = datetime.now()
                    print(datetime.now().strftime("%H:%M:%S.%f"))
