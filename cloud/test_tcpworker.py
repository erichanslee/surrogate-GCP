import sys
import time
import logging
import argparse
import threading
from poap.tcpserve import SimpleSocketWorker

timeout = 0

def f(x):
	logging.info("Request for {0}".format(x))
	if timeout > 0:
		time.sleep(timeout)
	logging.info("OK, done")
	return (x-1.23)*(x-1.23)

def worker_main(name):
	logging.info("Launching worker on port {0}".format(name[1]))
	SimpleSocketWorker(f, sockname=name, retries=1).run()

def main():
	logging.basicConfig(format="%(name)-18s: %(levelname)-8s %(message)s",level=logging.INFO)
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('integers', metavar='N', type=int, nargs='+',)
	args = parser.parse_args()
	port = args.integers
	port = port[0]
	print "Launching worker on port ", port

	# Make sure to change 'localhost' to the internal/external IP required
	name = ('localhost', int(port))
	wthreads = []
	for k in range(2):
		wthread = threading.Thread(target=worker_main, args=(name,))
		wthread.start()
		wthreads.append(wthread)	
	for t in wthreads:
		t.join()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        TIMEOUT = float(sys.argv[1])
    main()
