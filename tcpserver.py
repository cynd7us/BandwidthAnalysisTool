#!/usr/bin/env python

import select
import sys
import socket
import threading
import globals


class TCPServer:

    def __init__(self, port):
        """
        initializing basic local variables
        :param port: port which the server runs on
        """
        self.host = ""
        self.port = port
        self.backlog = 5
        self.size = 1024
        self.socket = None
        self.threads = []
        globals.init()
        globals.amount[0] = 0

    def open_conn(self):
        """
        this method opens connection to other socket and binds the connection.
        :return: void
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a = self.socket.bind((self.host, self.port))
            b = self.socket.listen(self.backlog)
            globals.logger.debug("socket has been initialized and bind.")
        except socket.error, (value, message):
            if self.socket:
                self.socket.close()
            globals.logger.error("Couldn't open connection to socket: " + message)
            sys.exit(1)

    def run(self):
        """
        this function responsible on running the server socket
        and receive data from the other point socket.
        :return:
        """
        globals.logger.debug("run method under tcpserver.py has been started")
        self.open_conn()
        inputs = [self.socket]
        running = 1

        while running:
            readable, writable, exceptional = select.select(inputs, [], [])
            for s in readable:
                if s == self.socket:
                    c = ThreadedClient(self.socket.accept())
                    c.setDaemon(True)
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    line = sys.stdin.readline()
                    if line.strip() == "q":
                        running = 0
                    else:
                        pass

        print "Received signal to stop."
        self.socket.close()

        for c in self.threads:
            c.running = 0
            c.join()


class ThreadedClient(threading.Thread):

    def __init__(self, (client, address)):
        """
        initializing basic local variables
        :param port: port which the server runs on
        """
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.running = 1
        globals.init()

    def run(self):
        """
        this function responsible on running the client threaded socket
        meaning this is a paralleled method
        :return:
        """
        globals.logger.debug("run method under ThreadedClient class in the tcpserver.py has been started.")
        while self.running:
            try:
                data = self.client.recv(self.size)
            except socket.error, e:
                globals.logger.warning("error while receiving data, : " + str(e))

            if data:
                globals.amount[0] += len(data)
            else:
                globals.amount[0] = 0
                self.client.close()
                self.running = 0