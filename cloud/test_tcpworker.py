import sys
import time
import logging
import argparse
from poap.tcpserve import SimpleSocketWorker

def f(x):
    logging.info("Request for {0}".format(x))
    if TIMEOUT > 0:
        time.sleep(TIMEOUT)
    logging.info("OK, done")
    return (x-1.23)*(x-1.23)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',)
args = parser.parse_args()
port = args.integers
port = port[0]
print "Launching worker on port ", port
name = ('localhost', int(port))
SimpleSocketWorker(f, sockname=name, retries=1).run()
