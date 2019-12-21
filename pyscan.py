#!/usr/bin/env python
# -*- coding: utf-8 -*-

from signal import signal, SIGINT
from queue import Queue

import argparse
import sys
import socket
import threading

MAX_THREADS = 100
TCP_MAX_PORT = 2048
TCP_TIMEOUT = 0.15

scan_results = {}

class CustomArgumentsParser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write("error: %s\n" % message)
		self.print_help()
		sys.exit(2)

def port_check(ip, port, timeout):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.settimeout(timeout)

    try:
        tcp_socket.connect((ip, port))
        scan_results[port] = 'Open'
    except:
        scan_results[port] = ''

def dispatch(ip, q, timeout):
    while True:
        job = q.get()
        port_check(ip, job, timeout)
        q.task_done()

def signal_handler(signal_received, frame):
	exit(0)

def main():
    signal(SIGINT, signal_handler)
    
    argp = CustomArgumentsParser()
    argp.add_argument('-s', '--server', help='IP address of server to scan.', required=True)
    argp.add_argument('-d', '--delay', help='The delay between port connections. Default: %s seconds.' % TCP_TIMEOUT, type=int, nargs='?', const=1, default=TCP_TIMEOUT)
    argp.add_argument('-m', '--maxport', help='The maximum port number to scan. Default: %s.' % TCP_MAX_PORT, type=int, nargs='?', const=1, default=TCP_MAX_PORT)
    argp.add_argument('-t', '--threads', help='The number of threads to spawn for scanning. Default: %s threads.' % MAX_THREADS, type=int, nargs='?', const=1, default=MAX_THREADS)
    args = argp.parse_args()

    q = Queue()
    lock = threading.Lock()

    for x in range(args.threads):
        t = threading.Thread(target=dispatch, args=(args.server,q,args.delay,))
        t.daemon = True
        t.start()

    for port in range(args.maxport):
        q.put(port)
    
    q.join()

    for i in range(args.maxport):
        if scan_results[i] == 'Open':
            print("%s\t%s\t%s" % (i, scan_results[i], socket.getservbyport(i)))

if __name__ == '__main__': main()