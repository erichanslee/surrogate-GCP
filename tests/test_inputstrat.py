import sys
import time
import logging
import threading
import GPy
import numpy as np
import matplotlib.pyplot as plt
import pdb
from IPython.display import display
from poap.strategy import FixedSampleStrategy
from poap.strategy import InputStrategy
from poap.tcpserve import ThreadedTCPServer
from poap.tcpserve import SimpleSocketWorker


# Set up default host, port, and time
TIMEOUT = 0


def f(x):
	logging.info("Request for {0}".format(x))
	if TIMEOUT > 0:
		time.sleep(TIMEOUT)
	logging.info("OK, done")
	return np.sin(x) + np.random.randn()*.05


def worker_main(name):
	logging.info("Launching worker on port {0}".format(name[1]))
	SimpleSocketWorker(f, sockname=name, retries=1).run()


def main():
	logging.basicConfig(format="%(name)-18s: %(levelname)-8s %(message)s",
						level=logging.INFO)

	# Launch controller
	strategy = FixedSampleStrategy([])
	server = ThreadedTCPServer()
	tstrategy = InputStrategy(server.controller, strategy);
	X = np.random.uniform(-3.,3.,(50,1))
	Y = np.ones([len(X), 1])
	for k in X:
		tstrategy.eval(k)
	server.strategy = tstrategy
	cthread = threading.Thread(target=server.run)
	cthread.start()

	# Get controller port
	name = server.sockname
	logging.info("Launch controller at {0}".format(name))

	# Launch workers
	numworkers = 5;
	wthreads = []
	for k in range(numworkers):
		wthread = threading.Thread(target=worker_main, args=(name,))
		wthread.start()
		wthreads.append(wthread)


	# Wait on controller and workers
	cthread.join()
	for t in wthreads:
		t.join()


	# Copy data from worker evals
	offset = numworkers;
	Xnew = np.zeros([len(server.controller.fevals)-offset, 1])
	Ynew = np.zeros([len(server.controller.fevals)-offset, 1])
	for k in range(len(server.controller.fevals)-offset):
		Ynew[k] = server.controller.fevals[k].value[0]
		Xnew[k] = server.controller.fevals[k].params[0]

	# Start GP
	kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)
	m = GPy.models.GPRegression(Xnew,Ynew,kernel)
	fig = m.plot()
	regfig = GPy.plotting.show(fig)
	regfig.savefig('test-GP-sinwave.png')
	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		TIMEOUT = float(sys.argv[1])
	main()
