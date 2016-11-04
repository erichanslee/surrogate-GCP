from poap.tcpserve import SocketWorker
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',)
args = parser.parse_args()
port = args.integers
port = port[0]
print "Launching worker on port ", port
name = ('localhost', int(port))
SocketWorker(sockname=name, retries=1).run()
