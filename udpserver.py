#!/usr/bin/env python

import socket
from numpy import *
import globals


class Server:
    def __init__(self, port):
        """
        initializing basic local variables
        :param port: port which the server runs on
        """
        self.host = "0.0.0.0"
        self.port = port
        self.backlog = 5
        self.size = 70000  # maximum size
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
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = self.socket.bind((self.host, self.port))
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
        globals.logger.debug("run method under udpserver.py has been started")
        self.open_conn()
        running = 1

        while running:
            try:
                data = self.socket.recv(self.size)
            except socket.error, e:
                globals.logger.warning("error while receiving data: " + str(e))

            if data:
                globals.amount[0] += len(data)
            else:
                globals.amount[0] = 0
                running = 0

        print "Received signal to stop connection."
        self.socket.close()

        for c in self.threads:
            c.running = 0
            c.join()

    def receive(self):
        """
        this method responsible on receiving data from the other point socket
        :return: transmitted data
        """
        globals.logger.debug("receive method under udpserver.py has been started")
        data_buffer = ""
        running = 1
        while running:
            try:
                data, address = self.socket.recvfrom(self.size)
            except socket.error:
                globals.logger.warning("error while receiving from data: " + str(e))

            if data:
                globals.amount[0] += len(data)
            else:
                globals.amount[0] = 0
                running = 0
        return data_buffer