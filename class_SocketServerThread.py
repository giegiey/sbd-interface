from threading import Thread
from datetime import *
import select


class SocketServerThread(Thread):
    def __init__(self, client_sock, client_addr, number):
        """ Initialize the Thread with a client socket and address """
        Thread.__init__(self)
        self.client_sock = client_sock
        self.client_addr = client_addr
        self.number = number

    def run(self):
        print("{} [Thr {}] SocketServerThread starting with client {}".format(
            datetime.now().strftime("%H:%M:%S.%f"), self.number, self.client_addr))
        self.__stop = False
        while not self.__stop:
            import var_global  # place where all variable needed
            if self.client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select(
                        [self.client_sock, ], [self.client_sock, ], [], 5)
                except select.error as err:
                    print('[Thr {}] Select() failed on socket with {}'.format(
                        self.number, self.client_addr))
                    self.stop()
                    return

                if len(rdy_read) > 0:
                    read_data = self.client_sock.recv(255)

                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('[Thr {}] {} closed the socket.'.format(
                            self.number, self.client_addr))
                        self.stop()
                    else:
                        # Strip newlines just for output clarity
                        #print('[Thr {}] Received {}'.format(self.number, read_data.rstrip()))
                        var_global.SocketRxMsg = str(read_data.rstrip())
                        var_global.SocketRxMsg = var_global.SocketRxMsg.rstrip("\n'")
                        var_global.SocketRxMsg = var_global.SocketRxMsg.lstrip("b'")

                if var_global.SocketTxMsg1 != "":
                    #print('[Thr {}] Send{}'.format(self.number, var_global.SocketTxMsg))
                    self.client_sock.send(str.encode(var_global.SocketTxMsg1))
                    if var_global.bPrint:
                        var_global.bPrint = False
                        print(" Message " + var_global.SocketTxMsg1)
                    var_global.SocketTxMsg1 = ""

                if var_global.SocketTxMsg2 != "":
                    #print('[Thr {}] Send{}'.format(self.number, var_global.SocketTxMsg2))
                    self.client_sock.send(str.encode(var_global.SocketTxMsg2))
                    var_global.SocketTxMsg2 = ""

                if var_global.SocketTxMsg3 != "":
                    #print('[Thr {}] Send{}'.format(self.number, var_global.SocketTxMsg3))
                    self.client_sock.send(str.encode(var_global.SocketTxMsg3))
                    var_global.SocketTxMsg3 = ""

            else:
                print("[Thr {}] No client is connected, SocketServer can't receive data".format(
                    self.number))
                self.stop()
        self.close()

    def stop(self):
        self.__stop = True

    def close(self):
        """ Close connection with the client socket. """
        if self.client_sock:
            print('[Thr {}] Closing connection with {}'.format(
                self.number, self.client_addr))
            self.client_sock.close()