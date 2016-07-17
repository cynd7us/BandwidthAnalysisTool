#!/usr/bin/env python

import sys
import time
import socket
from bandwidth_monitor import BandwidthMonitor
from tcpclient import TCPClient
import tcpserver
import threading
from udpclient import UDPClient
from udpserver import Server
from config_helper import read_config_map, update_key_value
import plotly.plotly as py
import plotly.graph_objs as go
from random import randint
import plotly
import globals


def generate_plotly_graph(x_axis, y_axis, protocol):
    """
    Plotly - Make charts and dashboards online which you find under https://plot.ly/
    This function responsible on creating a plotly graph.
    The graph stands as a visualization tool to view & transmit the bandwidth from the last running.
    :param x_axis: x axis label
    :param y_axis: y axis label
    :param protocol: protocol (udp/tcp)
    :return: opens chrome / default browser to Plotly graph view
    """
    data = [go.Scatter(x=x_axis, y=y_axis)]
    layout = go.Layout(title=protocol + " Bandwidth summary",
                       xaxis=dict(title="Seconds",
                                  titlefont=dict(
                                      family = "Courter New, monospace",
                                      size = 18,
                                      color = "#7f7f7f"
                                      )
                                  ),
                       yaxis=dict(title="Packet Size",
                                  titlefont=dict(
                                      family="Courier New, monospace",
                                      size=18,
                                      color="#7f7f7f"
                                    )
                                  )
                       )
    fig = go.Figure(data=data, layout=layout)
    file_name = "sysrun-" + str(randint(1000, 9999))
    plot_url = py.plot(fig, filename=file_name)
    print "connection to Plotly has been enabled. Please visit your account"
    print "The current run graph summary is under %s file" % file_name

if __name__ == "__main__":

    plotly.tools.set_credentials_file(username='oramranov', api_key='zf86oqsk6c')
    host = ""
    port = ""
    type = ""
    debug = ""
    visualization = ""
    globals.init()

    running_requests = 0
    total_bandwidth = 0
    max_bandwidth = 0
    monitor = BandwidthMonitor()
    time_test = int(read_config_map("runtime_globals")["test_time"])
    y_axis = []
    x_axis = []

    try:
        host = sys.argv[1]
        port = sys.argv[2]
        protocol = sys.argv[3]
        type = sys.argv[4]
        debug = sys.argv[5]
        visualization = sys.argv[6]
        globals.logger.debug("script parameters transferred successfully.")
    except IndexError:
        host = read_config_map("runtime_globals")["host"][1:-1]
        port = int(read_config_map("runtime_globals")["port"])
        protocol = read_config_map("runtime_globals")["protocol"][1:-1]
        type = read_config_map("runtime_globals")["type"][1:-1]
        debug = read_config_map("runtime_globals")["debug"]
        update_key_value("runtime_globals", "debug", debug)
        visualization = read_config_map("runtime_globals")["visualization"]
        globals.logger.debug("script parameters set to default via the config file.")

    if type == "s":
        if protocol == 'tcp':
            try:
                globals.logger.debug("script has been enabled as a tcp server type.")
                server_obj = tcpserver.TCPServer(int(port))
                thread_manager = threading.Thread(target=server_obj.run)
            except socket.error, e:
                globals.logger.warning("an error has been occurred. Message info: " + str(e))
                sys.exit(1)

        elif protocol == 'udp':
            try:
                globals.logger.debug("script has been enabled as a udp server type.")
                server_obj = Server(int(port))
                print "Hit any key to terminate server connection. "
                thread_manager = threading.Thread(target=server_obj.run)
            except socket.error, e:
                globals.logger.warning("an error has been occurred. Message info: " + str(e))
                sys.exit(1)

        thread_manager.setDaemon(False)
        thread_manager.start()
        print "Starting Bandwidth monitor"

        while running_requests <= time_test:
            monitor.initialization()
            time.sleep(1)
            monitor.terminate()
            speed = monitor.get_bandwidth() / (1000 * 1000)
            if float(speed) > 0:
                running_requests += 1
                y_axis.append(float(speed))
                x_axis.append(running_requests)
            if float(speed) > float(max_bandwidth):
                max_bandwidth = speed
            print str(speed) + " Mbytes/Second"
            total_bandwidth = str(float(total_bandwidth) + float(speed))

        print "process finished."
        print "%d seconds summary: " % time_test
        print "====================="
        print "Total bandwidth: " + total_bandwidth
        print "Maximum bandwidth request: " + str(max_bandwidth)
        print "====================="
        # data = [go.Scatter(
        # x=['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
        # y=[1, 3, 6])]
        monitor.terminate()
        if len(y_axis) > 0 and len(x_axis) > 0:
            generate_plotly_graph(x_axis, y_axis, protocol)

    elif type == "c":
        if protocol == 'tcp':
            globals.logger.debug("script has been enabled as a tcp client type")
            print "Starting TCP client"
            client_obj = TCPClient(host, int(port))
            client_obj.open_conn()
            thread_manager = threading.Thread(target=client_obj.spam)

        elif protocol == 'udp':
            globals.logger.debug("script has been enabled as a udp client type")
            print "Starting UDP client"
            client_obj = UDPClient(host, int(port))
            client_obj.open_conn()
            thread_manager = threading.Thread(target=client_obj.spam)

        thread_manager.setDaemon(False)
        thread_manager.start()
        for i in xrange(time_test):
            monitor.initialization()
            time.sleep(1)
            monitor.terminate()
            curr_payload = monitor.get_bandwidth() / (1000 * 1000)

            print str(curr_payload) + "MBytes/s payload sent."

        print "Data has been transmitted successfully."
        monitor.terminate()
