import threading
import time
import globals


class BandwidthMonitor(threading.Thread):

    def __init__(self):
        """
        initializing basic local variables
        """
        self.start = 0
        self.end = 0
        self.curr_amount = 0
        globals.init()

    def initialization(self):
        """
        this method initiates a timer
        :return: void
        """
        self.start = time.time()

    def terminate(self):
        """
        this method cleans the global & local
        variables and sets the total running time
        :return: void
        """
        self.curr_amount = globals.amount[0]
        globals.amount[0] = 0
        self.end = time.time()

    def get_bandwidth(self):
        """
        simulates bandwidth format
        :return: void
        """
        return self.curr_amount/(self.end - self.start)
