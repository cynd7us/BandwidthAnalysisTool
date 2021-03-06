#!/usr/bin/env python

"""
Docstring classification for udp client class
"""

import socket
import sys
import globals

class TCPClient:

    def __init__(self, ip, port):
        """
        initializing basic local variables
        :param port: port which the client runs on
        :param ip: host on which the client runs on
        """
        self.host = ip
        self.port = port
        self.size = 1024
        self.socket = None
        globals.init()
        globals.amount[0] = 0

    def open_conn(self):
        """
        this method opens connection to other socket and binds the connection.
        :return: void
        """
        globals.logger.debug("open_conn method under tcpclient.py has been started.")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except socket.error, e:
            print "Error, server refused connection."
            globals.logger.warning("error while initializing socket connection, : " + str(e))

    def close_conn(self):
        self.socket.close()

    def send(self, message):
        """
        this method sends data to the other point socket
        :param message: data to send
        :return: void
        """
        globals.logger.debug("send method under tcpclient.py has been started")
        try:
            self.socket.sendto(message, (self.host, self.port))
        except socket.error, e:
            globals.logger.error("Error, send request failed, :" + str(e))
            self.close_conn()
            sys.exit(0)

    def spam(self):
        """
        this method responsible on spamming the server
        this done by sending the maximum safe TCP pakcet size
        DOC of maximum TCP packet size: http://stackoverflow.com/a/35697810/5392156
        :return: void
        """
        globals.logger.debug("spam method under tcpclient.py has been started.")
        buff = 1024 * '\0'
        print "spamming server"
        while 1:
            try:
                self.send(buff)
                globals.amount[0] += len(buff)
            except socket.error, e:
                globals.logger.warning("error while spamming server, : " + str(e))
                return