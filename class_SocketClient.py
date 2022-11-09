from datetime import *
import var_global  # place where all variable needed

class ScanSocket:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global s
        fConnected = False
        host = "192.168.1.33"
        port = 48000
        print(datetime.now().strftime("%H:%M:%S.%f") +
              "ScanSocket thread started...")
        print("Host: " + host + " : " + str(port))

        while self._running:
            if fConnected == False:
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((host, port))
                print("Socket connected!!!")
                fConnected = True
            else:
                msg = s.recv(1024)
                var_global.SocketRxMsg = msg.decode(encoding='UTF-8')
                #print ("Socket Received : " + SocketMsg)