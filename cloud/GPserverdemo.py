import threading
import time
import GPy
import numpy as np
from matplotlib import pyplot as plt
from cloudUnit import cloudUnit
from poap.tcpserve import ThreadedTCPServer
from poap.strategy import FixedSampleStrategy
from poap.strategy import InputStrategy

# Evaluate points in initial sweep
numevals = 20
X = np.linspace(-3, 3, num=numevals)

# Start Up TCP Server
strategy = FixedSampleStrategy(X)
server = ThreadedTCPServer(sockname=('0.0.0.0', 3000), strategy=strategy)

# Get Server Socket
name = server.sockname 
print "Starting Server on socket ", name

# Start CloudUnit Worker
unit = cloudUnit('xenon-marker-147522')
unit.startWorker()
print "Worker Successfully Started"

# Start Server
cthread = threading.Thread(target=server.run)
cthread.start()
cthread.join()
Xnew = np.zeros([len(server.controller.fevals), 1])
Ynew = np.zeros([len(server.controller.fevals), 1])
for k in range(len(server.controller.fevals)):
	Ynew[k] = server.controller.fevals[k].value
	Xnew[k] = server.controller.fevals[k].params
kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)
plt.ion()
plt.show()
for i in range(2,len(Xnew)):
	m = GPy.models.GPRegression(Xnew[0:i],Ynew[0:i],kernel)
	fig = m.plot()
	plt.pause(.5)
result = server.controller.best_point()
unit.cleanupWorkers()
print("Final: {0:.3e} @ {1}".format(result.value, result.params))
